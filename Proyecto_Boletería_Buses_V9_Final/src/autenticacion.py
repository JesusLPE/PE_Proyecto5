"""
Módulo de autenticación - Login, registro y validación de usuarios
"""

import tkinter as tk
from tkinter import messagebox
from src.utilidades import crear_estilo_ventana, crear_frame_contenedor, crear_label_titulo, crear_boton_estilo
from src.archivos import cargar_usuarios, guardar_usuarios, cargar_administradores
from datetime import datetime

def mostrar_inicio(root):
    """Muestra la pantalla de inicio con opciones de login/registro."""
    for widget in root.winfo_children():
        widget.destroy()

    crear_estilo_ventana(root, "Boletería Express Ecuador - Inicio", "600x450")

    main_frame = crear_frame_contenedor(root, 30)

    titulo = crear_label_titulo(main_frame, "🇪🇨 Boletería Express Ecuador ", 20)
    titulo.pack(pady=(20, 10))
    titulo.config(bg='#FFFFFF')

    sub_titulo = tk.Label(main_frame, text="Portal de Venta de Boletos Interprovinciales",
                          font=('Arial', 12), fg='#7F8C8D', bg='#FFFFFF')
    sub_titulo.pack(pady=(0, 40))

    opciones_frame = tk.Frame(main_frame, bg='#FFFFFF')
    opciones_frame.pack(pady=10)

    btn_login_user = crear_boton_estilo(opciones_frame, " Ingresar como Usuario", 
                                        lambda: login_usuario(root), 'primary', 25)
    btn_login_user.pack(pady=10)

    btn_register = crear_boton_estilo(opciones_frame, " Registrar Nuevo Usuario", 
                                      lambda: mostrar_registro(root), 'success', 25)
    btn_register.pack(pady=10)

    btn_login_admin = crear_boton_estilo(opciones_frame, " Panel de Administrador", 
                                         lambda: login_admin(root), 'secondary', 25)
    btn_login_admin.pack(pady=10)

def mostrar_registro(root):
    """Muestra el formulario de registro"""
    for widget in root.winfo_children():
        widget.destroy()
        
    crear_estilo_ventana(root, "Registro de Usuario", "500x750")

    main_frame = crear_frame_contenedor(root, 15)
    
    titulo = crear_label_titulo(main_frame, " Registro de Usuario", 18)
    titulo.pack(pady=(20, 40))
    titulo.config(bg='#FFFFFF')
    
    campos = [
        ("Cédula (10 dígitos):", "cedula"),
        ("Nombres completos:", "nombre"),
        ("Teléfono (10 dígitos):", "telefono"),
        ("Email:", "email"),
        ("Usuario:", "usuario"),
        ("Contraseña:", "password1"),
        ("Repita Contraseña:", "password2")
    ]
    
    entradas = {}
    for label_text, key in campos:
        tk.Label(main_frame, text=label_text, font=('Arial', 10), 
                 fg='#2C3E50', bg='#FFFFFF').pack(anchor='w', padx=20, pady=(10, 5))
        
        if 'password' in key.lower():
            entrada = tk.Entry(main_frame, font=('Arial', 11), show="*", width=30)
        else:
            entrada = tk.Entry(main_frame, font=('Arial', 11), width=30)
        
        entrada.pack(padx=20, pady=(0, 5))
        entradas[key] = entrada

    def registrar():
        valores = {k: v.get().strip() for k, v in entradas.items()}
        
        # Validaciones
        if not all(valores.values()):
            messagebox.showerror("Error", "Por favor complete todos los campos.")
            return

        if len(valores['cedula']) != 10 or not valores['cedula'].isdigit():
            messagebox.showerror("Error", "La cédula debe tener exactamente 10 dígitos numéricos.")
            return

        if len(valores['telefono']) != 10 or not valores['telefono'].isdigit():
            messagebox.showerror("Error", "El teléfono debe tener exactamente 10 dígitos numéricos.")
            return

        if '@' not in valores['email'] or '.' not in valores['email']:
            messagebox.showerror("Error", "Ingrese un email válido.")
            return

        if valores['password1'] != valores['password2']:
            messagebox.showerror("Error", "Las contraseñas no coinciden.")
            return
            
        if len(valores['password1']) < 6:
            messagebox.showerror("Error", "La contraseña debe tener al menos 6 caracteres.")
            return

        usuarios = cargar_usuarios()
        if valores['usuario'] in usuarios:
            messagebox.showerror("Error", "El nombre de usuario ya existe.")
            return
            
        # Verificar cédula única
        for user_data in usuarios.values():
            if user_data.get('cedula') == valores['cedula']:
                messagebox.showerror("Error", "Esta cédula ya está registrada.")
                return

        usuarios[valores['usuario']] = {
            "contraseña": valores['password1'],
            "cedula": valores['cedula'],
            "nombre_completo": valores['nombre'],
            "telefono": valores['telefono'],
            "email": valores['email'],
            "fecha_registro": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "tipo": "usuario"
        }
        
        guardar_usuarios(usuarios)
        messagebox.showinfo("¡Registro Exitoso!", f"Usuario '{valores['usuario']}' creado exitosamente.")
        mostrar_inicio(root)

    frame_botones = tk.Frame(main_frame, bg='#FFFFFF')
    frame_botones.pack(pady=30)
    
    btn_registrar = crear_boton_estilo(frame_botones, "✓ Registrar", registrar, 'success')
    btn_registrar.pack(side='left', padx=10)
    
    btn_cancelar = crear_boton_estilo(frame_botones, "← Volver", lambda: mostrar_inicio(root), 'danger')
    btn_cancelar.pack(side='left', padx=10)

