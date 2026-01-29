"""
Funciones específicas del sistema de usuario
"""

import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime, timedelta
import uuid
from src.utilidades import crear_estilo_ventana, crear_frame_contenedor, crear_label_titulo, crear_boton_estilo, mostrar_info_sistema, crear_scrollable_frame
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
    
    tk.Label(seleccion_frame, text=" Origen:", font=('Arial', 12, 'bold'), 
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

def mostrar_resultados_busqueda(content_frame_usuario, origen, destino, usuario_actual, sort_by="default"):
    """Muestra los resultados de búsqueda de cooperativas.
    - Recomendaciones (más barata / más rápida / más larga) en la MISMA pantalla.
    - Ranking por Precio/Duración/Distancia en la MISMA pantalla (sin ventanas duplicadas).
    """
    # Limpiar contenedor
    for widget in content_frame_usuario.winfo_children():
        widget.destroy()

    main_frame = crear_frame_contenedor(content_frame_usuario, 20)

    titulo = crear_label_titulo(main_frame, f"Cooperativas Disponibles: {origen} → {destino}", 16)
    titulo.pack(pady=(20, 10))
    titulo.config(bg=COLORS['white'])

    cooperativas = cargar_cooperativas()
    rutas = cargar_rutas()

    def _to_float(v):
        try:
            return float(v)
        except (TypeError, ValueError):
            return None

    # ---- Recolectar rutas por cooperativa (para el trayecto origen->destino) ----
    coop_rutas = {}  # coop_id -> list[(ruta_id, ruta_data)]
    for ruta_id, ruta_data in rutas.items():
        if str(ruta_data.get('origen')) != str(origen):
            continue
        if str(ruta_data.get('destino')) != str(destino):
            continue
        if str(ruta_data.get('estado', 'Activa')).lower() not in ('activa', 'activo', 'true', '1'):
            continue

        coop_id = str(ruta_data.get('cooperativa_id', ''))
        if not coop_id or coop_id not in cooperativas:
            continue

        coop_rutas.setdefault(coop_id, []).append((ruta_id, ruta_data))

    if not coop_rutas:
        tk.Label(
            main_frame,
            text="No hay cooperativas disponibles para esta ruta",
            font=('Arial', 14),
            fg=COLORS['danger'],
            bg=COLORS['white']
        ).pack(pady=50)

        btn_volver = crear_boton_estilo(
            main_frame,
            "← Volver",
            lambda: mostrar_home_usuario(content_frame_usuario, usuario_actual),
            'primary'
        )
        btn_volver.pack(pady=20)
        return

    # ---- Elegir UNA ruta por cooperativa (por defecto: la más barata de esa cooperativa) ----
    def _pick_ruta_por_coop(coop_id, criterio="precio"):
        lst = coop_rutas.get(coop_id, [])
        if not lst:
            return None

        if criterio == "precio":
            key = lambda t: _to_float(t[1].get('precio')) if _to_float(t[1].get('precio')) is not None else float('inf')
            return min(lst, key=key)
        if criterio == "duracion":
            key = lambda t: _to_float(t[1].get('duracion_horas')) if _to_float(t[1].get('duracion_horas')) is not None else float('inf')
            return min(lst, key=key)
        if criterio == "distancia":
            key = lambda t: _to_float(t[1].get('distancia_km')) if _to_float(t[1].get('distancia_km')) is not None else float('-inf')
            return max(lst, key=key)

        # default
        return lst[0]

    def _build_items(criterio="precio"):
        items = []
        for coop_id in coop_rutas.keys():
            picked = _pick_ruta_por_coop(coop_id, criterio)
            if not picked:
                continue
            ruta_id, ruta_data = picked
            items.append({
                "coop_id": coop_id,
                "coop_data": cooperativas.get(coop_id, {}),
                "ruta_id": ruta_id,
                "ruta_data": ruta_data
            })
        return items

    base_items = _build_items("precio")  # uno por cooperativa

    # contador de cooperativas únicas
    topbar = tk.Frame(main_frame, bg=COLORS['white'])
    topbar.pack(fill='x', padx=20, pady=(0, 10))

    tk.Label(
        topbar,
        text=f"Resultados: {len(base_items)} cooperativa(s)",
        font=('Arial', 10, 'bold'),
        fg=COLORS['text_light'],
        bg=COLORS['white']
    ).pack(side='left')

    # ---- Vistas: recomendaciones y ranking (misma pantalla) ----
    view_reco = tk.Frame(main_frame, bg=COLORS['white'])
    view_rank = tk.Frame(main_frame, bg=COLORS['white'])

    view_reco.pack(fill='both', expand=True)
    view_rank.pack_forget()

    def _clear(frame):
        for w in frame.winfo_children():
            w.destroy()

    # ---- Selección de recomendaciones con reglas ----
    def _precio(item):
        v = _to_float(item["ruta_data"].get("precio"))
        return v if v is not None else float("inf")

    def _duracion(item):
        v = _to_float(item["ruta_data"].get("duracion_horas"))
        return v if v is not None else float("inf")

    def _distancia(item):
        v = _to_float(item["ruta_data"].get("distancia_km"))
        return v if v is not None else float("-inf")

    # Más barata
    mas_barata = min(base_items, key=_precio)

    # Más rápida (DEBE ser diferente a la más barata si existe alternativa)
    candidatos_rapida = [x for x in base_items if x["coop_id"] != mas_barata["coop_id"]]
    if candidatos_rapida:
        mas_rapida = min(candidatos_rapida, key=_duracion)
    else:
        # si solo hay 1 cooperativa, caerá aquí
        mas_rapida = mas_barata

    # Más larga: distancia máxima PERO distancia distinta a la más barata (y preferible otra cooperativa)
    dist_barata = _to_float(mas_barata["ruta_data"].get("distancia_km"))

    candidatos_larga = [x for x in base_items if _to_float(x["ruta_data"].get("distancia_km")) is not None]
    # 1) intenta otra cooperativa y distancia distinta
    cand1 = [x for x in candidatos_larga if x["coop_id"] != mas_barata["coop_id"] and _to_float(x["ruta_data"].get("distancia_km")) != dist_barata]
    # 2) si no hay, permite misma coop pero distancia distinta
    cand2 = [x for x in candidatos_larga if _to_float(x["ruta_data"].get("distancia_km")) != dist_barata]

    if cand1:
        mas_larga = max(cand1, key=_distancia)
    elif cand2:
        mas_larga = max(cand2, key=_distancia)
    else:
        mas_larga = None  # no hay alternativa con distancia diferente

    # Si "más rápida" resultó igual a "más barata" pero HAY alternativas, fuerza la segunda más rápida distinta
    if mas_rapida["coop_id"] == mas_barata["coop_id"] and len(base_items) > 1:
        mas_rapida_alt = min([x for x in base_items if x["coop_id"] != mas_barata["coop_id"]], key=_duracion)
        mas_rapida = mas_rapida_alt

    # ---- Render UI: tarjetas ----
    def _fmt_money(v):
        fv = _to_float(v)
        return f"${fv:.2f}" if fv is not None else "N/A"

    def _fmt_num(v, suf=""):
        fv = _to_float(v)
        return f"{fv:.2f}{suf}" if fv is not None else "N/A"

    def _tarjeta_reco(parent, titulo_txt, item, color_barra):
        card = tk.Frame(parent, bg=COLORS['white'], bd=1, relief='solid')
        card.pack(side='left', fill='both', expand=True, padx=10)

        barra = tk.Frame(card, bg=color_barra, height=36)
        barra.pack(fill='x')
        tk.Label(
            barra,
            text=f"★  {titulo_txt}",
            font=('Arial', 11, 'bold'),
            fg='white',
            bg=color_barra
        ).pack(anchor='w', padx=12, pady=8)

        body = tk.Frame(card, bg=COLORS['white'])
        body.pack(fill='both', expand=True, padx=12, pady=10)

        if item is None:
            tk.Label(
                body,
                text="No disponible (no hay distancia diferente)",
                font=('Arial', 10),
                fg=COLORS['danger'],
                bg=COLORS['white']
            ).pack(anchor='w', pady=(6, 10))
            return

        coop = item['coop_data']
        ruta = item['ruta_data']

        tk.Label(
            body,
            text=coop.get('nombre', 'Cooperativa'),
            font=('Arial', 11, 'bold'),
            fg=COLORS['text_dark'],
            bg=COLORS['white']
        ).pack(anchor='w')

        info = f" {_fmt_money(ruta.get('precio'))} {_fmt_num(ruta.get('duracion_horas'), ' h')} {_fmt_num(ruta.get('distancia_km'), ' km')}"
        tk.Label(
            body,
            text=info,
            font=('Arial', 10),
            fg=COLORS['text_light'],
            bg=COLORS['white']
        ).pack(anchor='w', pady=(6, 12))

        btn = crear_boton_estilo(
            body,
            "Elegir",
            lambda cid=item['coop_id'], rid=item['ruta_id']: mostrar_horarios(content_frame_usuario, cid, rid, usuario_actual),
            'primary'
        )
        btn.pack(anchor='w')

    def render_recomendaciones():
        view_rank.pack_forget()
        _clear(view_reco)
        view_reco.pack(fill='both', expand=True)

        tk.Label(
            view_reco,
            text="Recomendaciones",
            font=('Arial', 12, 'bold'),
            fg=COLORS['text_dark'],
            bg=COLORS['white']
        ).pack(anchor='w', padx=20, pady=(6, 10))

        row = tk.Frame(view_reco, bg=COLORS['white'])
        row.pack(fill='x', padx=10)

        # Mismo contraste (misma barra). Si quieres diferenciar, puedes cambiar color_barra por criterios.
        barra_color = COLORS['primary']

        _tarjeta_reco(row, "Más barata", mas_barata, barra_color)
        _tarjeta_reco(row, "Más rápida", mas_rapida, barra_color)
        _tarjeta_reco(row, "Más larga", mas_larga, barra_color)

        # Botón volver al inicio
        btn_back = crear_boton_estilo(
            view_reco,
            "← Volver al inicio",
            lambda: mostrar_home_usuario(content_frame_usuario, usuario_actual),
            'accent'
        )
        btn_back.pack(pady=20)

    # ---- Ranking view ----
    def render_ranking(modo):
        view_reco.pack_forget()
        _clear(view_rank)
        view_rank.pack(fill='both', expand=True)

        actions = tk.Frame(view_rank, bg=COLORS['white'])
        actions.pack(fill='x', padx=20, pady=(10, 8))

        crear_boton_estilo(
            actions,
            "← Volver a Recomendaciones",
            render_recomendaciones,
            'primary'
        ).pack(side='left')

        crear_boton_estilo(
            actions,
            " Inicio",
            lambda: mostrar_home_usuario(content_frame_usuario, usuario_actual),
            'accent'
        ).pack(side='left', padx=10)

        tk.Label(
            actions,
            text=f"Ranking por {modo.title()} | {origen} → {destino}",
            font=('Arial', 12, 'bold'),
            fg=COLORS['text_dark'],
            bg=COLORS['white']
        ).pack(side='right')

        # construir items por cooperativa según criterio
        if modo == "precio":
            items = _build_items("precio")
            items.sort(key=_precio)
        elif modo == "duracion":
            items = _build_items("duracion")
            items.sort(key=_duracion)
        else:
            items = _build_items("distancia")
            items.sort(key=_distancia, reverse=True)

        scrollable_frame, canvas = crear_scrollable_frame(view_rank)

        # rueda mouse
        def _on_mousewheel(event):
            try:
                canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            except Exception:
                pass
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        for i, item in enumerate(items, start=1):
            coop = item['coop_data']
            ruta = item['ruta_data']

            card = tk.Frame(scrollable_frame, bg=COLORS['background'], bd=1, relief='solid')
            card.pack(fill='x', padx=20, pady=8)

            tk.Label(
                card,
                text=f"#{i}  {coop.get('nombre','Cooperativa')}",
                font=('Arial', 11, 'bold'),
                fg=COLORS['text_dark'],
                bg=COLORS['background']
            ).pack(anchor='w', padx=12, pady=(10, 0))

            info = f" {_fmt_money(ruta.get('precio'))} {_fmt_num(ruta.get('duracion_horas'), ' h')} {_fmt_num(ruta.get('distancia_km'), ' km')}"
            tk.Label(
                card,
                text=info,
                font=('Arial', 10),
                fg=COLORS['text_light'],
                bg=COLORS['background']
            ).pack(anchor='w', padx=12, pady=(4, 10))

            btn = crear_boton_estilo(
                card,
                "Elegir",
                lambda cid=item['coop_id'], rid=item['ruta_id']: mostrar_horarios(content_frame_usuario, cid, rid, usuario_actual),
                'primary'
            )
            btn.pack(anchor='e', padx=12, pady=(0, 12))

    # Botones del topbar: abren ranking EN LA MISMA PANTALLA
    btns = tk.Frame(topbar, bg=COLORS['white'])
    btns.pack(side='right')

    tk.Button(btns, text="Precio", command=lambda: render_ranking("precio"),
              bg=COLORS['background'], fg=COLORS['text_dark'], relief='solid', bd=1, padx=14, pady=6).pack(side='left', padx=6)
    tk.Button(btns, text="Duración", command=lambda: render_ranking("duracion"),
              bg=COLORS['background'], fg=COLORS['text_dark'], relief='solid', bd=1, padx=14, pady=6).pack(side='left', padx=6)
    tk.Button(btns, text="Distancia", command=lambda: render_ranking("distancia"),
              bg=COLORS['background'], fg=COLORS['text_dark'], relief='solid', bd=1, padx=14, pady=6).pack(side='left', padx=6)

    render_recomendaciones()

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
    
    info_text = f" {ruta_data.get('origen', 'N/A')} → {ruta_data.get('destino', 'N/A')} |  ${ruta_data.get('precio', 0.0):.2f}"
    tk.Label(info_frame, text=info_text, font=('Arial', 12, 'bold'), 
             fg=COLORS['text_dark'], bg=COLORS['background']).pack(pady=15)
    
    # Horarios disponibles
    horarios_frame = tk.Frame(main_frame, bg=COLORS['white'])
    horarios_frame.pack(fill='both', expand=True, padx=20, pady=20)
    
    tk.Label(horarios_frame, text=" Horarios Disponibles:", 
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

    # Layout del bus (mejorado + scroll)
    # Nota: el layout está dentro de una tarjeta con header rojo, igual al estilo del sistema.
    bus_card = tk.Frame(main_left, bg=COLORS['white'], bd=1, relief='solid')
    bus_card.pack(pady=20, padx=20, fill='both', expand=True)

    header_bus = tk.Frame(bus_card, bg=COLORS['primary'])
    header_bus.pack(fill='x')
    tk.Label(
        header_bus,
        text="Layout del Bus (40 Asientos)",
        font=('Arial', 12, 'bold'),
        bg=COLORS['primary'],
        fg='white',
        padx=14,
        pady=10
    ).pack(anchor='w')

    body_bus = tk.Frame(bus_card, bg=COLORS['white'])
    body_bus.pack(fill='both', expand=True)

    # --- Scroll vertical para poder ver los últimos asientos ---
    canvas_bus = tk.Canvas(body_bus, bg=COLORS['white'], highlightthickness=0)
    scrollbar_bus = ttk.Scrollbar(body_bus, orient='vertical', command=canvas_bus.yview)
    canvas_bus.configure(yscrollcommand=scrollbar_bus.set)

    scrollbar_bus.pack(side='right', fill='y')
    canvas_bus.pack(side='left', fill='both', expand=True)

    # Frame interno dentro del canvas.
    # Lo centramos horizontalmente (especialmente útil cuando se pone pantalla completa).
    scroll_frame = tk.Frame(canvas_bus, bg=COLORS['white'])
    canvas_window_id = canvas_bus.create_window((0, 0), window=scroll_frame, anchor='n')

    def _on_bus_configure(event=None):
        # Ajusta el área scrolleable
        canvas_bus.configure(scrollregion=canvas_bus.bbox('all'))

    def _on_canvas_bus_resize(event):
        """Centra el contenido del canvas y lo hace tomar el ancho del canvas."""
        try:
            canvas_bus.itemconfigure(canvas_window_id, width=event.width)
            canvas_bus.coords(canvas_window_id, event.width / 2, 0)
        except Exception:
            pass

    scroll_frame.bind('<Configure>', _on_bus_configure)
    canvas_bus.bind('<Configure>', _on_canvas_bus_resize)

    # Ruedita del mouse (solo cuando el cursor está sobre el layout)
    def _on_mousewheel_bus(event):
        # Windows / Linux
        if hasattr(event, 'delta') and event.delta:
            delta = int(-1 * (event.delta / 120))
            canvas_bus.yview_scroll(delta, 'units')

    def _bind_mousewheel(_):
        canvas_bus.bind_all('<MouseWheel>', _on_mousewheel_bus)

    def _unbind_mousewheel(_):
        canvas_bus.unbind_all('<MouseWheel>')

    canvas_bus.bind('<Enter>', _bind_mousewheel)
    canvas_bus.bind('<Leave>', _unbind_mousewheel)

    # Contenedor de asientos (centrado) + más espacio de pasillo
    asientos_container = tk.Frame(scroll_frame, bg=COLORS['white'], padx=24, pady=18)
    asientos_container.pack(anchor='n')

    # Cabecera del bus (conductor / pasillo / entrada)
    driver_box = tk.Frame(asientos_container, bg=COLORS['background'], bd=1, relief='solid')
    driver_box.grid(row=0, column=0, columnspan=2, padx=6, pady=(0, 12), sticky='w')
    tk.Label(driver_box, text='Conductor', font=('Arial', 9, 'bold'), bg=COLORS['background'], fg=COLORS['text_dark']).pack(padx=12, pady=7)

    tk.Label(
        asientos_container,
        text='PASILLO',
        font=('Arial', 8, 'bold'),
        bg=COLORS['white'],
        fg=COLORS['text_light']
    ).grid(row=0, column=2, padx=20, pady=(0, 12))

    entry_box = tk.Frame(asientos_container, bg=COLORS['background'], bd=1, relief='solid')
    entry_box.grid(row=0, column=3, columnspan=2, padx=6, pady=(0, 12), sticky='e')
    tk.Label(entry_box, text='Entrada', font=('Arial', 9, 'bold'), bg=COLORS['background'], fg=COLORS['text_dark']).pack(padx=12, pady=7)

    # Ayuda pequeña abajo
    tk.Label(
        bus_card,
        text='Tip: usa la ruedita del mouse o la barra para ver los últimos asientos.',
        font=('Arial', 9),
        bg=COLORS['white'],
        fg=COLORS['text_light']
    ).pack(anchor='w', padx=14, pady=(6, 10))

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

    # Cargar datos
    boletos = cargar_boletos()
    rutas = cargar_rutas()
    cooperativas = cargar_cooperativas()
    horarios = cargar_horarios()

    # Historial Activo (boletos del usuario)
    mis_boletos = [b for b in boletos if b.get('usuario') == usuario_actual]
    mis_boletos.sort(key=lambda x: x.get('fecha_compra', '0000-01-01'), reverse=True)

    if not mis_boletos:
        tk.Label(tab_historial, text="No has comprado boletos activos.", 
                 font=('Arial', 12), fg=COLORS['text_light'], bg=COLORS['white']).pack(pady=50)
    else:
        crear_tabla_historial(tab_historial, mis_boletos, rutas, cooperativas, horarios, es_papelera=False,
                             content_frame_usuario=content_frame_usuario, usuario_actual=usuario_actual)

    # Nota:
    # La recuperación de boletos eliminados se gestiona desde el Panel del Administrador (Papelera de Boletos).

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
    """Muestra la búsqueda de rutas por horario (UI estilo tarjetas, similar a Buscar Cooperativa)"""
    for widget in content_frame_usuario.winfo_children():
        widget.destroy()

    main_frame = crear_frame_contenedor(content_frame_usuario, 20)
    main_frame.config(bg=COLORS['white'])

    # ---- Título ----
    titulo = crear_label_titulo(main_frame, "Buscar Rutas por Horario", 18)
    titulo.pack(pady=(18, 12))
    titulo.config(bg=COLORS['white'])

    # Fecha fija de viaje (mañana)
    fecha_viaje = (datetime.now() + timedelta(days=1))
    fecha_viaje_str = fecha_viaje.strftime('%Y-%m-%d')
    fecha_legible = fecha_viaje.strftime('%d/%m/%Y')

    # ---- Panel de filtros (similar a topbar) ----
    filtros_panel = tk.Frame(main_frame, bg=COLORS['background'], bd=1, relief='solid')
    filtros_panel.pack(fill='x', padx=25, pady=(0, 15))

    left = tk.Frame(filtros_panel, bg=COLORS['background'])
    left.pack(side='left', padx=15, pady=12)

    tk.Label(
        left,
        text=f"Fecha fija de viaje: {fecha_legible} (Mañana)",
        font=('Arial', 11, 'italic'),
        bg=COLORS['background'],
        fg=COLORS['text_light']
    ).pack(anchor='w')

    right = tk.Frame(filtros_panel, bg=COLORS['background'])
    right.pack(side='right', padx=15, pady=10)

    tk.Label(
        right,
        text="Rango de hora:",
        font=('Arial', 11, 'bold'),
        bg=COLORS['background'],
        fg=COLORS['text_dark']
    ).grid(row=0, column=0, padx=(0, 10), pady=2, sticky='e')

    horas_disponibles = [
        "Cualquier Hora",
        "00:00-06:00 (Madrugada)",
        "06:00-12:00 (Mañana)",
        "12:00-18:00 (Tarde)",
        "18:00-23:59 (Noche)"
    ]

    combo_hora = ttk.Combobox(
        right,
        values=horas_disponibles,
        width=28,
        font=('Arial', 10),
        state="readonly"
    )
    combo_hora.set("Cualquier Hora")
    combo_hora.grid(row=0, column=1, padx=(0, 10), pady=2)

    # ---- Resultados con scrollbar ----
    resultados_container = tk.Frame(main_frame, bg=COLORS['white'])
    resultados_container.pack(fill='both', expand=True, padx=25, pady=(0, 10))

    canvas = tk.Canvas(resultados_container, bg=COLORS['white'], highlightthickness=0)
    scrollbar = tk.Scrollbar(resultados_container, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg=COLORS['white'])

    window_id = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

    def _sync_width(event):
        # asegura que el contenido use el ancho del canvas (evita que quede angosto)
        try:
            canvas.itemconfig(window_id, width=event.width)
        except Exception:
            pass

    canvas.bind("<Configure>", _sync_width)

    def on_frame_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    scrollable_frame.bind("<Configure>", on_frame_configure)
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    def _match_filtro(hora_salida, filtro_hora_str):
        """Devuelve True si la hora coincide con el filtro seleccionado."""
        if filtro_hora_str == "Cualquier Hora":
            return True
        rango_part = filtro_hora_str.split('(')[0].strip()
        try:
            h_inicio_str, h_fin_str = rango_part.split('-')
            h_salida = datetime.strptime(hora_salida, '%H:%M').time()
            h_inicio = datetime.strptime(h_inicio_str, '%H:%M').time()
            h_fin = datetime.strptime(h_fin_str, '%H:%M').time()
            return (h_salida >= h_inicio and h_salida <= h_fin)
        except Exception:
            return True

    def _tarjeta_ruta(parent, info, row, col):
        """Crea una tarjeta estilo 'Buscar cooperativa' para una ruta con sus horarios."""
        ruta = info['ruta']
        coop = info['cooperativa']
        horarios_list = sorted(info['horarios'])

        # compactar horarios si son demasiados
        if len(horarios_list) > 6:
            horarios_str = ", ".join(horarios_list[:6]) + " ..."
        else:
            horarios_str = ", ".join(horarios_list)

        card = tk.Frame(parent, bg=COLORS['white'], bd=1, relief='solid')
        card.grid(row=row, column=col, sticky='nsew', padx=10, pady=10)

        # barra superior
        barra = tk.Frame(card, bg=COLORS['primary'], height=34)
        barra.pack(fill='x')
        tk.Label(
            barra,
            text=coop.get('nombre', 'Cooperativa'),
            font=('Arial', 11, 'bold'),
            fg='white',
            bg=COLORS['primary']
        ).pack(anchor='w', padx=12, pady=7)

        body = tk.Frame(card, bg=COLORS['white'])
        body.pack(fill='both', expand=True, padx=12, pady=10)

        # info principal
        tk.Label(
            body,
            text=f"Ruta: {ruta.get('origen', 'N/A')} → {ruta.get('destino', 'N/A')}",
            font=('Arial', 10, 'bold'),
            fg=COLORS['text_dark'],
            bg=COLORS['white']
        ).pack(anchor='w')

        precio = ruta.get('precio', 0.0)
        try:
            precio_txt = f"${float(precio):.2f}"
        except Exception:
            precio_txt = "N/A"

        tk.Label(
            body,
            text=f"💰 {precio_txt}   ⏱ {ruta.get('duracion_horas', 'N/A')} h   📏 {ruta.get('distancia_km', 'N/A')} km",
            font=('Arial', 10),
            fg=COLORS['text_light'],
            bg=COLORS['white']
        ).pack(anchor='w', pady=(6, 0))

        tk.Label(
            body,
            text=f"Horarios: {horarios_str}",
            font=('Arial', 10),
            fg=COLORS['text_light'],
            bg=COLORS['white'],
            wraplength=520,
            justify='left'
        ).pack(anchor='w', pady=(6, 12))

        def seleccionar_ruta(o=ruta.get('origen'), d=ruta.get('destino')):
            # lleva a la pantalla de cooperativas (misma experiencia visual)
            mostrar_resultados_busqueda(content_frame_usuario, o, d, usuario_actual)

        btn = crear_boton_estilo(body, "Elegir", seleccionar_ruta, 'primary')
        btn.pack(anchor='w', pady=(0, 6))

    def mostrar_todas_las_rutas():
        # limpiar resultados anteriores
        for widget in scrollable_frame.winfo_children():
            widget.destroy()

        filtro_hora_str = combo_hora.get()

        rutas = cargar_rutas()
        horarios = cargar_horarios()
        cooperativas = cargar_cooperativas()

        rutas_con_horarios = {}

        # agrupar horarios por ruta, filtrando por rango de hora
        for hid, hdata in horarios.items():
            ruta_id = hdata.get('ruta_id')
            if not ruta_id or ruta_id not in rutas:
                continue

            hora_salida = hdata.get('hora')
            if not hora_salida:
                continue

            if not _match_filtro(hora_salida, filtro_hora_str):
                continue

            ruta_data = rutas[ruta_id]
            coop_data = cooperativas.get(ruta_data.get('cooperativa_id'), {'nombre': 'N/A'})

            if ruta_id not in rutas_con_horarios:
                rutas_con_horarios[ruta_id] = {
                    'ruta': ruta_data,
                    'cooperativa': coop_data,
                    'horarios': []
                }
            if hora_salida not in rutas_con_horarios[ruta_id]['horarios']:
                rutas_con_horarios[ruta_id]['horarios'].append(hora_salida)

        if not rutas_con_horarios:
            msg = tk.Frame(scrollable_frame, bg=COLORS['white'])
            msg.pack(fill='both', expand=True, pady=60)

            tk.Label(
                msg,
                text="No hay rutas disponibles para el filtro seleccionado.",
                font=('Arial', 12, 'bold'),
                fg=COLORS['danger'],
                bg=COLORS['white']
            ).pack()
            return

        # cabecera de resultados
        header = tk.Frame(scrollable_frame, bg=COLORS['white'])
        header.pack(fill='x', padx=10, pady=(5, 10))

        tk.Label(
            header,
            text=f"Resultados de búsqueda: {len(rutas_con_horarios)} ruta(s)",
            font=('Arial', 12, 'bold'),
            fg=COLORS['text_dark'],
            bg=COLORS['white']
        ).pack(anchor='w')

        # grid de tarjetas (2 columnas)
        grid = tk.Frame(scrollable_frame, bg=COLORS['white'])
        grid.pack(fill='x', padx=0, pady=(0, 10))

        grid.grid_columnconfigure(0, weight=1)
        grid.grid_columnconfigure(1, weight=1)

        items = list(rutas_con_horarios.items())

        for idx, (ruta_id, info) in enumerate(items):
            r = idx // 2
            c = idx % 2
            _tarjeta_ruta(grid, info, r, c)

    # botón buscar (dispara render de resultados)
    btn_buscar = crear_boton_estilo(
        right,
        "Buscar",
        mostrar_todas_las_rutas,
        'accent',
        width=10
    )
    btn_buscar.grid(row=0, column=2, padx=(0, 0), pady=2)

    # botones inferiores (inicio)
    bottom = tk.Frame(main_frame, bg=COLORS['white'])
    bottom.pack(fill='x', pady=(0, 18))

    btn_volver = crear_boton_estilo(
        bottom,
        "← Volver al inicio",
        lambda: mostrar_home_usuario(content_frame_usuario, usuario_actual),
        'accent'
    )
    btn_volver.pack(pady=10)

    # render inicial
    mostrar_todas_las_rutas()

    # scroll con rueda del mouse
    def _on_mousewheel(event):
        if canvas.winfo_exists():
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    canvas.bind_all("<MouseWheel>", _on_mousewheel)
