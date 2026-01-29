"""
Módulo principal - Sistema de Boletería Express Ecuador
Punto de entrada de la aplicación
"""

import tkinter as tk
from src.archivos import inicializar_datos_prueba

# Variables globales que serán compartidas
asiento_seleccionado_var = None
root_global = None

def get_asiento_seleccionado_var():
    """Obtiene la variable global de asiento seleccionado"""
    global asiento_seleccionado_var
    if asiento_seleccionado_var is None:
        import tkinter as tk
        asiento_seleccionado_var = tk.StringVar()
        asiento_seleccionado_var.set("Ninguno")
    return asiento_seleccionado_var

def get_root_global():
    """Obtiene la ventana principal global"""
    global root_global
    return root_global

def main():
    """Función principal para inicializar la aplicación."""
    global asiento_seleccionado_var, root_global
    
    # Inicializar datos de prueba si no existen
    inicializar_datos_prueba()
    
    # Crear ventana principal
    root = tk.Tk()
    root.protocol("WM_DELETE_WINDOW", root.quit)
    
    # Inicializar variables Tkinter ANTES de cualquier otra cosa
    asiento_seleccionado_var = tk.StringVar()
    asiento_seleccionado_var.set("Ninguno")
    root_global = root
    
    # Importar y mostrar pantalla de inicio
    from src.autenticacion import mostrar_inicio
    mostrar_inicio(root)
    
    root.mainloop()

# Función para obtener la variable global
def get_asiento_seleccionado_var():
    return asiento_seleccionado_var

def get_root_global():
    return root_global

if __name__ == "__main__":
    main()