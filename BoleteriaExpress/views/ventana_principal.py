import tkinter as tk
from views.ventana_login import abrir_login
from views.ventana_registro import abrir_registro

def ventana_principal():
    root = tk.Tk()
    root.title("Boletería Express Ecuador - Inicio")
    root.state("zoomed")
    root.configure(bg="white")
    root.resizable(True, True)

    # Header con fondo celeste claro
    header = tk.Frame(root, bg="#e6f7ff", height=100)
    header.pack(fill="x")

    # Título principal
    titulo = tk.Label(
        header, text="EC Boletería Express Ecuador 🚍",
        fg="#003366", bg="#e6f7ff",
        font=("Segoe UI", 24, "bold")
    )
    titulo.pack(pady=20)

    # Subtítulo
    subtitulo = tk.Label(
        header, text="Portal de Venta de Boletos Interprovinciales",
        fg="#666666", bg="#e6f7ff",
        font=("Segoe UI", 12)
    )
    subtitulo.pack()

    # Cuerpo principal con botones centrados
    cuerpo = tk.Frame(root, bg="white")
    cuerpo.pack(expand=True)

    # Botón Ingresar como Usuario
    btn_ingresar = tk.Button(
        cuerpo, text="👤 Ingresar como Usuario",
        font=("Segoe UI", 14, "bold"),
        width=25, bg="#8B0000", fg="white",
        command=lambda: abrir_login(root)
    )
    btn_ingresar.pack(pady=20)

    # Botón Registrar Nuevo Usuario
    btn_registrar = tk.Button(
        cuerpo, text="📝 Registrar Nuevo Usuario",
        font=("Segoe UI", 14, "bold"),
        width=25, bg="#8B0000", fg="white",
        command=lambda: abrir_registro(root)
    )
    btn_registrar.pack(pady=20)

    # Botón Panel de Administrador
    btn_admin = tk.Button(
        cuerpo, text="⚙️ Panel de Administrador",
        font=("Segoe UI", 14, "bold"),
        width=25, bg="#FF0000", fg="white",
        command=lambda: abrir_login(root)
    )
    btn_admin.pack(pady=20)

    # Botón Salir (nuevo)
    btn_salir = tk.Button(
        cuerpo, text="Salir",
        font=("Segoe UI", 14, "bold"),
        width=25, bg="#FF0000", fg="white",
        command=root.destroy  # Cierra la aplicación completamente
    )
    btn_salir.pack(pady=20)

    root.mainloop()