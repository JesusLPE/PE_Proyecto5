import tkinter as tk
from ventana_login import abrir_login
from ventana_registro import abrir_registro

def ventana_principal():
    global root
    root = tk.Tk()
    root.title("Boletería Ecuador")
    root.geometry("1366x768")
    root.configure(bg="white")
    root.resizable(False, False)

    barra = tk.Frame(root, bg="#8B0000", height=60)
    barra.pack(fill="x")

    tk.Label(
        barra, text="Boletería Ecuador",
        fg="white", bg="#8B0000",
        font=("Segoe UI", 20, "bold")
    ).pack(side="left", padx=20)

    tk.Button(
        barra, text="Cerrar",
        command=root.destroy, bg="white", fg="black"
    ).pack(side="right", padx=10)

    cuerpo = tk.Frame(root, bg="white")
    cuerpo.pack(expand=True)

    tk.Button(
        cuerpo, text="Ingresar",
        font=("Segoe UI", 14, "bold"),
        width=20, bg="#B22222", fg="white",
        command=lambda: abrir_login(root)
    ).pack(pady=10)

    tk.Button(
        cuerpo, text="Registrar",
        font=("Segoe UI", 14),
        width=20, bg="#E05A5A", fg="white",
        command=lambda: abrir_registro(root)
    ).pack(pady=10)

    root.mainloop()
