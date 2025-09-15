from tkinter import ttk

def aplicar_estilos():
    style = ttk.Style()
    style.theme_use("clam")

    # === Treeview Estilo Oscuro ===
    style.configure("Treeview",
        font=("Arial", 13),
        rowheight=28,
        background="#2b2b2b",
        foreground="white",
        fieldbackground="#2b2b2b",
        bordercolor="#2b2b2b"
    )
    # === Encabezados ===
    style.configure(
        "Treeview.Heading",
        background="#1f1f1f",
        foreground="white",
        font=("Arial", 14, "bold")
    )
    style.map(
    "Treeview.Heading",
    background=[("active", "#1f1f1f")],
)