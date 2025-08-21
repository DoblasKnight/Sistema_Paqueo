import cv2
import time

class DetectorParqueadero:
    def __init__(self, camera_url, zonas, estados, log_callback=None):
        self.camera_url = camera_url
        self.zonas = zonas
        self.estados = estados
        self.log_callback = log_callback

        self.cap = cv2.VideoCapture(self.camera_url)
        ret, frame = self.cap.read()
        if not ret:
            raise Exception("No se pudo conectar a la cámara.")
        
        self.frame_ref = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        self.frame_ref = cv2.GaussianBlur(self.frame_ref, (21, 21), 0)

    def log_evento(self, mensaje):
        if self.log_callback:
            self.log_callback(mensaje)
        else:
            print(mensaje)

    def procesar(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (21, 21), 0)

            ocupados_actuales = [False] * len(self.zonas)

            for i, (x, y, w, h) in enumerate(self.zonas):
                zona_base = self.frame_ref[y:y+h, x:x+w]
                zona_actual = gray[y:y+h, x:x+w]
                diff = cv2.absdiff(zona_base, zona_actual)
                _, thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)
                blancos = cv2.countNonZero(thresh)
                total = w * h
                porcentaje = (blancos / total) * 100

                if porcentaje > 3:
                    if self.estados[i]['tiempo_ocupado'] is None:
                        self.estados[i]['tiempo_ocupado'] = time.time()
                    elif time.time() - self.estados[i]['tiempo_ocupado'] >= 3:
                        self.estados[i]['ocupado'] = True
                else:
                    self.estados[i]['ocupado'] = False
                    self.estados[i]['tiempo_ocupado'] = None

                ocupado = self.estados[i]['ocupado']
                ocupados_actuales[i] = ocupado

                color = (0, 0, 255) if ocupado else (0, 255, 0)
                texto = f"{i+1}: {'OCUPADO' if ocupado else 'LIBRE'}"
                if self.estados[i]['placa']:
                    texto += f" - {self.estados[i]['placa']}"
                cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
                cv2.putText(frame, texto, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
                if self.estados[i]['placa']:
                    cv2.putText(frame, f"{self.estados[i]['placa']}", (x, y+h+20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,0), 2)

            for i, ocupado in enumerate(ocupados_actuales):
                if ocupado and self.estados[i]['placa'] is None:
                    for j, est in enumerate(self.estados):
                        if est['asignado'] and time.time() - est['tiempo_asignado'] >= 10:
                            self.log_evento(f"⚠️ {est['placa']} se parqueó en el puesto {i+1} en lugar del {j+1}. Actualizando...")
                            self.estados[i] = {
                                'placa': est['placa'],
                                'asignado': False,
                                'ocupado': True,
                                'tiempo_asignado': None,
                                'tiempo_ocupado': None
                            }
                            self.estados[j] = {'placa': None, 'asignado': False, 'ocupado': False, 'tiempo_asignado': None, 'tiempo_ocupado': None}
                            break

            for i, estado in enumerate(self.estados):
                if estado['asignado'] and time.time() - estado['tiempo_asignado'] >= 10:
                    if not ocupados_actuales[i]:
                        self.log_evento(f"⚠️ {estado['placa']} NO se parqueó en el puesto {i+1}. Se libera.")
                        self.estados[i] = {'placa': None, 'asignado': False, 'ocupado': False, 'tiempo_asignado': None, 'tiempo_ocupado': None}
                    else:
                        self.log_evento(f"✅ {estado['placa']} parqueado correctamente en el puesto {i+1}.")
                        self.estados[i]['asignado'] = False

            libres = sum(1 for est in self.estados if not est['ocupado'])
            cv2.putText(frame, f"LIBRES: {libres}/{len(self.zonas)}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)

            cv2.imshow("Camara - Parqueadero", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.cap.release()
        cv2.destroyAllWindows()
