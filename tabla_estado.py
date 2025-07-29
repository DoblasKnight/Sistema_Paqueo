import tkinter as tk
from tkinter import ttk

class TablaEstado:
    def __init__(self, root, estados):
        self.estados = estados
        self.tabla = ttk.Treeview(root, columns=("Puesto", "Estado", "Placa"), show='headings', height=6)
        self.tabla.heading("Puesto", text="Puesto")
        self.tabla.heading("Estado", text="Estado")
        self.tabla.heading("Placa", text="Placa")
        self.tabla.pack(padx=10, pady=10)

    def actualizar(self):
        self.tabla.delete(*self.tabla.get_children())
        for i, estado in enumerate(self.estados):
            texto_estado = "OCUPADO" if estado['ocupado'] else "LIBRE"
            placa = estado['placa'] if estado['placa'] else "-"
            self.tabla.insert('', 'end', values=(i+1, texto_estado, placa))