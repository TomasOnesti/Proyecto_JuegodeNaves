import json
import os
#Base de datos: Insert score and username
class Ranking:
    def __init__(self, archivo="ranking_local.json"):
        self.archivo = archivo
        if not os.path.exists(self.archivo):
            with open(self.archivo, 'w') as f:
                json.dump([], f)
                
    def insertar(self, nombre, puntaje):
        with open(self.archivo, 'r') as f:
            datos = json.load(f)

        datos.append({"usuario": nombre, "puntaje": puntaje})

        with open(self.archivo, 'w') as f:
            json.dump(datos, f, indent=4)