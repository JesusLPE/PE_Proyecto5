"""
Funciones específicas del sistema de usuario
"""

import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime, timedelta
import uuid
from src.utilidades import crear_estilo_ventana, crear_frame_contenedor, crear_label_titulo, crear_boton_estilo, mostrar_info_sistema
from src.archivos import cargar_cooperativas, cargar_rutas, cargar_horarios, cargar_boletos, guardar_boletos, cargar_boletos_papelera, guardar_boletos_papelera, cargar_usuarios
from src.configuracion import CIUDADES_ECUADOR, COLORS

def mostrar_home_usuario(content_frame_usuario, usuario_actual):
    """Muestra la pantalla principal del usuario"""
    for widget in content_frame_usuario.winfo_children():
        widget.destroy()
    
    main_frame = crear_frame_contenedor(content_frame_usuario, 20)
    
    # Obtener nombre del usuario
    usuarios = cargar_usuarios()
    nombre_completo = usuarios.get(usuario_actual, {}).get("nombre_completo", "Usuario")
    
    # Título de bienvenida
    tk.Label(main_frame, text=f"¡Bienvenido, {nombre_completo}!", 
             font=('Arial', 16, 'bold'), fg=COLORS['primary'], bg=COLORS['white']).pack(pady=(10, 20))
    
    crear_label_titulo(main_frame, " Buscador Rápido de Rutas", 16).pack(pady=(20, 10))
    
    ruta_frame = tk.Frame(main_frame, bg=COLORS['white'], relief='raised', bd=2)
    ruta_frame.pack(fill='x', pady=10, padx=20)
    
    seleccion_frame = tk.Frame(ruta_frame, bg=COLORS['white'])
    seleccion_frame.pack(pady=20)
    
    tk.Label(seleccion_frame, text="🚩 Origen:", font=('Arial', 12, 'bold'), 
             fg=COLORS['text_dark'], bg=COLORS['white']).grid(row=0, column=0, padx=20, pady=10, sticky='w')
    combo_origen = ttk.Combobox(seleccion_frame, values=CIUDADES_ECUADOR, width=20, font=('Arial', 11))
    combo_origen.grid(row=0, column=1, padx=20, pady=10)
    combo_origen.set("Quito") 
    
    tk.Label(seleccion_frame, text=" Destino:", font=('Arial', 12, 'bold'), 
             fg=COLORS['text_dark'], bg=COLORS['white']).grid(row=0, column=2, padx=20, pady=10, sticky='w')
    combo_destino = ttk.Combobox(seleccion_frame, values=CIUDADES_ECUADOR, width=20, font=('Arial', 11))
    combo_destino.grid(row=0, column=3, padx=20, pady=10)
    combo_destino.set("Cuenca") 
    
    def buscar_cooperativas():
        origen = combo_origen.get()
        destino = combo_destino.get()
        
        if origen == destino:
            messagebox.showerror("Error", "Seleccione un origen y destino diferentes.")
            return
            
        mostrar_resultados_busqueda(content_frame_usuario, origen, destino, usuario_actual)
    
    btn_buscar = crear_boton_estilo(seleccion_frame, "🔍 Buscar Cooperativas", buscar_cooperativas, 'success')
    btn_buscar.grid(row=0, column=4, padx=20, pady=10)

    # Opciones rápidas - CORRECCIÓN: Usar pack en lugar de grid
    opciones_frame = tk.Frame(main_frame, bg=COLORS['white'])
    opciones_frame.pack(pady=40, fill='x', expand=True)
    
    tk.Label(opciones_frame, text="Opciones Rápidas de Boletería:", 
             font=('Arial', 14, 'bold'), fg=COLORS['primary'], bg=COLORS['white']).pack(pady=(10, 20))
    
    opciones = [
        (" Mi Historial", lambda: mostrar_historial_usuario(content_frame_usuario, usuario_actual), 'primary'), 
        (" Buscar por Horario", lambda: mostrar_buscar_horario(content_frame_usuario, usuario_actual), 'secondary'),
        (" Información", mostrar_info_sistema, 'accent'), 
        (" Salir", lambda: cerrar_sesion_usuario(content_frame_usuario), 'danger')
    ]
    
    # CORRECCIÓN: Usar un frame interno para los botones
    botones_frame = tk.Frame(opciones_frame, bg=COLORS['white'])
    botones_frame.pack()
    
    for i, (text, command, color) in enumerate(opciones):
        btn = crear_boton_estilo(botones_frame, text, command, color, 18)
        btn.pack(side='left', padx=15, pady=10)