def login_usuario(root):
    """Muestra el login de usuario"""
    for widget in root.winfo_children():
        widget.destroy()
        
    crear_estilo_ventana(root, "Inicio de Sesión - Usuario", "350x400")

    main_frame = crear_frame_contenedor(root, 15)
    
    titulo = crear_label_titulo(main_frame, "🚌 Acceso de Usuario", 16)
    titulo.pack(pady=(20, 30))
    titulo.config(bg='#FFFFFF')
    
    tk.Label(main_frame, text="Usuario:", font=('Arial', 10, 'bold'), 
             fg='#2C3E50', bg='#FFFFFF').pack(pady=(10, 5))
    entrada_usuario = tk.Entry(main_frame, font=('Arial', 11), width=25)
    entrada_usuario.pack(pady=(0, 10))
    entrada_usuario.focus()

    tk.Label(main_frame, text="Contraseña:", font=('Arial', 10, 'bold'), 
             fg='#2C3E50', bg='#FFFFFF').pack(pady=(10, 5))
    entrada_contraseña = tk.Entry(main_frame, font=('Arial', 11), show="*", width=25)
    entrada_contraseña.pack(pady=(0, 20))

    def autenticar(event=None):
        usuario = entrada_usuario.get().strip()
        contraseña = entrada_contraseña.get().strip()

        if not usuario or not contraseña:
            messagebox.showerror("Error", "Por favor complete todos los campos.")
            return

        usuarios = cargar_usuarios()
        if usuario in usuarios and usuarios[usuario]["contraseña"] == contraseña:
            messagebox.showinfo("¡Bienvenido!", f"¡Hola {usuarios[usuario]['nombre_completo']}!")
            # Importar dinámicamente para evitar importación circular
            from src.interfaz_usuario import iniciar_sistema_usuario
            iniciar_sistema_usuario(root, usuario) 
        else:
            messagebox.showerror("Error", "Credenciales incorrectas.")

    entrada_contraseña.bind('<Return>', autenticar)
    
    frame_botones = tk.Frame(main_frame, bg='#FFFFFF')
    frame_botones.pack(pady=20)
    
    btn_ingresar = crear_boton_estilo(frame_botones, "→ Ingresar", autenticar, 'primary')
    btn_ingresar.pack(side='left', padx=10)
    
    btn_cancelar = crear_boton_estilo(frame_botones, "← Volver", lambda: mostrar_inicio(root), 'accent')
    btn_cancelar.pack(side='left', padx=10)

def login_admin(root):
    """Muestra el login de administrador"""
    for widget in root.winfo_children():
        widget.destroy()
        
    crear_estilo_ventana(root, "Acceso de Administrador", "350x400")
    
    main_frame = crear_frame_contenedor(root, 15)
    
    titulo = crear_label_titulo(main_frame, " Panel de Administrador", 16)
    titulo.pack(pady=(20, 30))
    titulo.config(bg='#FFFFFF')
    
    tk.Label(main_frame, text="Usuario Admin:", font=('Arial', 10, 'bold'), 
             fg='#2C3E50', bg='#FFFFFF').pack(pady=(10, 5))
    entrada_usuario = tk.Entry(main_frame, font=('Arial', 11), width=25)
    entrada_usuario.pack(pady=(0, 10))
    entrada_usuario.focus()

    tk.Label(main_frame, text="Contraseña Admin:", font=('Arial', 10, 'bold'), 
             fg='#2C3E50', bg='#FFFFFF').pack(pady=(10, 5))
    entrada_contraseña = tk.Entry(main_frame, font=('Arial', 11), show="*", width=25)
    entrada_contraseña.pack(pady=(0, 20))

    def autenticar_admin(event=None):
        usuario = entrada_usuario.get().strip()
        contraseña = entrada_contraseña.get().strip()

        admins = cargar_administradores()
        if usuario in admins and admins[usuario] == contraseña:
            messagebox.showinfo("Acceso Concedido", "¡Bienvenido Administrador!")
            from src.interfaz_admin import iniciar_sistema_admin
            iniciar_sistema_admin(root, usuario) 
        else:
            messagebox.showerror("Acceso Denegado", "Credenciales incorrectas.")

    entrada_contraseña.bind('<Return>', autenticar_admin)
    
    frame_botones = tk.Frame(main_frame, bg='#FFFFFF')
    frame_botones.pack(pady=20)
    
    btn_ingresar = crear_boton_estilo(frame_botones, "🔓 Acceder", autenticar_admin, 'secondary')
    btn_ingresar.pack(side='left', padx=10)
    
    btn_cancelar = crear_boton_estilo(frame_botones, "← Volver", lambda: mostrar_inicio(root), 'accent')
    btn_cancelar.pack(side='left', padx=10)