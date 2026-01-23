"""
Módulo de manejo de archivos y datos JSON
Incluye funciones de carga/guardado y inicialización de datos
"""

import os
import json
from datetime import datetime
from src.configuracion import *

def cargar_json(archivo, default=None):
    """Carga datos desde un archivo JSON"""
    if os.path.exists(archivo):
        try:
            with open(archivo, "r", encoding='utf-8') as f:
                return json.load(f)
        except:
            return default if default else {}
    return default if default else {}

def guardar_json(archivo, datos):
    """Guarda datos en un archivo JSON"""
    with open(archivo, "w", encoding='utf-8') as f:
        json.dump(datos, f, ensure_ascii=False, indent=2)

def cargar_usuarios():
    return cargar_json(USERS_FILE)

def guardar_usuarios(usuarios):
    guardar_json(USERS_FILE, usuarios)

def cargar_administradores():
    default_admin = {"admin": "terminal"}
    return cargar_json(ADMINS_FILE, default_admin)

def guardar_administradores(admins):
    guardar_json(ADMINS_FILE, admins)

def cargar_cooperativas():
    return cargar_json(COOPERATIVAS_FILE)

def guardar_cooperativas(cooperativas):
    guardar_json(COOPERATIVAS_FILE, cooperativas)

def cargar_rutas():
    return cargar_json(RUTAS_FILE)

def guardar_rutas(rutas):
    guardar_json(RUTAS_FILE, rutas)

def cargar_boletos():
    return cargar_json(BOLETOS_FILE, [])

def guardar_boletos(boletos):
    guardar_json(BOLETOS_FILE, boletos)

def cargar_horarios():
    return cargar_json(HORARIOS_FILE)

def guardar_horarios(horarios):
    guardar_json(HORARIOS_FILE, horarios)

def cargar_boletos_papelera():
    return cargar_json(BOLETOS_PAPELERA_FILE, [])

def guardar_boletos_papelera(boletos_papelera):
    guardar_json(BOLETOS_PAPELERA_FILE, boletos_papelera)

def inicializar_datos_prueba():
    """Crea datos de prueba si no existen"""
    # Crear cooperativa de prueba
    cooperativas = cargar_cooperativas()
    if not os.path.exists(BOLETOS_PAPELERA_FILE):
        guardar_boletos_papelera([])
    if not cooperativas:
        coop_id = "coop_001"
        cooperativas[coop_id] = {
            "id": coop_id,
            "nombre": "Transportes Quito Express",
            "ruc": "1234567890001",
            "telefono": "02-2345678",
            "email": "info@quitoexpress.com",
            "direccion": "Av. Amazonas y Naciones Unidas",
            "representante": "Juan Pérez",
            "numero_buses": 25,
            "fecha_creacion": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "creado_por": "sistema",
            "estado": "activa"
        }
        guardar_cooperativas(cooperativas)
    
    # Crear ruta de prueba
    rutas = cargar_rutas()
    if not rutas:
        ruta_id = "ruta_001"
        rutas[ruta_id] = {
            "id": ruta_id,
            "cooperativa_id": "coop_001",
            "origen": "Quito",
            "destino": "Cuenca",
            "precio": 15.50,
            "fecha_creacion": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "creado_por": "sistema",
            "estado": "activa"
        }
        guardar_rutas(rutas)
    
    # Crear horarios de prueba
    horarios = cargar_horarios()
    if not horarios:
        horarios_lista = [
            {"id": "h001", "ruta_id": "ruta_001", "hora": "06:00"},
            {"id": "h002", "ruta_id": "ruta_001", "hora": "10:00"},
            {"id": "h003", "ruta_id": "ruta_001", "hora": "14:00"},
            {"id": "h004", "ruta_id": "ruta_001", "hora": "18:00"}
        ]
        
        for h in horarios_lista:
            horarios[h["id"]] = h
        
        guardar_horarios(horarios)