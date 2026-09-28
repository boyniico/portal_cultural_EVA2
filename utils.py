import json
from django.conf import settings

def load_json_app(name_file):
    """
    Construye la ruta y lee un archivo JSON ubicado dentro de 
    la carpeta 'data' de cualquier aplicación.
    """
    json_path = settings.BASE_DIR / 'data' / name_file
    
    with open(json_path, 'r', encoding='utf-8') as file:
        return json.load(file)