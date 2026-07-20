import tkinter as tk
from tkinter import ttk, messagebox
import cogs.crud as crud

class VistaPedidos:
    def __init__(self, parent):
        self.frame = parent
        self.id_seleccionado = None
        self.crear_interfaz()

    def crear_interfaz(self):
        frame_form = ttk.LabelFrame(self.frame, text=" Generar Nuevo Pedido ")
        frame_form.pack(fill="x", padx=10, pady=5)
        for i in range(4): frame_form.columnconfigure(i, weight=1)
        
        ttk.Label(frame_form, text="Cód. Cliente:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.ent_cli = ttk.Entry(frame_form)
        self.ent_cli.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        
        ttk.Label(frame_form, text="Cód. Producto:").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.ent_prod = ttk.Entry(frame_form)
        self.ent_prod.grid(row=0, column=3, padx=5, pady=5, sticky="ew")
        
        ttk.Label(frame_form, text="Cantidad:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.ent_cant = ttk.Entry(frame_form)
        self.ent_cant.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        
        frame_btns = ttk.Frame(frame_form)
        frame_btns.grid(row=2, column=0, columnspan=4, pady=10)
        ttk.Button(frame_btns, text="Crear Pedido", command=self.crear).pack(side="left", padx=5)
        ttk.Button(frame_btns, text="Eliminar Pedido", command=self.eliminar).pack(side="left", padx=5)
        
        self.tabla = ttk.Treeview(self.frame, columns=("ID", "CodCli", "Cliente", "CodProd", "Producto", "Cant"), show="headings", height=8)
        for col in self.tabla["columns"]: self.tabla.heading(col, text=col)
        self.tabla.column("ID", width=180) # Ocultar un poco el ObjectId
        self.tabla.pack(fill="both", expand=True, padx=10, pady=5)
        self.tabla.bind("<ButtonRelease-1>", self.seleccionar_fila)
        
        self.actualizar_tabla()

    def seleccionar_fila(self, event):
        seleccion = self.tabla.selection()
        if seleccion:
            valores = self.tabla.item(seleccion[0], "values")
            self.id_seleccionado = valores[0] # Guardamos el _id real para poder borrar
            self.ent_cli.delete(0, tk.END)
            self.ent_cli.insert(0, valores[1])
            self.ent_prod.delete(0, tk.END)
            self.ent_prod.insert(0, valores[3])
            self.ent_cant.delete(0, tk.END)
            self.ent_cant.insert(0, valores[5])

    def crear(self):
        try:
            if crud.registrar_pedido(self.ent_cli.get(), self.ent_prod.get(), int(self.ent_cant.get())):
                self.actualizar_tabla()
            else: messagebox.showerror("Error", "Cliente o Producto no encontrado.")
        except ValueError: messagebox.showerror("Error", "Cantidad inválida.")

    def eliminar(self):
        if self.id_seleccionado:
            # Pedimos confirmación mostrando el número del pedido
            if messagebox.askyesno("Confirmar", f"¿Estás seguro de eliminar el pedido N° {self.id_seleccionado}?"):
                
                # Ejecutamos la función en la base de datos
                if crud.eliminar_pedido(self.id_seleccionado):
                    messagebox.showinfo("Éxito", "Pedido eliminado correctamente.")
                    self.id_seleccionado = None
                    self.ent_cli.delete(0, tk.END)
                    self.ent_prod.delete(0, tk.END)
                    self.ent_cant.delete(0, tk.END)
                    self.actualizar_tabla()
                else:
                    messagebox.showerror("Error", "No se encontró el pedido para eliminar. ¿Quizás es un registro antiguo sin número?")
        else:
            messagebox.showwarning("Atención", "Por favor, selecciona un pedido de la tabla primero.")

    def actualizar_tabla(self):
        for row in self.tabla.get_children(): self.tabla.delete(row)
        for f in crud.obtener_pedidos(): self.tabla.insert("", "end", values=f)