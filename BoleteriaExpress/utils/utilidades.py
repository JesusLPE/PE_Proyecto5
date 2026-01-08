import tkinter as tk
from tkinter import messagebox

def cerrar_ventana(ventana, root=None):
    """Cierra la ventana actual y muestra la raíz si se proporciona."""
    ventana.destroy()
    if root:
        root.deiconify()

def mostrar_mensaje(tipo, titulo, mensaje):
    """Muestra un mensaje usando messagebox."""
    if tipo == "info":
        messagebox.showinfo(titulo, mensaje)
    elif tipo == "error":
        messagebox.showerror(titulo, mensaje)
    elif tipo == "warning":
        messagebox.showwarning(titulo, mensaje)

def proximamente(nombre):
    """Muestra mensaje de función no implementada."""
    mostrar_mensaje("info", "Próximamente", f"La función '{nombre}' estará disponible próximamente.")