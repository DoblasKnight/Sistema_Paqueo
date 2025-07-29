import tkinter as tk
from tkinter import ttk
import threading

from detector import DetectorParqueadero
from tabla_estado import TablaEstado
from gestor import GestorParqueo

camera_url = "http://192.168.20.39:8080/video"
zonas = [
    # x, y, Tamaño
    (80, 590, 150, 150), (370, 590, 150, 150),
    (630, 590, 150, 150),(850, 590, 150, 150),
    (1060, 590, 150, 150), (1300, 590, 150, 150),
]
estados = [{'placa': None, 'asignado': False, 'ocupado': False,
            'tiempo_asignado': None, 'tiempo_ocupado': None} for _ in zonas]

# === INTERFAZ TKINTER ===
root = tk.Tk()
root.title("Sistema de Parqueo")

notebook = ttk.Notebook(root)
notebook.pack(padx=10, pady=10, fill='both', expand=True)

frame_tab1 = ttk.Frame(notebook)
frame_tab2 = ttk.Frame(notebook)

notebook.add(frame_tab1, text="Registrar entrada/salida")
notebook.add(frame_tab2, text="Estado de puestos")


# === COMPONENTES TAB1 ===
tk.Label(frame_tab1, text="Placa del vehículo:").grid(row=0, column=0, padx=5, pady=5)
entry_placa = ttk.Entry(frame_tab1, width=20)
entry_placa.grid(row=0, column=1, padx=5)

log = tk.Listbox(frame_tab1, width=60, height=10)
log.grid(row=1, column=0, columnspan=4, pady=10)

def log_evento(mensaje):
    log.insert(tk.END, mensaje)
    log.yview(tk.END)

gestor = GestorParqueo(estados, log_evento)

btn_asignar = ttk.Button(frame_tab1, text="Asignar puesto",
                         command=lambda: [gestor.asignar_puesto(entry_placa.get()), entry_placa.delete(0, tk.END)])
btn_asignar.grid(row=0, column=2, padx=5)

btn_salida = ttk.Button(frame_tab1, text="Registrar salida",
                        command=lambda: [gestor.registrar_salida(entry_placa.get()), entry_placa.delete(0, tk.END)])
btn_salida.grid(row=0, column=3, padx=5)

# === COMPONENTES TAB2 ===
tabla_estado = TablaEstado(frame_tab2, estados)
def loop_tabla():
    tabla_estado.actualizar()
    root.after(1000, loop_tabla)

# === PROCESAMIENTO VIDEO (hilo) ===
detector = DetectorParqueadero(camera_url, zonas, estados, log_callback=log_evento)
threading.Thread(target=detector.procesar, daemon=True).start()

# === INICIO INTERFAZ ===
root.after(1000, loop_tabla)
root.mainloop()