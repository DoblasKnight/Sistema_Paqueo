import customtkinter as ctk
import threading

from detector import DetectorParqueadero
from tabla_estado import TablaEstado
from gestor import GestorParqueo

camera_url = "http://192.168.20.39:8080/video"
zonas = [
    (80, 590, 150, 150), (370, 590, 150, 150),
    (630, 590, 150, 150),(850, 590, 150, 150),
    (1060, 590, 150, 150), (1300, 590, 150, 150),
]
estados = [{'placa': None, 'asignado': False, 'ocupado': False,
            'tiempo_asignado': None, 'tiempo_ocupado': None} for _ in zonas]

# === CONFIGURACIÓN DE ESTILO ===
ctk.set_appearance_mode("dark")   # Apraiencia de la interfaz
ctk.set_default_color_theme("green")  
# === INTERFAZ PRINCIPAL ===
root = ctk.CTk()
root.title("Sistema de Parqueo Inteligente")
root.geometry("700x500")

tabview = ctk.CTkTabview(root, width=680, height=450)
tabview.pack(padx=10, pady=10, fill="both", expand=True)

tab1 = tabview.add("Registrar entrada/salida")
tab2 = tabview.add("Estado de puestos")

# === COMPONENTES TAB1 ===
ctk.CTkLabel(tab1, text="Placa del vehículo:", font=("Arial", 14)).grid(row=0, column=0, padx=10, pady=10)

entry_placa = ctk.CTkEntry(tab1, width=200, placeholder_text="ABC123")
entry_placa.grid(row=0, column=1, padx=10, pady=10)

log = ctk.CTkTextbox(tab1, width=500, height=200, wrap="word", state="disabled")
log.grid(row=1, column=0, columnspan=4, pady=15, padx=10)

def log_evento(mensaje):
    log.configure(state="normal") 
    log.insert("end", mensaje + "\n")
    log.see("end")
    log.configure(state="disabled") 

gestor = GestorParqueo(estados, log_evento)

btn_asignar = ctk.CTkButton(tab1, text="Asignar puesto",
    command=lambda: [gestor.asignar_puesto(entry_placa.get()), entry_placa.delete(0, "end")])
btn_asignar.grid(row=0, column=2, padx=10, pady=10)

btn_salida = ctk.CTkButton(tab1, text="Registrar salida",
    fg_color="red", hover_color="#b30000",
    command=lambda: [gestor.registrar_salida(entry_placa.get()), entry_placa.delete(0, "end")])
btn_salida.grid(row=0, column=3, padx=10, pady=10)

# === COMPONENTES TAB2 ===
tabla_estado = TablaEstado(tab2, estados)

def loop_tabla():
    tabla_estado.actualizar()
    root.after(1000, loop_tabla)

# === PROCESAMIENTO VIDEO EN HILO ===
detector = DetectorParqueadero(camera_url, zonas, estados, log_callback=log_evento)
threading.Thread(target=detector.procesar, daemon=True).start()

# === INICIO INTERFAZ ===
root.after(1000, loop_tabla)
root.mainloop()
