import tkinter as tk
from tkinter import ttk, messagebox
import cogs.crud_modules as crud

class AppComercioTechMongo:
    def __init__(self, root):
        self.root = root
        self.root.title("ComercioTech - MongoDB Edition")
        self.root.geometry("800x550")
        
        # Contenedor de pestañas
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Frames para cada pestaña
        self.tab_clientes = ttk.Frame(self.notebook)
        self.tab_productos = ttk.Frame(self.notebook)
        self.tab_pedidos = ttk.Frame(self.notebook)
        
        self.notebook.add(self.tab_clientes, text="Clientes")
        self.notebook.add(self.tab_productos, text="Productos")
        self.notebook.add(self.tab_pedidos, text="Pedidos")
        
        # Renderizar vistas
        self.crear_vista_clientes()
        self.crear_vista_productos()
        self.crear_vista_pedidos()

    # --- VISTA CLIENTES ---
    def crear_vista_clientes(self):
        frame_form = ttk.LabelFrame(self.tab_clientes, text=" Registrar Cliente ")
        frame_form.pack(fill="x", padx=10, pady=5)
        frame_form.columnconfigure(1, weight=1) # <--- Agrega esta línea para que se estire
        
        ttk.Label(frame_form, text="Nombre:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.ent_cli_nombre = ttk.Entry(frame_form)
        self.ent_cli_nombre.grid(row=0, column=1, padx=5, pady=5, sticky="ew") # <--- Cambiado aquí
        
        ttk.Label(frame_form, text="Email:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.ent_cli_email = ttk.Entry(frame_form)
        self.ent_cli_email.grid(row=1, column=1, padx=5, pady=5, sticky="ew") # <--- Cambiado aquí
        
        ttk.Label(frame_form, text="Teléfono:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.ent_cli_tel = ttk.Entry(frame_form)
        self.ent_cli_tel.grid(row=2, column=1, padx=5, pady=5, sticky="ew") # <--- Cambiado aquí
        
        ttk.Button(frame_form, text="Guardar en Mongo", command=self.guardar_cliente).grid(row=3, column=0, columnspan=2, pady=10)
        
        # Tabla amplia para soportar el ObjectId largo de Mongo
        self.tabla_cli = ttk.Treeview(self.tab_clientes, columns=("ID", "Nombre", "Email", "Teléfono"), show="headings", height=8)
        self.tabla_cli.heading("ID", text="Mongo ObjectId")
        self.tabla_cli.heading("Nombre", text="Nombre")
        self.tabla_cli.heading("Email", text="Email")
        self.tabla_cli.heading("Teléfono", text="Teléfono")
        self.tabla_cli.column("ID", width=180, anchor="center")
        self.tabla_cli.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.actualizar_tabla_clientes()

    def guardar_cliente(self):
        nom = self.ent_cli_nombre.get()
        em = self.ent_cli_email.get()
        tel = self.ent_cli_tel.get()
        
        if nom and em:
            if crud.registrar_cliente(nom, em, tel):
                messagebox.showinfo("Éxito", "Cliente guardado en la base de datos distribuida.")
                self.actualizar_tabla_clientes()
                self.ent_cli_nombre.delete(0, tk.END)
                self.ent_cli_email.delete(0, tk.END)
                self.ent_cli_tel.delete(0, tk.END)
            else:
                messagebox.showerror("Error", "No se pudo guardar el cliente (Verifica conexión o email duplicado).")
        else:
            messagebox.showwarning("Campos vacíos", "Nombre y Email obligatorios.")

    def actualizar_tabla_clientes(self):
        for row in self.tabla_cli.get_children():
            self.tabla_cli.delete(row)
        for fila in crud.obtener_clientes():
            self.tabla_cli.insert("", "end", values=fila)


    # --- VISTA PRODUCTOS ---
    def crear_vista_productos(self):
        frame_form = ttk.LabelFrame(self.tab_productos, text=" Registrar Producto ")
        frame_form.pack(fill="x", padx=10, pady=5)
        frame_form.columnconfigure(1, weight=1) # <--- Agrega esto
        
        ttk.Label(frame_form, text="Nombre:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.ent_prod_nombre = ttk.Entry(frame_form)
        self.ent_prod_nombre.grid(row=0, column=1, padx=5, pady=5, sticky="ew") # <--- Cambiado
        
        ttk.Label(frame_form, text="Precio:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.ent_prod_precio = ttk.Entry(frame_form)
        self.ent_prod_precio.grid(row=1, column=1, padx=5, pady=5, sticky="ew") # <--- Cambiado
        
        ttk.Label(frame_form, text="Stock:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.ent_prod_stock = ttk.Entry(frame_form)
        self.ent_prod_stock.grid(row=2, column=1, padx=5, pady=5, sticky="ew") # <--- Cambiado
        
        ttk.Button(frame_form, text="Guardar Producto", command=self.guardar_producto).grid(row=3, column=0, columnspan=2, pady=10)
        
        self.tabla_prod = ttk.Treeview(self.tab_productos, columns=("ID", "Nombre", "Precio", "Stock"), show="headings", height=8)
        self.tabla_prod.heading("ID", text="Mongo ObjectId")
        self.tabla_prod.heading("Nombre", text="Nombre")
        self.tabla_prod.heading("Precio", text="Precio")
        self.tabla_prod.heading("Stock", text="Stock")
        self.tabla_prod.column("ID", width=180, anchor="center")
        self.tabla_prod.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.actualizar_tabla_productos()

    def guardar_producto(self):
        nom = self.ent_prod_nombre.get()
        try:
            pre = float(self.ent_prod_precio.get())
            stk = int(self.ent_prod_stock.get())
            if nom:
                if crud.registrar_producto(nom, pre, stk):
                    messagebox.showinfo("Éxito", "Producto registrado en el cluster local.")
                    self.actualizar_tabla_productos()
                    self.ent_prod_nombre.delete(0, tk.END)
                    self.ent_prod_precio.delete(0, tk.END)
                    self.ent_prod_stock.delete(0, tk.END)
            else:
                messagebox.showwarning("Atención", "El nombre es obligatorio.")
        except ValueError:
            messagebox.showerror("Error", "Formatos inválidos de precio o stock.")

    def actualizar_tabla_productos(self):
        for row in self.tabla_prod.get_children():
            self.tabla_prod.delete(row)
        for fila in crud.obtener_productos():
            self.tabla_prod.insert("", "end", values=fila)


    # --- VISTA PEDIDOS ---
    def crear_vista_pedidos(self):
        frame_form = ttk.LabelFrame(self.tab_pedidos, text=" Registrar Transacción (Pedido) ")
        frame_form.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(frame_form, text="ID Cliente (Hex):").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.ent_ped_cli = ttk.Entry(frame_form, width=30)
        self.ent_ped_cli.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        
        ttk.Label(frame_form, text="ID Producto (Hex):").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.ent_ped_prod = ttk.Entry(frame_form, width=30)
        self.ent_ped_prod.grid(row=0, column=3, padx=5, pady=5, sticky="w")
        
        ttk.Label(frame_form, text="Cantidad:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.ent_ped_cant = ttk.Entry(frame_form, width=10)
        self.ent_ped_cant.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        
        ttk.Button(frame_form, text="Generar Pedido", command=self.guardar_pedido).grid(row=1, column=2, columnspan=2, padx=5, pady=5)
        
        self.tabla_ped = ttk.Treeview(self.tab_pedidos, columns=("ID", "Cliente", "Producto", "Cantidad"), show="headings", height=8)
        self.tabla_ped.heading("ID", text="ID Pedido")
        self.tabla_ped.heading("Cliente", text="Nombre Cliente")
        self.tabla_ped.heading("Producto", text="Nombre Producto")
        self.tabla_ped.heading("Cantidad", text="Cantidad")
        self.tabla_ped.column("ID", width=180, anchor="center")
        self.tabla_ped.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.actualizar_tabla_pedidos()

    def guardar_pedido(self):
        cli_id = self.ent_ped_cli.get().strip()
        prod_id = self.ent_ped_prod.get().strip()
        try:
            cant = int(self.ent_ped_cant.get())
            if len(cli_id) != 24 or len(prod_id) != 24:
                raise ValueError("Los ObjectIds de Mongo deben tener exactamente 24 caracteres hex.")
                
            if crud.registrar_pedido(cli_id, prod_id, cant):
                messagebox.showinfo("Éxito", "Pedido enlazado exitosamente.")
                self.actualizar_tabla_pedidos()
                self.ent_ped_cli.delete(0, tk.END)
                self.ent_ped_prod.delete(0, tk.END)
                self.ent_ped_cant.delete(0, tk.END)
            else:
                messagebox.showerror("Error", "No se encontró el Cliente o el Producto con esos IDs.")
        except ValueError as ex:
            messagebox.showerror("Error", f"Entrada inválida: {ex}")

    def actualizar_tabla_pedidos(self):
        for row in self.tabla_ped.get_children():
            self.tabla_ped.delete(row)
        for fila in crud.obtener_pedidos():
            self.tabla_ped.insert("", "end", values=fila)

if __name__ == "__main__":
    root = tk.Tk()
    app = AppComercioTechMongo(root)
    root.mainloop()