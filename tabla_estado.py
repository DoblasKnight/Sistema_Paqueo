import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from Style_Tkinter import aplicar_estilos

class TablaEstado:
    def __init__(self, root, estados):
        self.estados = estados
        aplicar_estilos()

        # Frame contenedor
        frame = ctk.CTkFrame(root, corner_radius=10)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Título arriba
        label = ctk.CTkLabel(
            frame,
            text="📋 Estado de puestos",
            font=("Arial", 16, "bold")
        )
        label.pack(pady=10)

        # Treeview (tabla)
        self.tabla = ttk.Treeview(
            frame,
            columns=("Puesto", "Estado", "Placa"),
            show='headings',
            height=8
        )
        self.tabla.heading("Puesto", text="Puesto")
        self.tabla.heading("Estado", text="Estado")
        self.tabla.heading("Placa", text="Placa")
        self.tabla.pack(fill="both", expand=True, padx=10, pady=10)

    def actualizar(self):
        self.tabla.delete(*self.tabla.get_children())
        for i, estado in enumerate(self.estados):
            texto_estado = "OCUPADO" if estado['ocupado'] else "LIBRE"
            placa = estado['placa'] if estado['placa'] else "-"
            color = "red" if estado['ocupado'] else "green"

            self.tabla.insert(
                '',
                'end',
                values=(i+1, texto_estado, placa),
                tags=(color,)
            )

        # Colores dinámicos para estado
        self.tabla.tag_configure("red", foreground="red")
        self.tabla.tag_configure("green", foreground="lime")
