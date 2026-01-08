# Módulo para manejar usuarios (datos en memoria)
usuarios = [
    {"usuario": "admin", "contraseña": "0000", "nombre": "Administrador"},
    {"usuario": "erazo", "contraseña": "123", "nombre": "Erazo"},
    {"usuario": "diocles", "contraseña": "123", "nombre": "Diocles"},
    {"usuario": "adonis", "contraseña": "123", "nombre": "Adonis"},
    {"usuario": "jesus", "contraseña": "123", "nombre": "Jesus"},
    {"usuario": "yosbell", "contraseña": "123", "nombre": "Yosbell"},
]

def validar_usuario(usuario, clave):
    """Valida si el usuario y contraseña existen. Retorna el dict del usuario o None."""
    for u in usuarios:
        if u["usuario"] == usuario and u["contraseña"] == clave:
            return u
    return None

def agregar_usuario(nombre, usuario, clave):
    """Agrega un nuevo usuario si no existe."""
    for u in usuarios:
        if u["usuario"] == usuario:
            return False  # Ya existe
    usuarios.append({"nombre": nombre, "usuario": usuario, "contraseña": clave})
    return True

def obtener_todos_usuarios():
    """Retorna la lista de usuarios."""
    return usuarios