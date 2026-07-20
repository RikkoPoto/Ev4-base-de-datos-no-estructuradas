import tkinter as tk
from tkinter import ttk, messagebox
import cogs.crud as crud

class VistaProductos:
    def __init__(self, parent):
        self.frame = parent
        self.crear_interfaz()

    def crear_interfaz(self):
        frame_form = ttk.LabelFrame(self.frame, text=" Gestión de Productos ")
        frame_form.pack(fill="x", padx=10, pady=5)
        frame_form.columnconfigure(1, weight=1)
        
        campos = ["Código:", "Nombre:", "Precio:", "Stock:"]
        self.entries = {}
        for i, campo in enumerate(campos):
            ttk.Label(frame_form, text=campo).grid(row=i, column=0, padx=5, pady=5, sticky="w")
            ent = ttk.Entry(frame_form)
            ent.grid(row=i, column=1, padx=5, pady=5, sticky="ew")
            self.entries[campo] = ent
            
        frame_btns = ttk.Frame(frame_form)
        frame_btns.grid(row=4, column=0, columnspan=2, pady=10)
        ttk.Button(frame_btns, text="Crear", command=self.crear).pack(side="left", padx=5)
        ttk.Button(frame_btns, text="Modificar", command=self.modificar).pack(side="left", padx=5)
        ttk.Button(frame_btns, text="Eliminar", command=self.eliminar).pack(side="left", padx=5)
        ttk.Button(frame_btns, text="Limpiar", command=self.limpiar).pack(side="left", padx=5)
        
        self.tabla = ttk.Treeview(self.frame, columns=("Codigo", "Nombre", "Precio", "Stock"), show="headings", height=8)
        for col in self.tabla["columns"]: self.tabla.heading(col, text=col)
        self.tabla.pack(fill="both", expand=True, padx=10, pady=5)
        self.tabla.bind("<ButtonRelease-1>", self.seleccionar_fila)
        self.actualizar_tabla()

    def seleccionar_fila(self, event):
        seleccion = self.tabla.selection()
        if seleccion:
            cod = self.tabla.item(seleccion[0], "values")[0]
            prod = crud.obtener_producto_por_codigo(cod)
            if prod:
                self.limpiar()
                self.entries["Código:"].insert(0, prod["codigo"])
                self.entries["Código:"].config(state="readonly")
                self.entries["Nombre:"].insert(0, prod["nombre"])
                self.entries["Precio:"].insert(0, prod["precio"])
                self.entries["Stock:"].insert(0, prod["stock"])

    def crear(self):
        try:
            if crud.registrar_producto(self.entries["Código:"].get(), self.entries["Nombre:"].get(), int(self.entries["Precio:"].get()), int(self.entries["Stock:"].get())):
                self.limpiar()
                self.actualizar_tabla()
            else: messagebox.showerror("Error", "Código duplicado.")
        except ValueError: messagebox.showerror("Error", "Precio y Stock deben ser numéricos.")

    def modificar(self):
        try:
            if crud.actualizar_producto(self.entries["Código:"].get(), self.entries["Nombre:"].get(), int(self.entries["Precio:"].get()), int(self.entries["Stock:"].get())):
                self.limpiar()
                self.actualizar_tabla()
        except ValueError: messagebox.showerror("Error", "Valores numéricos inválidos.")

    def eliminar(self):
        cod = self.entries["Código:"].get()
        if cod and messagebox.askyesno("Confirmar", f"¿Eliminar {cod}?"):
            crud.eliminar_producto(cod)
            self.limpiar()
            self.actualizar_tabla()

    def limpiar(self):
        self.entries["Código:"].config(state="normal")
        for ent in self.entries.values(): ent.delete(0, tk.END)

    def actualizar_tabla(self):
        for row in self.tabla.get_children(): self.tabla.delete(row)
        for f in crud.obtener_productos(): self.tabla.insert("", "end", values=f)