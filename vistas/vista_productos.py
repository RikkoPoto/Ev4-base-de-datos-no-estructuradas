import tkinter as tk
from tkinter import ttk, messagebox
import cogs.crud as crud

class VistaProductos:
    def __init__(self, parent):
        self.frame = parent
        self.datos_memoria = []
        self.crear_interfaz()

    def crear_interfaz(self):
        # BARRA BÚSQUEDA
        frame_busqueda = ttk.Frame(self.frame)
        frame_busqueda.pack(fill="x", padx=10, pady=5)
        ttk.Label(frame_busqueda, text="🔎 Buscar Producto:").pack(side="left", padx=5)
        self.ent_buscar = ttk.Entry(frame_busqueda, width=40)
        self.ent_buscar.pack(side="left", padx=5)
        self.ent_buscar.bind("<KeyRelease>", self.filtrar_tabla)

        # FORMULARIO
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
            
        self.entries["Código:"].insert(0, "Auto-generado")
        self.entries["Código:"].config(state="readonly")
            
        # BOTONES
        frame_btns = ttk.Frame(frame_form)
        frame_btns.grid(row=4, column=0, columnspan=2, pady=10)
        ttk.Button(frame_btns, text="Crear", command=self.crear).pack(side="left", padx=5)
        ttk.Button(frame_btns, text="Modificar", command=self.modificar).pack(side="left", padx=5)
        tk.Button(frame_btns, text="Eliminar", command=self.eliminar, bg="#d9534f", fg="white", relief="flat", padx=10, pady=2, cursor="hand2").pack(side="left", padx=5)
        ttk.Button(frame_btns, text="Limpiar", command=self.limpiar).pack(side="left", padx=5)
        ttk.Button(frame_btns, text="Refrescar Tabla", command=self.actualizar_tabla).pack(side="left", padx=5)
        
        # TABLA CON ORDENAMIENTO
        self.tabla = ttk.Treeview(self.frame, columns=("Codigo", "Nombre", "Precio", "Stock"), show="headings", height=8)
        
        self.tabla.heading("Codigo", text="Código", command=lambda: self.ordenar_columna("Codigo", False))
        self.tabla.heading("Nombre", text="Nombre", command=lambda: self.ordenar_columna("Nombre", False))
        self.tabla.heading("Precio", text="Precio ($)", command=lambda: self.ordenar_columna("Precio", False))
        self.tabla.heading("Stock", text="Stock", command=lambda: self.ordenar_columna("Stock", False))
        
        self.tabla.column("Codigo", width=100, anchor="center")
        self.tabla.column("Nombre", width=300, anchor="w")
        self.tabla.column("Precio", width=100, anchor="center")
        self.tabla.column("Stock", width=80, anchor="center")
        
        self.tabla.pack(fill="both", expand=True, padx=10, pady=5)
        self.tabla.bind("<ButtonRelease-1>", self.seleccionar_fila)
        self.actualizar_tabla()

    def filtrar_tabla(self, event):
        texto = self.ent_buscar.get().lower()
        for row in self.tabla.get_children(): self.tabla.delete(row)
        for fila in self.datos_memoria:
            if any(texto in str(item).lower() for item in fila):
                self.tabla.insert("", "end", values=fila)

    def ordenar_columna(self, col, reverso):
        l = [(self.tabla.set(k, col), k) for k in self.tabla.get_children('')]
        try:
            # Limpia los símbolos "$" para poder ordenar el precio matemáticamente
            l.sort(key=lambda t: float(str(t[0]).replace('$', '').replace(',', '')), reverse=reverso)
        except ValueError:
            l.sort(reverse=reverso)
        
        for index, (val, k) in enumerate(l):
            self.tabla.move(k, '', index)
        self.tabla.heading(col, command=lambda: self.ordenar_columna(col, not reverso))

    def seleccionar_fila(self, event):
        seleccion = self.tabla.selection()
        if seleccion:
            cod = self.tabla.item(seleccion[0], "values")[0]
            prod = crud.obtener_producto_por_codigo(cod)
            if prod:
                self.limpiar()
                self.entries["Código:"].config(state="normal")
                self.entries["Código:"].delete(0, tk.END)
                self.entries["Código:"].insert(0, prod["codigo"])
                self.entries["Código:"].config(state="readonly")
                
                self.entries["Nombre:"].insert(0, prod["nombre"])
                self.entries["Precio:"].insert(0, prod["precio"])
                self.entries["Stock:"].insert(0, prod["stock"])

    def crear(self):
        if self.entries["Código:"].get() != "Auto-generado": return messagebox.showwarning("Denegado", "Limpie campos primero.")
        
        # VALIDACIÓN N°9: Campos vacíos
        if not all([self.entries["Nombre:"].get().strip(), self.entries["Precio:"].get().strip(), self.entries["Stock:"].get().strip()]):
            return messagebox.showwarning("Campos Vacíos", "Por favor, complete todos los campos del producto. No se permiten datos vacíos.")

        try:
            if crud.registrar_producto(self.entries["Nombre:"].get(), int(self.entries["Precio:"].get()), int(self.entries["Stock:"].get())):
                self.limpiar(); self.actualizar_tabla()
        except ValueError: messagebox.showerror("Error", "Precio y Stock deben ser numéricos.")

    def modificar(self):
        # VALIDACIÓN N°9: Campos vacíos
        if not all([self.entries["Nombre:"].get().strip(), self.entries["Precio:"].get().strip(), self.entries["Stock:"].get().strip()]):
            return messagebox.showwarning("Campos Vacíos", "Por favor, complete todos los campos del producto. No se permiten datos vacíos.")

        try:
            self.entries["Código:"].config(state="normal"); c = self.entries["Código:"].get(); self.entries["Código:"].config(state="readonly")
            if crud.actualizar_producto(c, self.entries["Nombre:"].get(), int(self.entries["Precio:"].get()), int(self.entries["Stock:"].get())):
                self.limpiar(); self.actualizar_tabla()
        except ValueError: messagebox.showerror("Error", "Precio y Stock deben ser numéricos.")

    def eliminar(self):
        self.entries["Código:"].config(state="normal")
        c = self.entries["Código:"].get().strip()
        self.entries["Código:"].config(state="readonly")
        
        if c != "Auto-generado" and messagebox.askyesno("Confirmar", f"¿Eliminar el producto {c}?"):
            # Recibimos el estado y el mensaje
            exito, mensaje = crud.eliminar_producto(c)
            
            if exito:
                messagebox.showinfo("Éxito", mensaje)
                self.limpiar()
                self.actualizar_tabla()
            else:
                # Si falla por integridad referencial, lanzamos el error
                messagebox.showerror("Acción Denegada", mensaje)

    def limpiar(self):
        self.entries["Código:"].config(state="normal")
        for ent in self.entries.values(): ent.delete(0, tk.END)
        self.entries["Código:"].insert(0, "Auto-generado")
        self.entries["Código:"].config(state="readonly")
        self.ent_buscar.delete(0, tk.END)
        
        # Quitar la selección azul de la tabla
        for item in self.tabla.selection():
            self.tabla.selection_remove(item)
            
        self.actualizar_tabla()

    def actualizar_tabla(self):
        for row in self.tabla.get_children(): self.tabla.delete(row)
        self.datos_memoria = crud.obtener_productos()
        for f in self.datos_memoria: self.tabla.insert("", "end", values=f)