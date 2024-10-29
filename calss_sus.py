import tkinter as tk
from tkinter import messagebox, ttk
from link import link

class sus:
    def __init__(self, root):
        self.__root = root
        self.__root.title("Hangar")
        self.__root.geometry("1000x500")
        self.__root.resizable(False, False)

        self.__LINK = link()
        self.__crear_widgets()
        self.__mostrar_datos()

    def __crear_widgets(self):
        self.__label = tk.Label(self.__root, text="Registros de aeronaves en un hangar:")
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

    def __mostrar_datos(self):
        for item in self.__tabla.get_children():
            self.__tabla.delete(item)

        for registro in self.__LINK.obtener_datos():
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
