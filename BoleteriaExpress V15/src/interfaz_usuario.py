"""
Interfaz principal del usuario - Punto de entrada para el sistema de usuario
"""

import tkinter as tk
from src.utilidades import crear_estilo_ventana
from src.archivos import cargar_usuarios
from src.sistema_usuario import mostrar_home_usuario
from src.configuracion import COLORS
from src.autenticacion import abrir_admin_en_ventana

def iniciar_sistema_usuario(root, usuario_logueado):
    """Sistema principal para usuarios"""
    # Limpiar ventana
    for widget in root.winfo_children():
        widget.destroy()
    
    # Configurar ventana
    usuarios = cargar_usuarios()
    nombre_completo = usuarios.get(usuario_logueado, {}).get("nombre_completo", "Usuario")
    
    crear_estilo_ventana(root, f" Boletería Express Ecuador - {nombre_completo}", "1000x700")

    # Barra de navegación superior
    nav_frame = tk.Frame(root, bg=COLORS['primary'], height=80)
    nav_frame.pack(fill='x')
    nav_frame.pack_propagate(False)
    
    tk.Label(nav_frame, text=f"¡Bienvenido {nombre_completo}! |  Boletería Express", 
             font=('Arial', 16, 'bold'), fg='white', bg=COLORS['primary']).pack(pady=10)

    # Botón para abrir Admin en otra ventana (opcional)
    tk.Button(nav_frame, text="Admin", command=lambda: abrir_admin_en_ventana(root),
              bg=COLORS['accent'], fg='white', relief='flat', padx=14, pady=6).pack(side='right', padx=18)

    # Frame para contenido
    content_frame_usuario = tk.Frame(root, bg=COLORS['background'])
    content_frame_usuario.pack(fill='both', expand=True, padx=10, pady=10)
    
    # Mostrar pantalla principal del usuario
    mostrar_home_usuario(content_frame_usuario, usuario_logueado)
    
    return content_frame_usuario