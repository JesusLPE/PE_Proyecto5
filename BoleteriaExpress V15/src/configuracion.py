"""
Configuración del sistema - Constantes y configuraciones
"""

# Ciudades principales de Ecuador
CIUDADES_ECUADOR = [
    "Quito", "Guayaquil", "Cuenca", "Santo Domingo", "Machala", 
    "Manta", "Portoviejo", "Loja", "Ambato", 
]

# Colores del tema (SOLO ROJO, BLANCO Y TONOS MÁS BAJOS)
COLORS = {
    'primary': '#9B0000',    # Rojo Oscuro/Borgoña 
    'secondary': '#E32636',  # Rojo Brillante
    'accent': '#CC5500',     # Rojo Ladrillo/Cobre 
    'success': '#9B0000',    # Rojo Oscuro 
    'danger': '#E32636',     # Rojo Brillante
    'background': '#F5F5F5', # Blanco roto 
    'white': '#FFFFFF',      # Blanco
    'text_dark': '#2C3E50',  # Azul oscuro 
    'text_light': '#7F8C8D', # Gris 
    'available': "#16E32A",  # Rojo Oscuro (Asiento Disponible)
    'sold': '#E32636',       # Rojo Brillante (Asiento Vendido/Ocupado)
    'selected': '#CC5500'    # Rojo Ladrillo/Cobre (Asiento Seleccionado)
}

# Nombres de archivos
USERS_FILE = "usuarios.json"
ADMINS_FILE = "administradores.json"
COOPERATIVAS_FILE = "cooperativas.json"
RUTAS_FILE = "rutas.json"
BOLETOS_FILE = "boletos.json"
HORARIOS_FILE = "horarios.json"
BOLETOS_PAPELERA_FILE = "boletos_papelera.json"