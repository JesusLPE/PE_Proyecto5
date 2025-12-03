import tkinter as tk
from PIL import Image, ImageTk

def ventana_funciones():
    win = tk.Toplevel()
    win.title("Funciones avanzadas")
    win.geometry("500x500")
    win.resizable(False, False)

    try:
        ruta_logo = "logodlaya.jpg"
        img_pil = Image.open(ruta_logo).resize((500, 500))
        logo_tk = ImageTk.PhotoImage(img_pil)

        label_logo = tk.Label(win, image=logo_tk)
        label_logo.pack(pady=10)
        label_logo.image = logo_tk

    except:
        tk.Label(win, text="[Error al cargar logo]", fg="red").pack(pady=10)

    tk.Label(win, text="FUNCIONES AVANZADAS",
             font=("Segoe UI", 16, "bold")).pack(pady=20)
