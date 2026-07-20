import tkinter as tk
from tkinter import ttk, messagebox
import sys

# Importamos la conexión para validar
from cogs.conexion import conectar_db

# Importamos las vistas modulares
from vistas.vista_clientes import VistaClientes
from vistas.vista_productos import VistaProductos
from vistas.vista_pedidos import VistaPedidos

def iniciar_aplicacion():
    # 1. PRUEBA DE CONEXIÓN AL ARRANCAR
    db = conectar_db()
    if db is None:
        # Si falla, creamos una ventana invisible solo para mostrar el error gráfico
        root_oculto = tk.Tk()
        root_oculto.withdraw() 
        messagebox.showerror("Error Crítico", "No se pudo conectar a la base de datos MongoDB.\nPor favor, encienda la máquina virtual y verifique la red.")
        sys.exit() # Cerramos el programa inmediatamente

    # 2. INICIO DE LA APLICACIÓN NORMAL
    root = tk.Tk()
    root.title("ComercioTech - MongoDB (Entorno Producción)")
    root.geometry("900x650")
    
    # Contenedor de pestañas
    notebook = ttk.Notebook(root)
    notebook.pack(fill="both", expand=True, padx=10, pady=10)
    
    # Frames para cada pestaña
    tab_cli = ttk.Frame(notebook)
    tab_prod = ttk.Frame(notebook)
    tab_ped = ttk.Frame(notebook)
    
    notebook.add(tab_cli, text="Clientes")
    notebook.add(tab_prod, text="Productos")
    notebook.add(tab_ped, text="Pedidos")
    
    # Cargar las vistas modulares en cada pestaña
    VistaClientes(tab_cli)
    VistaProductos(tab_prod)
    VistaPedidos(tab_ped)
    
    root.mainloop()

if __name__ == "__main__":
    iniciar_aplicacion()