def cerrar_sesion_usuario(content_frame_usuario):
    """Cierra la sesión del usuario y vuelve al inicio - VERSIÓN SIMPLIFICADA"""
    try:
        # Obtener la ventana principal
        root = content_frame_usuario.winfo_toplevel()
        
        # Importar aquí para evitar problemas de importación circular
        import tkinter as tk
        from tkinter import messagebox
        
        # Preguntar confirmación
        if messagebox.askyesno("Cerrar Sesión", "¿Está seguro que desea salir?"):
            # Destruir todos los widgets
            for widget in root.winfo_children():
                widget.destroy()
            
            # Ahora importar mostrar_inicio (después de limpiar)
            from src.autenticacion import mostrar_inicio
            
            # Mostrar pantalla de inicio
            mostrar_inicio(root)
            root.geometry("600x450")
            
    except Exception as e:
        print(f"Error al cerrar sesión: {e}")
        # Si hay error, simplemente mostrar mensaje y salir
        import tkinter as tk
        from tkinter import messagebox
        messagebox.showinfo("Sesión cerrada", "Ha salido del sistema de usuario.")

def mostrar_resultados_busqueda(content_frame_usuario, origen, destino, usuario_actual):
    """Muestra los resultados de búsqueda de cooperativas"""
    for widget in content_frame_usuario.winfo_children():
        widget.destroy()
    
    main_frame = crear_frame_contenedor(content_frame_usuario, 20)
    
    titulo = crear_label_titulo(main_frame, f" Cooperativas Disponibles: {origen} → {destino}", 16)
    titulo.pack(pady=(20, 30))
    titulo.config(bg=COLORS['white'])
    
    cooperativas = cargar_cooperativas()
    rutas = cargar_rutas()
    
    cooperativas_disponibles = []
    for coop_id, coop_data in cooperativas.items():
        for ruta_id, ruta_data in rutas.items():
            if (ruta_data['origen'] == origen and ruta_data['destino'] == destino and 
                ruta_data['cooperativa_id'] == coop_id):
                cooperativas_disponibles.append({
                    'coop_id': coop_id,
                    'coop_data': coop_data,
                    'ruta_data': ruta_data,
                    'ruta_id': ruta_id
                })
    
    if not cooperativas_disponibles:
        tk.Label(main_frame, text=" No hay cooperativas disponibles para esta ruta", 
                 font=('Arial', 14), fg=COLORS['danger'], bg=COLORS['white']).pack(pady=50)
        
        btn_volver = crear_boton_estilo(main_frame, "← Volver", 
                                       lambda: mostrar_home_usuario(content_frame_usuario, usuario_actual), 'primary')
        btn_volver.pack(pady=20)
        return
    
    # Frame con scrollbar
    scroll_frame = tk.Frame(main_frame, bg=COLORS['white'])
    scroll_frame.pack(fill='both', expand=True, padx=20)
    
    canvas = tk.Canvas(scroll_frame, bg=COLORS['white'])
    scrollbar = tk.Scrollbar(scroll_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg=COLORS['white'])
    
    def on_frame_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    scrollable_frame.bind("<Configure>", on_frame_configure)
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    for i, coop_info in enumerate(cooperativas_disponibles):
        coop_data = coop_info['coop_data']
        ruta_data = coop_info['ruta_data']
        ruta_id = coop_info['ruta_id']
        
        card_frame = tk.Frame(scrollable_frame, bg='#f8f9fa', relief='solid', bd=1)
        card_frame.pack(fill='x', padx=10, pady=10)
        
        header_card = tk.Frame(card_frame, bg=COLORS['primary'])
        header_card.pack(fill='x')
        
        tk.Label(header_card, text=f" {coop_data['nombre']}", 
                 font=('Arial', 14, 'bold'), fg='white', bg=COLORS['primary']).pack(pady=10)
        
        info_card = tk.Frame(card_frame, bg='#f8f9fa')
        info_card.pack(fill='x', padx=20, pady=15)
        
        info_text = f"📍 Ruta: {ruta_data['origen']} → {ruta_data['destino']}\n💰 Precio: ${ruta_data['precio']:.2f}\n🚌 Buses disponibles: {coop_data['numero_buses']}\n📞 Teléfono: {coop_data['telefono']}"
        
        tk.Label(info_card, text=info_text, font=('Arial', 11), 
                 fg=COLORS['text_dark'], bg='#f8f9fa', justify='left').pack(side='left')
        
        def seleccionar_horarios(cid=coop_info['coop_id'], rid=ruta_id):
            mostrar_horarios(content_frame_usuario, cid, rid, usuario_actual)
        
        btn_seleccionar = crear_boton_estilo(info_card, "Seleccionar →", seleccionar_horarios, 'success')
        btn_seleccionar.pack(side='right', padx=20)
    
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    btn_volver = crear_boton_estilo(main_frame, "← Volver al Inicio", 
                                   lambda: mostrar_home_usuario(content_frame_usuario, usuario_actual), 'accent')
    btn_volver.pack(pady=20)

