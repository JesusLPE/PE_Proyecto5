"""
Interfaz del administrador - Gestión completa del sistema
"""

import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
from src.utilidades import crear_estilo_ventana, crear_frame_contenedor, crear_label_titulo, crear_boton_estilo
from src.archivos import (
    cargar_cooperativas, guardar_cooperativas, 
    cargar_rutas, guardar_rutas, 
    cargar_horarios, guardar_horarios,
    cargar_boletos, cargar_usuarios
)
from src.configuracion import CIUDADES_ECUADOR, COLORS



def mostrar_gestion_cooperativas(content_frame, admin_user):
    """Muestra el panel de gestión de Cooperativas."""
    for widget in content_frame.winfo_children():
        widget.destroy()
        
    main_frame = crear_frame_contenedor(content_frame, 10)
    
    crear_label_titulo(main_frame, " Gestión de Cooperativas", 16).pack(pady=(10, 20))
    
    # Formulario de registro
    form_frame = tk.LabelFrame(main_frame, text="➕ Registrar Nueva Cooperativa", 
                              bg=COLORS['background'], font=('Arial', 11, 'bold'))
    form_frame.pack(fill='x', padx=20, pady=10)
    
    campos = [
        ("Nombre:", "nombre", 0),
        ("RUC:", "ruc", 1),
        ("Teléfono:", "telefono", 2),
        ("Email:", "email", 3),
        ("Dirección:", "direccion", 4),
        ("Representante:", "representante", 5),
        ("Número de Buses:", "numero_buses", 6)
    ]
    
    entradas = {}
    
    for label_text, key, row in campos:
        tk.Label(form_frame, text=label_text, bg=COLORS['background']).grid(
            row=row, column=0, padx=10, pady=5, sticky='w')
        
        if key == 'numero_buses':
            entrada = tk.Entry(form_frame, width=30)
            entrada.insert(0, "25")  # Valor por defecto
        else:
            entrada = tk.Entry(form_frame, width=30)
            
        entrada.grid(row=row, column=1, padx=10, pady=5, sticky='ew')
        entradas[key] = entrada
    
    def registrar_cooperativa():
        valores = {k: v.get().strip() for k, v in entradas.items()}
        
        if not all(valores.values()):
            messagebox.showerror("Error", "Complete todos los campos de la cooperativa.")
            return
        
        # Validar RUC (13 dígitos)
        if len(valores['ruc']) != 13 or not valores['ruc'].isdigit():
            messagebox.showerror("Error", "El RUC debe tener 13 dígitos numéricos.")
            return
        
        # Validar número de buses
        try:
            num_buses = int(valores['numero_buses'])
            if num_buses <= 0:
                messagebox.showerror("Error", "El número de buses debe ser mayor a 0.")
                return
        except ValueError:
            messagebox.showerror("Error", "Número de Buses debe ser un número entero.")
            return
        
        cooperativas = cargar_cooperativas()
        
        # Verificar si el RUC ya existe
        for coop_id, coop_data in cooperativas.items():
            if coop_data.get('ruc') == valores['ruc']:
                messagebox.showerror("Error", "El RUC ya está registrado para otra cooperativa.")
                return
        
        # Generar ID único
        new_id = f"coop_{len(cooperativas) + 1:03d}"
        
        cooperativas[new_id] = {
            "id": new_id,
            "nombre": valores['nombre'],
            "ruc": valores['ruc'],
            "telefono": valores['telefono'],
            "email": valores['email'],
            "direccion": valores['direccion'],
            "representante": valores['representante'],
            "numero_buses": num_buses,
            "fecha_creacion": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "creado_por": admin_user,
            "estado": "activa"
        }
        
        guardar_cooperativas(cooperativas)
        messagebox.showinfo("Éxito", f"Cooperativa '{valores['nombre']}' registrada exitosamente.")
        
        # Limpiar campos
        for entrada in entradas.values():
            entrada.delete(0, tk.END)
            if 'numero_buses' in str(entrada):
                entrada.insert(0, "25")
        
        # Actualizar lista
        mostrar_gestion_cooperativas(content_frame, admin_user)
    
    btn_frame = tk.Frame(form_frame, bg=COLORS['background'])
    btn_frame.grid(row=7, column=1, pady=10, sticky='e')
    
    crear_boton_estilo(btn_frame, "Guardar Cooperativa", registrar_cooperativa, 'primary', 20).pack(side='right', padx=5)
    
    # Lista de cooperativas existentes
    lista_frame = tk.LabelFrame(main_frame, text=" Cooperativas Existentes", 
                               bg=COLORS['white'], font=('Arial', 11, 'bold'), fg=COLORS['text_dark'])
    lista_frame.pack(fill='both', expand=True, padx=20, pady=10)
    
    cooperativas = cargar_cooperativas()
    
    if not cooperativas:
        tk.Label(lista_frame, text=" No hay cooperativas registradas.", 
                 font=('Arial', 11), fg=COLORS['danger'], bg=COLORS['white']).pack(pady=20)
        return
    
    # Crear tabla con Treeview
    columns = ("ID", "Nombre", "RUC", "Teléfono", "Buses", "Estado")
    tree = ttk.Treeview(lista_frame, columns=columns, show="headings", height=10)
    
    # Configurar columnas
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=100)
    
    tree.column("Nombre", width=150)
    tree.column("RUC", width=120)
    
    # Agregar scrollbar
    scrollbar = ttk.Scrollbar(lista_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    
    # Insertar datos
    for coop_id, data in cooperativas.items():
        tree.insert("", "end", values=(
            coop_id,
            data['nombre'],
            data['ruc'],
            data['telefono'],
            data['numero_buses'],
            data['estado']
        ))
    
    # Empacar
    tree.pack(side="left", fill="both", expand=True, padx=10, pady=10)
    scrollbar.pack(side="right", fill="y", pady=10)
    
    # Botones de acción
    action_frame = tk.Frame(lista_frame, bg=COLORS['white'])
    action_frame.pack(fill='x', padx=10, pady=5)
    
    def eliminar_cooperativa():
        seleccionado = tree.selection()
        if not seleccionado:
            messagebox.showerror("Error", "Seleccione una cooperativa para eliminar.")
            return
        
        item = tree.item(seleccionado[0])
        coop_id = item['values'][0]
        coop_nombre = item['values'][1]
        
        if not messagebox.askyesno("Confirmar", f"¿Eliminar la cooperativa '{coop_nombre}'?"):
            return
        
        cooperativas.pop(coop_id, None)
        guardar_cooperativas(cooperativas)
        messagebox.showinfo("Éxito", f"Cooperativa '{coop_nombre}' eliminada.")
        mostrar_gestion_cooperativas(content_frame, admin_user)
    
    crear_boton_estilo(action_frame, "Eliminar Seleccionada", eliminar_cooperativa, 'danger', 20).pack(side='right', padx=5)

def mostrar_gestion_rutas(content_frame, admin_user):
    """Muestra el panel de gestión de Rutas."""
    for widget in content_frame.winfo_children():
        widget.destroy()
        
    main_frame = crear_frame_contenedor(content_frame, 10)
    
    crear_label_titulo(main_frame, " Gestión de Rutas", 16).pack(pady=(10, 20))
    
    # Formulario de registro
    form_frame = tk.LabelFrame(main_frame, text="➕ Registrar Nueva Ruta", 
                              bg=COLORS['background'], font=('Arial', 11, 'bold'))
    form_frame.pack(fill='x', padx=20, pady=10)
    
    # Cargar cooperativas para el combobox
    cooperativas = cargar_cooperativas()
    coop_options = [f"{data['nombre']} ({cid})" for cid, data in cooperativas.items()]
    
    # Campos del formulario
    tk.Label(form_frame, text="Cooperativa:", bg=COLORS['background']).grid(
        row=0, column=0, padx=10, pady=5, sticky='w')
    combo_coop = ttk.Combobox(form_frame, values=coop_options, state="readonly", width=28)
    combo_coop.grid(row=0, column=1, padx=10, pady=5, sticky='ew')
    
    tk.Label(form_frame, text="Origen:", bg=COLORS['background']).grid(
        row=1, column=0, padx=10, pady=5, sticky='w')
    combo_origen = ttk.Combobox(form_frame, values=CIUDADES_ECUADOR, state="readonly", width=28)
    combo_origen.grid(row=1, column=1, padx=10, pady=5, sticky='ew')
    combo_origen.set("Quito")
    
    tk.Label(form_frame, text="Destino:", bg=COLORS['background']).grid(
        row=2, column=0, padx=10, pady=5, sticky='w')
    combo_destino = ttk.Combobox(form_frame, values=CIUDADES_ECUADOR, state="readonly", width=28)
    combo_destino.grid(row=2, column=1, padx=10, pady=5, sticky='ew')
    combo_destino.set("Cuenca")
    
    tk.Label(form_frame, text="Precio ($):", bg=COLORS['background']).grid(
        row=3, column=0, padx=10, pady=5, sticky='w')
    entrada_precio = tk.Entry(form_frame, width=30)
    entrada_precio.grid(row=3, column=1, padx=10, pady=5, sticky='ew')
    entrada_precio.insert(0, "15.50")
    
    def registrar_ruta():
        coop_str = combo_coop.get()
        origen = combo_origen.get()
        destino = combo_destino.get()
        precio_str = entrada_precio.get().strip()
        
        if not all([coop_str, origen, destino, precio_str]):
            messagebox.showerror("Error", "Complete todos los campos de la ruta.")
            return
        
        if origen == destino:
            messagebox.showerror("Error", "El origen y destino deben ser diferentes.")
            return
        
        try:
            precio = float(precio_str)
            if precio <= 0:
                messagebox.showerror("Error", "El precio debe ser mayor a 0.")
                return
        except ValueError:
            messagebox.showerror("Error", "El precio debe ser un número válido.")
            return
        
        # Extraer ID de cooperativa del string seleccionado
        try:
            coop_id = coop_str.split('(')[-1].replace(')', '').strip()
        except:
            messagebox.showerror("Error", "Seleccione una cooperativa válida.")
            return
        
        rutas = cargar_rutas()
        
        # Verificar si ya existe esta ruta para la cooperativa
        for ruta_id, ruta_data in rutas.items():
            if (ruta_data['cooperativa_id'] == coop_id and 
                ruta_data['origen'] == origen and 
                ruta_data['destino'] == destino):
                messagebox.showerror("Error", "Esta ruta ya existe para la cooperativa seleccionada.")
                return
        
        # Generar ID único
        new_id = f"ruta_{len(rutas) + 1:03d}"
        
        rutas[new_id] = {
            "id": new_id,
            "cooperativa_id": coop_id,
            "origen": origen,
            "destino": destino,
            "precio": precio,
            "fecha_creacion": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "creado_por": admin_user,
            "estado": "activa"
        }
        
        guardar_rutas(rutas)
        messagebox.showinfo("Éxito", f"Ruta {origen} -> {destino} registrada exitosamente.")
        
        # Limpiar campos
        entrada_precio.delete(0, tk.END)
        entrada_precio.insert(0, "15.50")
        
        # Actualizar lista
        mostrar_gestion_rutas(content_frame, admin_user)
    
    btn_frame = tk.Frame(form_frame, bg=COLORS['background'])
    btn_frame.grid(row=4, column=1, pady=10, sticky='e')
    
    crear_boton_estilo(btn_frame, "Guardar Ruta", registrar_ruta, 'primary', 20).pack(side='right', padx=5)
    
    # Lista de rutas existentes
    lista_frame = tk.LabelFrame(main_frame, text=" Rutas Existentes", 
                               bg=COLORS['white'], font=('Arial', 11, 'bold'), fg=COLORS['text_dark'])
    lista_frame.pack(fill='both', expand=True, padx=20, pady=10)
    
    rutas = cargar_rutas()
    
    if not rutas:
        tk.Label(lista_frame, text=" No hay rutas registradas.", 
                 font=('Arial', 11), fg=COLORS['danger'], bg=COLORS['white']).pack(pady=20)
        return
    
    # Crear tabla con Treeview
    columns = ("ID", "Cooperativa", "Origen", "Destino", "Precio", "Estado")
    tree = ttk.Treeview(lista_frame, columns=columns, show="headings", height=10)
    
    # Configurar columnas
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=100)
    
    tree.column("Cooperativa", width=150)
    tree.column("Origen", width=100)
    tree.column("Destino", width=100)
    tree.column("Precio", width=80)
    
    # Agregar scrollbar
    scrollbar = ttk.Scrollbar(lista_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    
    # Insertar datos
    for ruta_id, data in rutas.items():
        coop_nombre = cooperativas.get(data['cooperativa_id'], {}).get('nombre', 'N/A')
        tree.insert("", "end", values=(
            ruta_id,
            coop_nombre,
            data['origen'],
            data['destino'],
            f"${data['precio']:.2f}",
            data['estado']
        ))
    
    # Empacar
    tree.pack(side="left", fill="both", expand=True, padx=10, pady=10)
    scrollbar.pack(side="right", fill="y", pady=10)
    
    # Botones de acción
    action_frame = tk.Frame(lista_frame, bg=COLORS['white'])
    action_frame.pack(fill='x', padx=10, pady=5)
    
    def eliminar_ruta():
        seleccionado = tree.selection()
        if not seleccionado:
            messagebox.showerror("Error", "Seleccione una ruta para eliminar.")
            return
        
        item = tree.item(seleccionado[0])
        ruta_id = item['values'][0]
        origen = item['values'][2]
        destino = item['values'][3]
        
        if not messagebox.askyesno("Confirmar", f"¿Eliminar la ruta {origen} -> {destino}?"):
            return
        
        rutas.pop(ruta_id, None)
        guardar_rutas(rutas)
        messagebox.showinfo("Éxito", f"Ruta {origen} -> {destino} eliminada.")
        mostrar_gestion_rutas(content_frame, admin_user)
    
    crear_boton_estilo(action_frame, "Eliminar Seleccionada", eliminar_ruta, 'danger', 20).pack(side='right', padx=5)

def mostrar_gestion_horarios(content_frame, admin_user):
    """Muestra el panel de gestión de Horarios."""
    for widget in content_frame.winfo_children():
        widget.destroy()
        
    main_frame = crear_frame_contenedor(content_frame, 10)
    
    crear_label_titulo(main_frame, " Gestión de Horarios", 16).pack(pady=(10, 20))
    
    # Formulario de registro
    form_frame = tk.LabelFrame(main_frame, text="➕ Registrar Nuevo Horario", 
                              bg=COLORS['background'], font=('Arial', 11, 'bold'))
    form_frame.pack(fill='x', padx=20, pady=10)
    
    # Cargar datos para combobox
    rutas = cargar_rutas()
    cooperativas = cargar_cooperativas()
    
    # Crear lista de rutas formateadas
    rutas_options = []
    for ruta_id, ruta_data in rutas.items():
        coop_nombre = cooperativas.get(ruta_data['cooperativa_id'], {}).get('nombre', 'N/A')
        ruta_text = f"{ruta_data['origen']} → {ruta_data['destino']} ({coop_nombre}) - ID: {ruta_id}"
        rutas_options.append(ruta_text)
    
    tk.Label(form_frame, text="Ruta:", bg=COLORS['background']).grid(
        row=0, column=0, padx=10, pady=5, sticky='w')
    combo_ruta = ttk.Combobox(form_frame, values=rutas_options, state="readonly", width=45)
    combo_ruta.grid(row=0, column=1, padx=10, pady=5, sticky='ew')
    
    tk.Label(form_frame, text="Hora (HH:MM):", bg=COLORS['background']).grid(
        row=1, column=0, padx=10, pady=5, sticky='w')
    entrada_hora = tk.Entry(form_frame, width=30)
    entrada_hora.grid(row=1, column=1, padx=10, pady=5, sticky='ew')
    entrada_hora.insert(0, "06:00")
    
    def registrar_horario():
        ruta_str = combo_ruta.get()
        hora_str = entrada_hora.get().strip()
        
        if not all([ruta_str, hora_str]):
            messagebox.showerror("Error", "Complete todos los campos del horario.")
            return
        
        # Validar formato de hora
        try:
            datetime.strptime(hora_str, '%H:%M')
        except ValueError:
            messagebox.showerror("Error", "Formato de hora incorrecto. Use HH:MM (ej: 14:30).")
            return
        
        # Extraer ID de ruta (última parte después de "ID: ")
        try:
            ruta_id = ruta_str.split('ID: ')[-1].strip()
        except:
            messagebox.showerror("Error", "Seleccione una ruta válida.")
            return
        
        horarios = cargar_horarios()
        
        # Verificar si ya existe este horario para la ruta
        for horario_id, horario_data in horarios.items():
            if (horario_data['ruta_id'] == ruta_id and 
                horario_data['hora'] == hora_str):
                messagebox.showerror("Error", "Este horario ya existe para la ruta seleccionada.")
                return
        
        # Generar ID único
        new_id = f"h{len(horarios) + 1:03d}"
        
        horarios[new_id] = {
            "id": new_id,
            "ruta_id": ruta_id,
            "hora": hora_str
        }
        
        guardar_horarios(horarios)
        messagebox.showinfo("Éxito", f"Horario {hora_str} registrado exitosamente.")
        
        # Limpiar campo de hora
        entrada_hora.delete(0, tk.END)
        entrada_hora.insert(0, "06:00")
        
        # Actualizar lista
        mostrar_gestion_horarios(content_frame, admin_user)
    
    btn_frame = tk.Frame(form_frame, bg=COLORS['background'])
    btn_frame.grid(row=2, column=1, pady=10, sticky='e')
    
    crear_boton_estilo(btn_frame, "Guardar Horario", registrar_horario, 'primary', 20).pack(side='right', padx=5)
    
    # Lista de horarios existentes
    lista_frame = tk.LabelFrame(main_frame, text=" Horarios Existentes", 
                               bg=COLORS['white'], font=('Arial', 11, 'bold'), fg=COLORS['text_dark'])
    lista_frame.pack(fill='both', expand=True, padx=20, pady=10)
    
    horarios = cargar_horarios()
    
    if not horarios:
        tk.Label(lista_frame, text=" No hay horarios registrados.", 
                 font=('Arial', 11), fg=COLORS['danger'], bg=COLORS['white']).pack(pady=20)
        return
    
    # Crear tabla con Treeview
    columns = ("ID", "Ruta", "Origen → Destino", "Hora")
    tree = ttk.Treeview(lista_frame, columns=columns, show="headings", height=10)
    
    # Configurar columnas
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=100)
    
    tree.column("Ruta", width=150)
    tree.column("Origen → Destino", width=150)
    
    # Agregar scrollbar
    scrollbar = ttk.Scrollbar(lista_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    
    # Insertar datos
    for horario_id, data in horarios.items():
        ruta_data = rutas.get(data['ruta_id'], {})
        coop_nombre = cooperativas.get(ruta_data.get('cooperativa_id', ''), {}).get('nombre', 'N/A')
        ruta_info = f"{ruta_data.get('origen', 'N/A')} → {ruta_data.get('destino', 'N/A')}"
        
        tree.insert("", "end", values=(
            horario_id,
            coop_nombre,
            ruta_info,
            data['hora']
        ))
    
    # Empacar
    tree.pack(side="left", fill="both", expand=True, padx=10, pady=10)
    scrollbar.pack(side="right", fill="y", pady=10)
    
    # Botones de acción
    action_frame = tk.Frame(lista_frame, bg=COLORS['white'])
    action_frame.pack(fill='x', padx=10, pady=5)
    
    def eliminar_horario():
        seleccionado = tree.selection()
        if not seleccionado:
            messagebox.showerror("Error", "Seleccione un horario para eliminar.")
            return
        
        item = tree.item(seleccionado[0])
        horario_id = item['values'][0]
        hora = item['values'][3]
        
        if not messagebox.askyesno("Confirmar", f"¿Eliminar el horario {hora}?"):
            return
        
        horarios.pop(horario_id, None)
        guardar_horarios(horarios)
        messagebox.showinfo("Éxito", f"Horario {hora} eliminado.")
        mostrar_gestion_horarios(content_frame, admin_user)
    
    crear_boton_estilo(action_frame, "Eliminar Seleccionado", eliminar_horario, 'danger', 20).pack(side='right', padx=5)

def mostrar_reportes(content_frame, admin_user):
    """Muestra reportes y estadísticas de ventas."""
    for widget in content_frame.winfo_children():
        widget.destroy()
    
    # Crear frame principal con scrollbar
    main_container = tk.Frame(content_frame, bg=COLORS['background'])
    main_container.pack(fill='both', expand=True)
    
    # Crear canvas y scrollbar
    canvas = tk.Canvas(main_container, bg=COLORS['background'], highlightthickness=0)
    scrollbar = tk.Scrollbar(main_container, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg=COLORS['background'])
    
    # Configurar scroll
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    canvas.pack(side="left", fill="both", expand=True, padx=(0, 5))
    scrollbar.pack(side="right", fill="y")
    
  
    main_frame = crear_frame_contenedor(scrollable_frame, 10)
    
    crear_label_titulo(main_frame, "Reportes y Estadísticas", 16).pack(pady=(10, 20))
    
    # Cargar datos
    boletos = cargar_boletos()
    rutas = cargar_rutas()
    cooperativas = cargar_cooperativas()
    usuarios = cargar_usuarios()
    horarios = cargar_horarios()
    
    if not boletos:
        tk.Label(main_frame, text="No hay ventas registradas aún.", 
                 font=('Arial', 14), fg=COLORS['danger'], bg=COLORS['white']).pack(pady=50)
        
  
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        return
    
    # Calcular estadísticas
    total_boletos = len(boletos)
    ingresos_totales = sum(b['precio'] for b in boletos)
    
    # Estadísticas por cooperativa
    stats_coop = {}
    for b in boletos:
        ruta_data = rutas.get(b['ruta_id'], {})
        coop_id = ruta_data.get('cooperativa_id', 'Desconocida')
        if coop_id not in stats_coop:
            stats_coop[coop_id] = {
                'boletos': 0, 
                'ingresos': 0, 
                'nombre': cooperativas.get(coop_id, {}).get('nombre', 'Desconocida')
            }
        stats_coop[coop_id]['boletos'] += 1
        stats_coop[coop_id]['ingresos'] += b['precio']
    
    # Estadísticas por ruta
    stats_ruta = {}
    for b in boletos:
        ruta_id = b['ruta_id']
        if ruta_id not in stats_ruta:
            ruta_data = rutas.get(ruta_id, {})
            stats_ruta[ruta_id] = {
                'boletos': 0, 
                'ingresos': 0,
                'nombre': f"{ruta_data.get('origen', 'N/A')} → {ruta_data.get('destino', 'N/A')}"
            }
        stats_ruta[ruta_id]['boletos'] += 1
        stats_ruta[ruta_id]['ingresos'] += b['precio']
    
    # Resumen General
    resumen_frame = tk.LabelFrame(main_frame, text="Resumen General", 
                                 bg=COLORS['white'], font=('Arial', 11, 'bold'))
    resumen_frame.pack(fill='x', padx=20, pady=10)
    
  
    grid_frame = tk.Frame(resumen_frame, bg=COLORS['white'])
    grid_frame.pack(padx=10, pady=10)
    
    # Métricas
    metricas = [
        ("Total Boletos Vendidos:", f"{total_boletos}", 0, 0),
        ("Ingresos Totales:", f"${ingresos_totales:.2f}", 0, 1),
        ("Cooperativas Activas:", f"{len(cooperativas)}", 1, 0),
        ("Rutas Registradas:", f"{len(rutas)}", 1, 1),
        ("Usuarios Registrados:", f"{len(usuarios)}", 2, 0),
        ("Horarios Disponibles:", f"{len(horarios)}", 2, 1)
    ]
    
    for text, valor, row, col in metricas:
        frame = tk.Frame(grid_frame, bg=COLORS['background'], relief='raised', bd=1)
        frame.grid(row=row, column=col, padx=10, pady=10, sticky='nsew')
        
        tk.Label(frame, text=text, font=('Arial', 10, 'bold'), 
                fg=COLORS['text_dark'], bg=COLORS['background']).pack(pady=(10, 5))
        tk.Label(frame, text=valor, font=('Arial', 16, 'bold'), 
                fg=COLORS['primary'], bg=COLORS['background']).pack(pady=(0, 10))
    
    # Reporte por Cooperativa
    if stats_coop:
        coop_frame = tk.LabelFrame(main_frame, text="Ventas por Cooperativa", 
                                  bg=COLORS['white'], font=('Arial', 11, 'bold'))
        coop_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
      
        coop_container = tk.Frame(coop_frame, bg=COLORS['white'])
        coop_container.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Crear Treeview
        columns = ("Cooperativa", "Boletos Vendidos", "Ingresos", "% del Total")
        tree_coop = ttk.Treeview(coop_container, columns=columns, show="headings", height=6)
        
        for col in columns:
            tree_coop.heading(col, text=col)
            tree_coop.column(col, width=120)
        
        tree_coop.column("Cooperativa", width=200)
        
        
        scrollbar_coop = ttk.Scrollbar(coop_container, orient="vertical", command=tree_coop.yview)
        tree_coop.configure(yscrollcommand=scrollbar_coop.set)
        
        
        scrollbar_coop_h = ttk.Scrollbar(coop_container, orient="horizontal", command=tree_coop.xview)
        tree_coop.configure(xscrollcommand=scrollbar_coop_h.set)
        
        # Ordenar por ingresos de mayor a menor
        sorted_coops = sorted(stats_coop.items(), key=lambda x: x[1]['ingresos'], reverse=True)
        
        for coop_id, stats in sorted_coops:
            porcentaje = (stats['ingresos'] / ingresos_totales * 100) if ingresos_totales > 0 else 0
            tree_coop.insert("", "end", values=(
                stats['nombre'],
                stats['boletos'],
                f"${stats['ingresos']:.2f}",
                f"{porcentaje:.1f}%"
            ))
        
        # Empacar treeview y scrollbars
        tree_coop.grid(row=0, column=0, sticky='nsew')
        scrollbar_coop.grid(row=0, column=1, sticky='ns')
        scrollbar_coop_h.grid(row=1, column=0, sticky='ew')
        
        # Configurar grid weights
        coop_container.grid_rowconfigure(0, weight=1)
        coop_container.grid_columnconfigure(0, weight=1)
    
    # Reporte por Ruta
    if stats_ruta:
        ruta_frame = tk.LabelFrame(main_frame, text="Ventas por Ruta", 
                                  bg=COLORS['white'], font=('Arial', 11, 'bold'))
        ruta_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Contenedor para treeview
        ruta_container = tk.Frame(ruta_frame, bg=COLORS['white'])
        ruta_container.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Crear Treeview
        columns = ("Ruta", "Boletos Vendidos", "Ingresos", "Precio Promedio")
        tree_ruta = ttk.Treeview(ruta_container, columns=columns, show="headings", height=6)
        
        for col in columns:
            tree_ruta.heading(col, text=col)
            tree_ruta.column(col, width=120)
        
        tree_ruta.column("Ruta", width=200)
        
 
        scrollbar_ruta = ttk.Scrollbar(ruta_container, orient="vertical", command=tree_ruta.yview)
        tree_ruta.configure(yscrollcommand=scrollbar_ruta.set)
        
    
        scrollbar_ruta_h = ttk.Scrollbar(ruta_container, orient="horizontal", command=tree_ruta.xview)
        tree_ruta.configure(xscrollcommand=scrollbar_ruta_h.set)
        
        # Ordenar por ingresos mayor a menor
        sorted_rutas = sorted(stats_ruta.items(), key=lambda x: x[1]['ingresos'], reverse=True)
        
        for ruta_id, stats in sorted_rutas:
            precio_promedio = stats['ingresos'] / stats['boletos'] if stats['boletos'] > 0 else 0
            tree_ruta.insert("", "end", values=(
                stats['nombre'],
                stats['boletos'],
                f"${stats['ingresos']:.2f}",
                f"${precio_promedio:.2f}"
            ))
        
        # Empacar treeview y scrollbars
        tree_ruta.grid(row=0, column=0, sticky='nsew')
        scrollbar_ruta.grid(row=0, column=1, sticky='ns')
        scrollbar_ruta_h.grid(row=1, column=0, sticky='ew')
        
        # Configurar grid weights
        ruta_container.grid_rowconfigure(0, weight=1)
        ruta_container.grid_columnconfigure(0, weight=1)
    
    # Reporte Detallado de Boletos
    if boletos:
        detalle_frame = tk.LabelFrame(main_frame, text="Detalle de Boletos Vendidos", 
                                     bg=COLORS['white'], font=('Arial', 11, 'bold'))
        detalle_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Contenedor para treeview y scrollbar
        detalle_container = tk.Frame(detalle_frame, bg=COLORS['white'])
        detalle_container.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Crear Treeview con más columnas
        columns = ("ID", "Usuario", "Ruta", "Fecha Viaje", "Asiento", "Precio", "Fecha Compra")
        tree_detalle = ttk.Treeview(detalle_container, columns=columns, show="headings", height=8)
        
        # Configurar columnas
        column_widths = {
            "ID": 100, "Usuario": 120, "Ruta": 150, 
            "Fecha Viaje": 100, "Asiento": 80, "Precio": 80, "Fecha Compra": 120
        }
        
        for col in columns:
            tree_detalle.heading(col, text=col)
            tree_detalle.column(col, width=column_widths.get(col, 100))
        
        
        scrollbar_detalle = ttk.Scrollbar(detalle_container, orient="vertical", command=tree_detalle.yview)
        tree_detalle.configure(yscrollcommand=scrollbar_detalle.set)
        
        
        scrollbar_detalle_h = ttk.Scrollbar(detalle_container, orient="horizontal", command=tree_detalle.xview)
        tree_detalle.configure(xscrollcommand=scrollbar_detalle_h.set)
        
        # Insertar datos de boletos ordenados por fecha de compra descendente
        boletos_ordenados = sorted(boletos, key=lambda x: x.get('fecha_compra', ''), reverse=True)
        
        for boleto in boletos_ordenados:
            ruta_data = rutas.get(boleto.get('ruta_id', ''), {})
            ruta_info = f"{ruta_data.get('origen', 'N/A')} → {ruta_data.get('destino', 'N/A')}"
            
            tree_detalle.insert("", "end", values=(
                boleto['id'][:8] + "...",
                boleto.get('usuario', 'N/A'),
                ruta_info,
                boleto.get('fecha_viaje', 'N/A'),
                f"A{boleto.get('asiento', 'N/A')}",
                f"${boleto.get('precio', 0):.2f}",
                boleto.get('fecha_compra', 'N/A')
            ))
        
        # Empacar treeview
        tree_detalle.grid(row=0, column=0, sticky='nsew')
        scrollbar_detalle.grid(row=0, column=1, sticky='ns')
        scrollbar_detalle_h.grid(row=1, column=0, sticky='ew')
        
        # Configurar grid weights
        detalle_container.grid_rowconfigure(0, weight=1)
        detalle_container.grid_columnconfigure(0, weight=1)
    
    # Botón para exportar reportes
    export_frame = tk.Frame(main_frame, bg=COLORS['white'])
    export_frame.pack(pady=20)
    
    def exportar_reporte():
        messagebox.showinfo("Exportar", "Función de exportación en desarrollo.")
    
    crear_boton_estilo(export_frame, "Exportar Reporte", exportar_reporte, 'accent', 20).pack()
    
    # Agregar scroll con rueda del mouse
    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    canvas.bind_all("<MouseWheel>", _on_mousewheel)
    
    # Configurar resize del canvas
    def on_canvas_resize(event):
        canvas.itemconfig(1, width=event.width)
    
    canvas.bind('<Configure>', on_canvas_resize)
    

def cerrar_sesion_admin(root):
    """Cierra sesión de administrador"""
    for widget in root.winfo_children():
        widget.destroy()
    
    from src.autenticacion import mostrar_inicio
    mostrar_inicio(root)
    root.geometry("600x450")

def iniciar_sistema_admin(root, admin_logueado):
    """Sistema principal para el Administrador."""
    for widget in root.winfo_children():
        widget.destroy()
    
    crear_estilo_ventana(root, f" Panel de Administración - {admin_logueado}", "1200x700")

    root.grid_columnconfigure(0, weight=0)
    root.grid_columnconfigure(1, weight=1)
    root.grid_rowconfigure(0, weight=1)

    # Barra lateral de navegación
    nav_frame = tk.Frame(root, bg=COLORS['secondary'], width=250)
    nav_frame.grid(row=0, column=0, sticky="nsew")
    nav_frame.grid_propagate(False)

    content_frame = tk.Frame(root, bg=COLORS['background'])
    content_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
   
    tk.Label(nav_frame, text="ADMIN\nMENU", font=('Arial', 18, 'bold'), 
             fg='white', bg=COLORS['secondary']).pack(pady=(40, 20))

    # Funciones para manejar el contenido
    def cargar_contenido(func):
        for widget in content_frame.winfo_children():
            widget.destroy()
        
        if func == cerrar_sesion_admin:
            func(root)
            return
        else:
            return func(content_frame, admin_logueado)

    # Botones del menú
    opciones = [
        (" Gestión de Cooperativas", lambda: cargar_contenido(mostrar_gestion_cooperativas)),
        (" Gestión de Rutas", lambda: cargar_contenido(mostrar_gestion_rutas)),
        (" Gestión de Horarios", lambda: cargar_contenido(mostrar_gestion_horarios)),
        (" Reportes", lambda: cargar_contenido(mostrar_reportes)),
        (" Cerrar Sesión", lambda: cargar_contenido(cerrar_sesion_admin))
    ]
   
    for text, command in opciones:
        btn = crear_boton_estilo(nav_frame, text, command, 'accent', 25)
        btn.pack(fill='x', padx=15, pady=10)

    # Mostrar gestión de cooperativas por defecto
    cargar_contenido(mostrar_gestion_cooperativas)