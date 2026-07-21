import tkinter as tk
from tkinter import ttk, messagebox
import sys

# Importamos la conexión para validar
from cogs.conexion import conectar_db

# Importamos las vistas modulares
from vistas.vista_clientes import VistaClientes
from vistas.vista_productos import VistaProductos
from vistas.vista_pedidos import VistaPedidos

def aplicar_estilo_moderno(root):
    # 1. Color de fondo general de la ventana
    root.configure(bg="#F3F4F6")
    
    style = ttk.Style()
    # 2. Cambiamos el tema de Windows al tema 'clam', que permite colorear todo
    style.theme_use("clam")
    
    # --- PALETA DE COLORES ---
    BG_FONDO = "#F3F4F6"       # Gris muy claro para el fondo
    BG_PANEL = "#FFFFFF"       # Blanco puro para los formularios
    COLOR_PRIMARIO = "#2563EB" # Azul moderno (botones y selecciones)
    COLOR_HOVER = "#1D4ED8"    # Azul más oscuro al pasar el mouse
    TEXTO_OSCURO = "#1F2937"   # Gris casi negro para leer mejor
    BORDE = "#D1D5DB"          # Gris claro para los bordes

    # --- CONFIGURACIÓN GENERAL ---
    style.configure(".", background=BG_FONDO, foreground=TEXTO_OSCURO, font=("Segoe UI", 10))
    
    # --- PESTAÑAS (Notebook) ---
    style.configure("TNotebook", background=BG_FONDO, borderwidth=0)
    style.configure("TNotebook.Tab", background="#E5E7EB", padding=[15, 8], font=("Segoe UI", 10, "bold"), borderwidth=0)
    # Al seleccionar una pestaña, se vuelve azul
    style.map("TNotebook.Tab", 
              background=[("selected", COLOR_PRIMARIO)], 
              foreground=[("selected", "white")])
    
    # --- PANELES Y FORMULARIOS (Frames) ---
    style.configure("TFrame", background=BG_FONDO)
    style.configure("TLabelframe", background=BG_PANEL, bordercolor=BORDE, borderwidth=1)
    style.configure("TLabelframe.Label", background=BG_PANEL, foreground=COLOR_PRIMARIO, font=("Segoe UI", 11, "bold"))
    
    # --- TEXTOS Y CAMPOS DE ENTRADA ---
    style.configure("TLabel", background=BG_PANEL, foreground=TEXTO_OSCURO)
    style.configure("TEntry", fieldbackground="#F9FAFB", borderwidth=1, bordercolor=BORDE, padding=5)
    
    # --- BOTONES PRINCIPALES ---
    style.configure("TButton", background=COLOR_PRIMARIO, foreground="white", borderwidth=0, padding=6, font=("Segoe UI", 10, "bold"))
    style.map("TButton", background=[("active", COLOR_HOVER)]) # Efecto al pasar el mouse
    
    # --- TABLAS (Treeview) ---
    style.configure("Treeview", 
                    background=BG_PANEL, 
                    fieldbackground=BG_PANEL, 
                    foreground=TEXTO_OSCURO, 
                    rowheight=30, # Filas más altas para que respire el texto
                    borderwidth=0)
    
    style.configure("Treeview.Heading", 
                    background="#F9FAFB", 
                    foreground=TEXTO_OSCURO, 
                    font=("Segoe UI", 10, "bold"), 
                    borderwidth=1, 
                    bordercolor=BORDE)
                    
    style.map("Treeview.Heading", background=[("active", "#E5E7EB")])
    style.map("Treeview", 
              background=[("selected", COLOR_PRIMARIO)], 
              foreground=[("selected", "white")])


def iniciar_aplicacion():
    # 1. PRUEBA DE CONEXIÓN AL ARRANCAR
    db = conectar_db()
    if db is None:
        root_oculto = tk.Tk()
        root_oculto.withdraw() 
        messagebox.showerror("Error Crítico", "No se pudo conectar a MongoDB.\nPor favor, encienda la máquina virtual y verifique la red.")
        sys.exit()

    # 2. INICIO DE LA APLICACIÓN NORMAL
    root = tk.Tk()
    root.title("ComercioTech - MongoDB (v0.8)")
    root.geometry("950x700") # Un poco más grande para lucir el diseño
    
    # --- APLICAR NUESTRO ESTILO ---
    aplicar_estilo_moderno(root)
    
    # Contenedor de pestañas
    notebook = ttk.Notebook(root)
    notebook.pack(fill="both", expand=True, padx=15, pady=15)
    
    # Frames para cada pestaña
    tab_cli = ttk.Frame(notebook)
    tab_prod = ttk.Frame(notebook)
    tab_ped = ttk.Frame(notebook)
    
    notebook.add(tab_cli, text="👥 Gestión de Clientes")
    notebook.add(tab_prod, text="📦 Inventario y Productos")
    notebook.add(tab_ped, text="🛒 Transacciones y Pedidos")
    
    # Cargar las vistas modulares en cada pestaña
    VistaClientes(tab_cli)
    VistaProductos(tab_prod)
    VistaPedidos(tab_ped)
    
    root.mainloop()

if __name__ == "__main__":
    iniciar_aplicacion()