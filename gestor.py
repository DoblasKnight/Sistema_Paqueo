import time

class GestorParqueo:
    def __init__(self, estados, log_callback=None):
        self.estados = estados
        self.log = log_callback

    def log_evento(self, mensaje):
        if self.log:
            self.log(mensaje)
        else:
            print(mensaje)

    def asignar_puesto(self, placa):
        placa = placa.strip().upper()
        if not placa:
            return
        for i, estado in enumerate(self.estados):
            if not estado['ocupado'] and not estado['asignado']:
                self.estados[i] = {
                    'placa': placa,
                    'asignado': True,
                    'ocupado': True,  # Temporal hasta confirmación por cámara
                    'tiempo_asignado': time.time(),
                    'tiempo_ocupado': None
                }
                self.log_evento(f"🟢 Se asignó el puesto {i+1} a {placa}")
                return
        self.log_evento("🔴 No hay puestos libres para asignar.")

    def registrar_salida(self, placa):
        placa = placa.strip().upper()
        if not placa:
            return
        for i, estado in enumerate(self.estados):
            if estado['placa'] == placa:
                self.estados[i] = {
                    'placa': None,
                    'asignado': False,
                    'ocupado': False,
                    'tiempo_asignado': None,
                    'tiempo_ocupado': None
                }
                self.log_evento(f"🚗 {placa} ha salido del puesto {i+1}")
                return
        self.log_evento(f"❓ No se encontró la placa {placa} en ningún puesto.")