def mostrar_horarios(content_frame_usuario, coop_id, ruta_id, usuario_actual):
    """Muestra los horarios disponibles para una ruta"""
    for widget in content_frame_usuario.winfo_children():
        widget.destroy()
    
    main_frame = crear_frame_contenedor(content_frame_usuario, 20)
    
    cooperativas = cargar_cooperativas()
    rutas = cargar_rutas()
    horarios = cargar_horarios()
    
    coop_data = cooperativas.get(coop_id, {})
    ruta_data = rutas.get(ruta_id, {})
    
    titulo = crear_label_titulo(main_frame, f" Horarios - {coop_data.get('nombre', 'N/A')}", 16)
    titulo.pack(pady=(20, 30))
    titulo.config(bg=COLORS['white'])
    
    # Información de la ruta
    info_frame = tk.Frame(main_frame, bg=COLORS['background'], relief='sunken', bd=2)
    info_frame.pack(fill='x', padx=20, pady=10)
    
    info_text = f"📍 {ruta_data.get('origen', 'N/A')} → {ruta_data.get('destino', 'N/A')} | 💰 ${ruta_data.get('precio', 0.0):.2f}"
    tk.Label(info_frame, text=info_text, font=('Arial', 12, 'bold'), 
             fg=COLORS['text_dark'], bg=COLORS['background']).pack(pady=15)
    
    # Horarios disponibles
    horarios_frame = tk.Frame(main_frame, bg=COLORS['white'])
    horarios_frame.pack(fill='both', expand=True, padx=20, pady=20)
    
    tk.Label(horarios_frame, text=" Horarios Disponibles (Día de Mañana):", 
             font=('Arial', 14, 'bold'), fg=COLORS['text_dark'], bg=COLORS['white']).pack(pady=10)
    
    horarios_ruta = [(hid, hdata) for hid, hdata in horarios.items() if hdata.get('ruta_id') == ruta_id]
    
    if not horarios_ruta:
        tk.Label(horarios_frame, text=" No hay horarios configurados para esta ruta", 
                 font=('Arial', 12), fg=COLORS['danger'], bg=COLORS['white']).pack(pady=30)
    else:
        grid_frame = tk.Frame(horarios_frame, bg=COLORS['white'])
        grid_frame.pack(pady=20)
        
        for i, (horario_id, horario_data) in enumerate(horarios_ruta):
            hora = horario_data['hora']
            
            def seleccionar_asientos(cid=coop_id, rid=ruta_id, hid=horario_id):
                mostrar_asientos(content_frame_usuario, cid, rid, hid, usuario_actual)
            
            btn_horario = tk.Button(
                grid_frame,
                text=f" {hora}\nVer Asientos",
                font=('Arial', 11, 'bold'),
                bg=COLORS['success'],
                fg='white',
                width=12,
                height=3,
                relief='raised',
                bd=2,
                cursor='hand2',
                command=seleccionar_asientos
            )
            btn_horario.grid(row=i//4, column=i%4, padx=10, pady=10)
    
    # Botón para volver
    btn_volver = crear_boton_estilo(main_frame, "← Volver a Cooperativas", 
                                   lambda: mostrar_resultados_busqueda(
                                       content_frame_usuario, 
                                       ruta_data.get('origen', 'N/A'), 
                                       ruta_data.get('destino', 'N/A'),
                                       usuario_actual
                                   ), 'accent')
    btn_volver.pack(pady=20)

def mostrar_asientos(content_frame_usuario, coop_id, ruta_id, horario_id, usuario_actual):
    """Muestra la selección de asientos"""
    for widget in content_frame_usuario.winfo_children():
        widget.destroy()
    
    # Obtener la variable global CORRECTAMENTE
    from main import get_asiento_seleccionado_var
    asiento_seleccionado_var = get_asiento_seleccionado_var()
    
    if asiento_seleccionado_var is None:
        # Si por alguna razón es None, crear una nueva
        import tkinter as tk
        asiento_seleccionado_var = tk.StringVar()
        asiento_seleccionado_var.set("Ninguno")
    
    # Inicializar diccionario de asientos
    asiento_botones = {}
    
    # Crear layout principal
    wrapper = crear_frame_contenedor(content_frame_usuario, 16)
    wrapper.grid_columnconfigure(0, weight=3)
    wrapper.grid_columnconfigure(1, weight=1)
    wrapper.grid_rowconfigure(0, weight=1)

    main_left = tk.Frame(wrapper, bg=COLORS['white'])
    main_left.grid(row=0, column=0, sticky="nsew", padx=(10, 5), pady=10)

    sidebar = tk.Frame(wrapper, bg=COLORS['white'])
    sidebar.grid(row=0, column=1, sticky="ns", padx=(5, 10), pady=10)

    # Cargar datos necesarios
    cooperativas = cargar_cooperativas()
    rutas = cargar_rutas()
    horarios = cargar_horarios()
    boletos = cargar_boletos()

    coop_data = cooperativas.get(coop_id, {})
    ruta_data = rutas.get(ruta_id, {})
    horario_data = horarios.get(horario_id, {})
    
    # Fecha de viaje (mañana)
    fecha_viaje = datetime.now() + timedelta(days=1)
    fecha_str = fecha_viaje.strftime('%Y-%m-%d')
    precio_base = ruta_data.get('precio', 0.0)

    # Título
    titulo = crear_label_titulo(main_left, f"🪑 Seleccionar Asiento - {coop_data.get('nombre', 'N/A')}", 16)
    titulo.pack(pady=(15, 10))
    titulo.config(bg=COLORS['white'])

    # Información del viaje
    info_frame = tk.Frame(main_left, bg=COLORS['background'], relief='sunken', bd=1)
    info_frame.pack(fill='x', padx=10)
    
    info_text = f" {ruta_data.get('origen', 'N/A')} → {ruta_data.get('destino', 'N/A')} |  {horario_data.get('hora', 'N/A')} |  Fecha de Viaje: {fecha_str} |  Precio: ${precio_base:.2f}"
    tk.Label(info_frame, text=info_text, font=('Arial', 11, 'bold'),
             fg=COLORS['text_dark'], bg=COLORS['background'], justify='center').pack(pady=10)

    # Filtrar asientos vendidos
    boletos_vendidos = [
        b.get('asiento') for b in boletos
        if b.get('ruta_id') == ruta_id and
           b.get('horario_id') == horario_id and
           b.get('fecha_viaje') == fecha_str
    ]
    asientos_vendidos = set(boletos_vendidos)

    # Layout del bus
    bus_frame = tk.LabelFrame(main_left, text="Layout del Bus (40 Asientos)", bg=COLORS['white'],
                              font=('Arial', 12, 'bold'), fg=COLORS['text_dark'])
    bus_frame.pack(pady=20, padx=20, fill='both', expand=True)

    asientos_container = tk.Frame(bus_frame, bg=COLORS['white'], padx=20, pady=20)
    asientos_container.pack(expand=True)

    # Icono de volante y pasillo
    tk.Label(asientos_container, text="Volante ", font=('Arial', 10), bg=COLORS['text_light'], fg='white', width=6).grid(row=0, column=0, padx=5, pady=5, sticky='w')
    tk.Label(asientos_container, text="Pasillo", font=('Arial', 8), bg=COLORS['white'], fg=COLORS['text_light']).grid(row=0, column=2, padx=5, pady=5)

    # Función para seleccionar asiento
    def seleccionar_asiento(asiento):
        info = asiento_botones[asiento]
        
        if info['estado'] == 'sold':
            messagebox.showerror("Asiento Ocupado", f"El asiento A{asiento} ya está vendido.")
            return

        asiento_actual = asiento_seleccionado_var.get()
        
        if asiento_actual == asiento:
            # Deseleccionar
            asiento_seleccionado_var.set("Ninguno")
            info['btn'].config(bg=COLORS['available'])
            btn_comprar.config(state=tk.DISABLED)
            info['estado'] = 'available'
        else:
            # Deseleccionar anterior si hay uno
            if asiento_actual != "Ninguno" and asiento_actual in asiento_botones:
                try:
                    prev_info = asiento_botones[asiento_actual]
                    prev_info['btn'].config(bg=COLORS['available'])
                    prev_info['estado'] = 'available'
                except KeyError:
                    pass

            # Seleccionar nuevo
            asiento_seleccionado_var.set(asiento)
            info['btn'].config(bg=COLORS['selected'])
            btn_comprar.config(state=tk.NORMAL)
            info['estado'] = 'selected'

    # Crear botones de asientos (4x10 = 40 asientos)
    for i in range(1, 41):
        asiento_id = str(i)
        row = (i - 1) // 4 + 1
        col_index = (i - 1) % 4
        
        if col_index >= 2:
            col = col_index + 1  # Saltar columna del pasillo
        else:
            col = col_index

        estado = 'sold' if asiento_id in asientos_vendidos else 'available'
        
        btn = tk.Button(
            asientos_container,
            text=f"A{asiento_id}",
            bg=COLORS[estado],
            fg='white',
            font=('Arial', 10, 'bold'),
            width=4, height=2, relief='raised',
            bd=2, cursor='hand2',
            command=lambda asiento=asiento_id: seleccionar_asiento(asiento)
        )
        btn.grid(row=row, column=col, padx=5, pady=5)
        asiento_botones[asiento_id] = {'btn': btn, 'estado': estado}

    # Leyenda de colores
    legend_frame = tk.Frame(main_left, bg=COLORS['white'])
    legend_frame.pack(pady=10)
    
    tk.Label(legend_frame, text="Leyenda:", font=('Arial', 10, 'bold'), bg=COLORS['white']).pack(side='left', padx=10)
    tk.Label(legend_frame, text="Disponible", bg=COLORS['available'], fg='white', width=10).pack(side='left', padx=5)
    tk.Label(legend_frame, text="Vendido", bg=COLORS['sold'], fg='white', width=10).pack(side='left', padx=5)
    tk.Label(legend_frame, text="Seleccionado", bg=COLORS['selected'], fg='white', width=10).pack(side='left', padx=5)

    # --- SIDEBAR: Resumen de compra ---
    tk.Label(sidebar, text="🛒 Resumen de Compra", font=('Arial', 14, 'bold'),
             fg=COLORS['secondary'], bg=COLORS['white']).pack(pady=(20, 10), padx=10)

    # Asiento seleccionado
    tk.Label(sidebar, text="Asiento:", font=('Arial', 11, 'bold'), bg=COLORS['white']).pack(anchor='w', padx=10, pady=(10, 0))
    lbl_asiento = tk.Label(sidebar, textvariable=asiento_seleccionado_var, font=('Arial', 12), bg=COLORS['white'], fg=COLORS['primary'])
    lbl_asiento.pack(anchor='w', padx=10)
    
    # Precio
    tk.Label(sidebar, text="Precio Total:", font=('Arial', 11, 'bold'), bg=COLORS['white']).pack(anchor='w', padx=10, pady=(10, 0))
    lbl_precio = tk.Label(sidebar, text=f"${precio_base:.2f}", font=('Arial', 16, 'bold'), bg=COLORS['white'], fg=COLORS['success'])
    lbl_precio.pack(anchor='w', padx=10)

    # Función para comprar boleto
    def comprar_boleto():
        asiento = asiento_seleccionado_var.get()
        if asiento == "Ninguno":
            messagebox.showerror("Error", "Debe seleccionar un asiento antes de comprar.")
            return

        if not messagebox.askyesno("Confirmar Compra", f"¿Confirma la compra del asiento A{asiento} por ${precio_base:.2f}?"):
            return
        
        # Crear nuevo boleto
        boletos = cargar_boletos()
        nuevo_boleto = {
            'id': str(uuid.uuid4()),
            'usuario': usuario_actual,
            'cooperativa_id': coop_id,
            'ruta_id': ruta_id,
            'horario_id': horario_id,
            'fecha_viaje': fecha_str,
            'asiento': asiento,
            'precio': precio_base,
            'fecha_compra': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        boletos.append(nuevo_boleto)
        guardar_boletos(boletos)
        
        messagebox.showinfo("Compra Exitosa", f"¡Boleto A{asiento} comprado con éxito!\nID de Boleto: {nuevo_boleto['id']}\nGuarde este ID.")
        
        # Recargar la pantalla de asientos
        mostrar_asientos(content_frame_usuario, coop_id, ruta_id, horario_id, usuario_actual)

    # Botón de comprar
    btn_comprar = crear_boton_estilo(sidebar, "💳 Comprar Boleto", comprar_boleto, 'success', width=20)
    btn_comprar.pack(pady=30, padx=10)
    
    # Verificar estado inicial del botón de comprar
    if asiento_seleccionado_var.get() == "Ninguno":
        btn_comprar.config(state=tk.DISABLED)
    else:
        btn_comprar.config(state=tk.NORMAL)

    def volver_a_horarios():
        mostrar_horarios(content_frame_usuario, coop_id, ruta_id, usuario_actual)
    
    btn_volver = crear_boton_estilo(sidebar, "← Volver a Horarios", volver_a_horarios, 'accent', width=20)
    btn_volver.pack(pady=10, padx=10)
    
    # Asegurar que la variable se actualice cuando se seleccione un asiento
    def actualizar_estado_boton(*args):
        if asiento_seleccionado_var.get() == "Ninguno":
            btn_comprar.config(state=tk.DISABLED)
        else:
            btn_comprar.config(state=tk.NORMAL)
    
    asiento_seleccionado_var.trace('w', actualizar_estado_boton)

def mostrar_historial_usuario(content_frame_usuario, usuario_actual):
    """Muestra el historial de compras del usuario"""
    for widget in content_frame_usuario.winfo_children():
        widget.destroy()
    
    main_frame = crear_frame_contenedor(content_frame_usuario, 20)
    
    titulo = crear_label_titulo(main_frame, " Mi Historial de Boletos", 16)
    titulo.pack(pady=(20, 30))
    titulo.config(bg=COLORS['white'])
    
    notebook = ttk.Notebook(main_frame)
    notebook.pack(fill='both', expand=True, padx=20, pady=10)
    
    tab_historial = tk.Frame(notebook, bg=COLORS['white'])
    notebook.add(tab_historial, text="Historial Activo")
    
    tab_papelera = tk.Frame(notebook, bg=COLORS['white'])
    notebook.add(tab_papelera, text="Papelera")
    
    # Cargar datos
    boletos = cargar_boletos()
    rutas = cargar_rutas()
    cooperativas = cargar_cooperativas()
    horarios = cargar_horarios()
    
    # Historial Activo
    mis_boletos = [b for b in boletos if b.get('usuario') == usuario_actual]
    mis_boletos.sort(key=lambda x: x.get('fecha_compra', '0000-01-01'), reverse=True)
    
    if not mis_boletos:
        tk.Label(tab_historial, text="No has comprado boletos activos.", 
                 font=('Arial', 12), fg=COLORS['text_light'], bg=COLORS['white']).pack(pady=50)
    else:
        crear_tabla_historial(tab_historial, mis_boletos, rutas, cooperativas, horarios, es_papelera=False,
                             content_frame_usuario=content_frame_usuario, usuario_actual=usuario_actual)
    
    # Papelera
    boletos_papelera = cargar_boletos_papelera()
    mis_boletos_papelera = [b for b in boletos_papelera if b.get('usuario') == usuario_actual]
    mis_boletos_papelera.sort(key=lambda x: x.get('fecha_compra', '0000-01-01'), reverse=True)
    
    if not mis_boletos_papelera:
        tk.Label(tab_papelera, text="La papelera está vacía.", 
                 font=('Arial', 12), fg=COLORS['text_light'], bg=COLORS['white']).pack(pady=50)
    else:
        crear_tabla_historial(tab_papelera, mis_boletos_papelera, rutas, cooperativas, horarios, es_papelera=True,
                             content_frame_usuario=content_frame_usuario, usuario_actual=usuario_actual)
    
    btn_volver = crear_boton_estilo(main_frame, "← Volver al Inicio", 
                                   lambda: mostrar_home_usuario(content_frame_usuario, usuario_actual), 'accent')
    btn_volver.pack(pady=20)

def crear_tabla_historial(parent, boletos_lista, rutas, cooperativas, horarios, es_papelera=False,
                         content_frame_usuario=None, usuario_actual=None):
    """Crea una tabla con el historial de boletos"""
    scroll_frame = tk.Frame(parent, bg=COLORS['white'])
    scroll_frame.pack(fill='both', expand=True, padx=20)
    
    canvas = tk.Canvas(scroll_frame, bg=COLORS['white'])
    scrollbar = tk.Scrollbar(scroll_frame, orient="vertical", command=canvas.yview)
    scrollable_inner_frame = tk.Frame(canvas, bg=COLORS['white'])
    
    def on_frame_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))
    
    scrollable_inner_frame.bind("<Configure>", on_frame_configure)
    canvas.create_window((0, 0), window=scrollable_inner_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    # Cabecera de la tabla
    header_frame = tk.Frame(scrollable_inner_frame, bg=COLORS['primary'])
    header_frame.pack(fill='x', pady=(0, 5), padx=5)
    
    headers = [("ID Boleto", 10), ("Ruta", 25), ("Fecha/Hora", 20), ("Asiento", 10), ("Precio", 10), ("Acción", 15)]
    
    for col, (text, rel_width) in enumerate(headers):
        tk.Label(header_frame, text=text, font=('Arial', 10, 'bold'), 
                 fg='white', bg=COLORS['primary'], width=rel_width).grid(row=0, column=col, sticky='nsew', padx=1, pady=5)
    
    # Funciones para eliminar/recuperar boletos
    def eliminar_boleto(boleto):
        if not messagebox.askyesno("Confirmar Eliminación", f"¿Mover el boleto {boleto['id'][:8]}... a la papelera?"):
            return
        
        boletos = cargar_boletos()
        boletos.remove(boleto)
        guardar_boletos(boletos)
        
        boletos_papelera = cargar_boletos_papelera()
        boletos_papelera.append(boleto)
        guardar_boletos_papelera(boletos_papelera)
        
        messagebox.showinfo("Éxito", "Boleto movido a la papelera.")
        mostrar_historial_usuario(content_frame_usuario, usuario_actual)
    
    def recuperar_boleto(boleto):
        if not messagebox.askyesno("Confirmar Recuperación", f"¿Recuperar el boleto {boleto['id'][:8]}... al historial?"):
            return
        
        boletos_papelera = cargar_boletos_papelera()
        boletos_papelera.remove(boleto)
        guardar_boletos_papelera(boletos_papelera)
        
        boletos = cargar_boletos()
        boletos.append(boleto)
        guardar_boletos(boletos)
        
        messagebox.showinfo("Éxito", "Boleto recuperado al historial.")
        mostrar_historial_usuario(content_frame_usuario, usuario_actual)
    
    # Agregar cada boleto a la tabla
    for i, boleto in enumerate(boletos_lista):
        ruta_data = rutas.get(boleto.get('ruta_id', ''), {})
        coop_data = cooperativas.get(boleto.get('cooperativa_id', ''), {})
        horario_data = horarios.get(boleto.get('horario_id', ''), {})
        
        ruta_info = f"{ruta_data.get('origen', 'N/A')} → {ruta_data.get('destino', 'N/A')}\n({coop_data.get('nombre', 'N/A')})"
        fecha_hora_info = f"{boleto.get('fecha_viaje', 'N/A')} @ {horario_data.get('hora', 'N/A')}"
        
        item_frame = tk.Frame(scrollable_inner_frame, bg='#f8f8f8' if i % 2 == 0 else COLORS['white'], 
                             relief='groove', bd=1)
        item_frame.pack(fill='x', padx=5, pady=2)
        
        data = [
            (boleto['id'][:8] + '...', 10),
            (ruta_info, 25),
            (fecha_hora_info, 20),
            (f"A{boleto['asiento']}", 10),
            (f"${boleto['precio']:.2f}", 10)
        ]
        
        for col, (text, rel_width) in enumerate(data):
            tk.Label(item_frame, text=text, font=('Arial', 10), fg=COLORS['text_dark'], 
                    bg=item_frame['bg'], width=rel_width, justify='left', anchor='w').grid(
                    row=0, column=col, sticky='nsew', padx=5, pady=5)
        
        # Botón de acción
        if es_papelera:
            btn_accion = crear_boton_estilo(item_frame, "Recuperar", 
                                           lambda b=boleto: recuperar_boleto(b), 'success', 10)
        else:
            btn_accion = crear_boton_estilo(item_frame, "Eliminar", 
                                           lambda b=boleto: eliminar_boleto(b), 'danger', 10)
        btn_accion.grid(row=0, column=5, padx=5, pady=5)
    
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

def mostrar_buscar_horario(content_frame_usuario, usuario_actual):
    """Muestra la búsqueda de rutas por horario"""
    for widget in content_frame_usuario.winfo_children():
        widget.destroy()
    
    main_frame = crear_frame_contenedor(content_frame_usuario, 20)
    
    titulo = crear_label_titulo(main_frame, " Buscar Rutas por Horario", 16)
    titulo.pack(pady=(20, 30))
    titulo.config(bg=COLORS['white'])

    # Fecha fija de viaje (mañana)
    fecha_viaje_str = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
    tk.Label(main_frame, text=f" Fecha Fija de Viaje: {(datetime.now() + timedelta(days=1)).strftime('%d/%m/%Y')} (Mañana)", 
             font=('Arial', 12, 'italic'), bg=COLORS['white'], fg=COLORS['text_light']).pack(pady=10)
    
    # Filtro por rango de hora
    tk.Label(main_frame, text="Filtrar por Rango de Hora (Opcional):", 
             font=('Arial', 12), bg=COLORS['white'], fg=COLORS['text_dark']).pack(pady=(20, 5))
    
    horas_disponibles = ["Cualquier Hora", "00:00-06:00 (Madrugada)", "06:00-12:00 (Mañana)", 
                        "12:00-18:00 (Tarde)", "18:00-23:59 (Noche)"]
    combo_hora = ttk.Combobox(main_frame, values=horas_disponibles, width=30, 
                             font=('Arial', 11), state="readonly")
    combo_hora.set("Cualquier Hora")
    combo_hora.pack(pady=(0, 20))
    
    # Frame para resultados con scrollbar
    resultados_container = tk.Frame(main_frame, bg=COLORS['white'])
    resultados_container.pack(fill='both', expand=True, padx=20, pady=20)
    
    # Crear canvas y scrollbar para resultados
    canvas = tk.Canvas(resultados_container, bg=COLORS['white'], highlightthickness=0)
    scrollbar = tk.Scrollbar(resultados_container, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg=COLORS['white'])
    
    def on_frame_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))
    
    scrollable_frame.bind("<Configure>", on_frame_configure)
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    def mostrar_todas_las_rutas():
        # Limpiar resultados anteriores
        for widget in scrollable_frame.winfo_children():
            widget.destroy()
        
        filtro_hora_str = combo_hora.get()
        
        rutas = cargar_rutas()
        horarios = cargar_horarios()
        cooperativas = cargar_cooperativas()
        
        rutas_con_horarios = {}
        
        # Filtrar rutas por horario
        for hid, hdata in horarios.items():
            ruta_id = hdata['ruta_id']
            
            if ruta_id in rutas:
                hora_salida = hdata['hora']
                
                # Verificar si coincide con el filtro
                hora_match = True
                if filtro_hora_str != "Cualquier Hora":
                    rango_part = filtro_hora_str.split('(')[0].strip()
                    try:
                        h_inicio_str, h_fin_str = rango_part.split('-')
                        
                        h_salida = datetime.strptime(hora_salida, '%H:%M').time()
                        h_inicio = datetime.strptime(h_inicio_str, '%H:%M').time()
                        h_fin = datetime.strptime(h_fin_str, '%H:%M').time()
                        
                        if not (h_salida >= h_inicio and h_salida <= h_fin):
                            hora_match = False
                    except ValueError:
                        pass

                if hora_match:
                    ruta_data = rutas[ruta_id]
                    coop_data = cooperativas.get(ruta_data['cooperativa_id'], {'nombre': 'N/A'})
                    
                    if ruta_id not in rutas_con_horarios:
                        rutas_con_horarios[ruta_id] = {
                            'ruta': ruta_data,
                            'cooperativa': coop_data,
                            'horarios': []
                        }
                    if hora_salida not in rutas_con_horarios[ruta_id]['horarios']:
                        rutas_con_horarios[ruta_id]['horarios'].append(hora_salida)

        if not rutas_con_horarios:
            tk.Label(scrollable_frame, text="❌ No hay rutas disponibles para el filtro seleccionado.", 
                     font=('Arial', 12), fg=COLORS['danger'], bg=COLORS['white']).pack(pady=50)
            return

        # Mostrar resultados
        tk.Label(scrollable_frame, text=f"Resultados de Búsqueda ({len(rutas_con_horarios)} rutas encontradas):", 
                 font=('Arial', 13, 'bold'), fg=COLORS['primary'], bg=COLORS['white']).pack(pady=(10, 15))

        for i, (ruta_id, info) in enumerate(rutas_con_horarios.items()):
            ruta = info['ruta']
            coop = info['cooperativa']
            horarios_str = ", ".join(sorted(info['horarios']))
            
            card_frame = tk.Frame(scrollable_frame, bg='#f8f9fa', relief='solid', bd=1)
            card_frame.pack(fill='x', padx=10, pady=5)

            info_text = f"🚌 Coop: {coop['nombre']}\n Ruta: {ruta['origen']} → {ruta['destino']}\n Precio: ${ruta['precio']:.2f}\n Horas: {horarios_str}"
            
            tk.Label(card_frame, text=info_text, font=('Arial', 10), 
                     fg=COLORS['text_dark'], bg='#f8f9fa', justify='left').pack(side='left', padx=15, pady=10)

            # Botón para seleccionar ruta
            def seleccionar_ruta(o=ruta['origen'], d=ruta['destino']):
                mostrar_resultados_busqueda(content_frame_usuario, o, d, usuario_actual)
            
            btn_seleccionar = crear_boton_estilo(card_frame, "Seleccionar Horario →", 
                                               seleccionar_ruta, 'secondary', width=18)
            btn_seleccionar.pack(side='right', padx=15)
    
    # Botón para mostrar resultados
    btn_mostrar = crear_boton_estilo(main_frame, "🔍 Mostrar Rutas Disponibles", 
                                     mostrar_todas_las_rutas, 'primary')
    btn_mostrar.pack(pady=10)
    
    # Empaquetar canvas y scrollbar
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    # Mostrar resultados iniciales
    mostrar_todas_las_rutas()

    # Botón para volver
    btn_volver = crear_boton_estilo(main_frame, "← Volver al Inicio", 
                                   lambda: mostrar_home_usuario(content_frame_usuario, usuario_actual), 'accent')
    btn_volver.pack(pady=20)
    
    # Agregar funcionalidad de scroll con rueda del mouse
    def _on_mousewheel(event):
        if canvas.winfo_exists():
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    canvas.bind_all("<MouseWheel>", _on_mousewheel)