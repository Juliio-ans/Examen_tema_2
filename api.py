#aparatado de conexion con la api
import requests
from tkinter import messagebox

class link:
    def __init__(self):
        self.__url = "https://671d4a4d09103098807cbfb3.mockapi.io/usuarios"

    def obtener_datos(self):
        try:
            response = requests.get(self.__url)#realiza la solicitud a la pi
            response.raise_for_status()#inspeciona que no aiga errores
            return response.json()
        except requests.RequestException as e:
            messagebox.showerror("Error", f"Error al obtener datos: {e}")
            return []
