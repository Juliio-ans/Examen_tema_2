import tkinter as tk
from tkinter import messagebox, ttk
import requests
import random

class link:
    def __init__(self):
        self.__url = "https://671d4a4d09103098807cbfb3.mockapi.io/usuarios"

    def obtener_datos(self):
        try:
            response = requests.get(self.__url)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            messagebox.showerror("Error", f"Error al obtener datos: {e}")
            return []

class sus:
    def __init__(self, root):
        self.__root = root
        self.__root.title("hangar")
        self.__root.geometry("1000x500")
        self.__root.resizable(False, False)

        self.__LINK = link()
        self.__crear_widgets()
        self.__mostrar_datos()

    def __crear_widgets(self):
        self.__label = tk.Label(self.__root, text="Registros de un hangar:")
        self.__label.pack(pady=10)

        self.__tabla = ttk.Treeview(self.__root, columns=("No de Serie", "Piloto", "En Servicio", "Modelo", "Horas de Vuelo"), show='headings')
        for col in self.__tabla["columns"]:
            self.__tabla.heading(col, text=col)
            self.__tabla.column(col, anchor="center")

        self.__tabla.pack(pady=10, fill=tk.BOTH, expand=True)
        self.__tabla.bind("<Double-1>", self.__mostrar_seleccionado)

        self.__entrada_id = tk.Entry(self.__root)
        self.__entrada_id.pack(pady=5)

        self.__boton_buscar = tk.Button(self.__root, text="Buscar por No de Serie", command=self.__buscar_por_id)
        self.__boton_buscar.pack(pady=5)

        self.__boton_todos = tk.Button(self.__root, text="Mostrar Todos", command=self.__mostrar_datos)
        self.__boton_todos.pack_forget()

        self.__boton_random = tk.Button(self.__root, text="Mostrar Dato Aleatorio", command=self.__mostrar_random)
        self.__boton_random.pack(pady=5)

    def __mostrar_datos(self):
        for item in self.__tabla.get_children():
            self.__tabla.delete(item)

        for registro in self.__LINK.obtener_datos():
            # Incluye el valor de "piloto" en la tabla
            self.__tabla.insert("", tk.END, values=(registro['no_serie'], registro['piloto'], registro['en_servicio'], registro['modelo'], registro['horas_de_vuelo']))

        self.__boton_todos.pack_forget()

    def __buscar_por_id(self):
        id_buscar = self.__entrada_id.get()
        if not id_buscar:
            messagebox.showwarning("Advertencia", "Por favor ingresa un No de Serie.")
            return
        for item in self.__tabla.get_children():
            self.__tabla.delete(item)
        datos = self.__LINK.obtener_datos()
        encontrado = False
        for registro in datos:
            if registro['no_serie'] == id_buscar:
                self.__tabla.insert("", tk.END, values=(registro['no_serie'], registro['piloto'], registro['en_servicio'], registro['modelo'], registro['horas_de_vuelo']))
                encontrado = True
                break

        if encontrado:
            self.__boton_todos.pack(pady=5)
        else:
            messagebox.showinfo("Resultado", "Registro no encontrado.")

    def __mostrar_random(self):
        datos = self.__LINK.obtener_datos()
        if not datos:
            messagebox.showwarning("Advertencia", "No hay registros disponibles.")
            return

        registro_random = random.choice(datos)
        mensaje = (f"No de Serie: {registro_random['no_serie']}\n"
                   f"Piloto: {registro_random['piloto']}\n"
                   f"En Servicio: {registro_random['en_servicio']}\n"
                   f"Modelo: {registro_random['modelo']}\n"
                   f"Horas de Vuelo: {registro_random['horas_de_vuelo']}")
        messagebox.showinfo("Registro Aleatorio", mensaje)

    def __mostrar_seleccionado(self, event=None):
        selecion_item = self.__tabla.selection()
        if selecion_item:
            item = self.__tabla.item(selecion_item)
            datos = item['values']
            mensaje = (f"No de Serie: {datos[0]}\n"
                       f"Piloto: {datos[1]}\n"
                       f"En Servicio: {datos[2]}\n"
                       f"Modelo: {datos[3]}\n"
                       f"Horas de Vuelo: {datos[4]}")
            messagebox.showinfo("Registro Seleccionado", mensaje)
        else:
            messagebox.showwarning("Advertencia", "Por favor selecciona un registro.")
