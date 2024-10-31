import tkinter as tk
from calss_sus import sus

if __name__ == "__main__":#sive para ver si el archivo esta ejecutandose como principal
    root = tk.Tk() #instancia de la clase
    app = sus(root)#llama a la cales y la inicia
    root.mainloop()
