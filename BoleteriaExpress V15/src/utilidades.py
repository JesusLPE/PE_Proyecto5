"""
Utilidades comunes - Funciones de estilo y helpers
"""

import tkinter as tk
from tkinter import messagebox
from src.configuracion import COLORS

def crear_estilo_ventana(ventana, titulo, geometry="800x600"):
    """Aplica estilos consistentes a las ventanas"""
    ventana.title(titulo)
    ventana.geometry(geometry)
    ventana.config(bg=COLORS['background'])
    ventana.resizable(True, True) 
    
    # Centrar ventana
    ventana.update_idletasks()
    x = (ventana.winfo_screenwidth() // 2) - (ventana.winfo_width() // 2)
    y = (ventana.winfo_screenheight() // 2) - (ventana.winfo_height() // 2)
    ventana.geometry(f"{geometry}+{x}+{y}") 

def crear_boton_estilo(parent, text, command=None, color='primary', width=15):
    """Crea botones con estilo consistente"""
    bg_color = COLORS[color]
    
    btn = tk.Button(
        parent, 
        text=text, 
        command=command,
        bg=bg_color,
        fg='white',
        font=('Arial', 10, 'bold'),
        relief='flat',
        padx=20,
        pady=8,
        width=width,
        cursor='hand2'
    )
    # Asegurar que el botón responda al hover
    def on_enter(e):
        btn['bg'] = COLORS.get('accent', bg_color)
    def on_leave(e):
        btn['bg'] = bg_color
    
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)
    
    return btn

def crear_label_titulo(parent, text, size=16):
    """Crea labels de título con estilo"""
    return tk.Label(
        parent,
        text=text,
        font=('Arial', size, 'bold'),
        fg=COLORS['text_dark'],
        bg=COLORS['background']
    )

def crear_frame_contenedor(parent, padding=20):
    """Crea frame contenedor con estilo"""
    frame = tk.Frame(parent, bg=COLORS['white'], relief='raised', bd=1)
    frame.pack(padx=padding, pady=padding, fill='both', expand=True)
    return frame

def mostrar_info_sistema():
    """Muestra una caja de diálogo con información sobre el sistema."""
    info_text = (
        "Sistema de Boletería Express \n\n"
        "Primera Versión: 1.0 (Octubre 2025)\n"
        "Ultima Versión: 2.0 (Enero 2026)\n"
        "Desarrollado para la venta y gestión de boletos de bus interprovincial en Ecuador.\n\n"
        "Características:\n"
        " - Login y Registro de Usuarios\n"
        " - Login de Administrador (Usuario: admin, Contraseña: terminal)\n"
        " - Búsqueda de Rutas por Cooperativa\n"
        " - Selección visual de Asientos (Ficticio)\n"
        " - Historial de Compras de Usuario\n\n"
        "Gestión de Archivos (JSON): Los datos son almacenados localmente en archivos JSON."
    )
    messagebox.showinfo("Información del Sistema", info_text)

def crear_scrollable_frame(parent):
    """Crea un frame con scrollbar"""
    scroll_frame = tk.Frame(parent, bg=COLORS['white'])
    scroll_frame.pack(fill='both', expand=True)
    
    canvas = tk.Canvas(scroll_frame, bg=COLORS['white'], highlightthickness=0)
    scrollbar = tk.Scrollbar(scroll_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg=COLORS['white'])
    
    def on_frame_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))
    
    scrollable_frame.bind("<Configure>", on_frame_configure)
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    def on_canvas_resize(event):
        canvas.itemconfig(1, width=event.width)
    
    canvas.bind('<Configure>', on_canvas_resize)
    
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    return scrollable_frame, canvas