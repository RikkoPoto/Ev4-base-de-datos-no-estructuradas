import tkinter as tk
from tkinter import ttk, messagebox
import cogs.crud as crud

class VistaPedidos:
    def __init__(self, parent):
        self.frame = parent
        self.id_seleccionado = None
        self.datos_memoria = [] # Memoria para el buscador
        self.crear_interfaz()

    def crear_interfaz(self):
        # 1. BARRA DE BÚSQUEDA
        frame_busqueda = ttk.Frame(self.frame)
        frame_busqueda.pack(fill="x", padx=10, pady=5)
        ttk.Label(frame_busqueda, text="🔎 Buscar Pedido (Cualquier campo):").pack(side="left", padx=5)
        self.ent_buscar = ttk.Entry(frame_busqueda, width=40)
        self.ent_buscar.pack(side="left", padx=5)
        self.ent_buscar.bind("<KeyRelease>", self.filtrar_tabla) # Filtra en tiempo real

        # 2. FORMULARIO
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
        
        # 3. BOTONES
        frame_btns = ttk.Frame(frame_form)
        frame_btns.grid(row=2, column=0, columnspan=4, pady=10)
        ttk.Button(frame_btns, text="Crear Pedido", command=self.crear).pack(side="left", padx=5)
        tk.Button(frame_btns, text="Eliminar Pedido", command=self.eliminar, bg="#d9534f", fg="white", relief="flat", padx=10, pady=2, cursor="hand2").pack(side="left", padx=5)
        ttk.Button(frame_btns, text="Limpiar", command=self.limpiar).pack(side="left", padx=5)
        ttk.Button(frame_btns, text="Refrescar Tabla", command=self.actualizar_tabla).pack(side="left", padx=5)
        
        # 4. TABLA CON ORDENAMIENTO
        self.tabla = ttk.Treeview(self.frame, columns=("ID", "CodCli", "Cliente", "CodProd", "Producto", "Cant"), show="headings", height=8)
        
        # Configurar cabeceras con la función de ordenar
        self.tabla.heading("ID", text="ID Pedido", command=lambda: self.ordenar_columna("ID", False))
        self.tabla.heading("CodCli", text="Cód. Cliente", command=lambda: self.ordenar_columna("CodCli", False))
        self.tabla.heading("Cliente", text="Nombre Cliente", command=lambda: self.ordenar_columna("Cliente", False))
        self.tabla.heading("CodProd", text="Cód. Producto", command=lambda: self.ordenar_columna("CodProd", False))
        self.tabla.heading("Producto", text="Nombre Producto", command=lambda: self.ordenar_columna("Producto", False))
        self.tabla.heading("Cant", text="Cant.", command=lambda: self.ordenar_columna("Cant", False))
        
        self.tabla.column("ID", width=120, anchor="center")
        self.tabla.column("CodCli", width=80, anchor="center")
        self.tabla.column("Cliente", width=150, anchor="w")
        self.tabla.column("CodProd", width=80, anchor="center")
        self.tabla.column("Producto", width=180, anchor="w")
        self.tabla.column("Cant", width=50, anchor="center")
        
        self.tabla.pack(fill="both", expand=True, padx=10, pady=5)
        self.tabla.bind("<ButtonRelease-1>", self.seleccionar_fila)
        self.tabla.bind("<Double-1>", self.abrir_detalle)
        
        self.actualizar_tabla()

    # --- LÓGICA DE INTERFAZ INTELIGENTE ---
    def filtrar_tabla(self, event):
        texto = self.ent_buscar.get().lower()
        for row in self.tabla.get_children(): 
            self.tabla.delete(row)
        for fila in self.datos_memoria:
            # Filtra si el texto coincide con cualquier columna (ID, nombre, código, etc.)
            if any(texto in str(item).lower() for item in fila):
                self.tabla.insert("", "end", values=fila)

    def ordenar_columna(self, col, reverso):
        l = [(self.tabla.set(k, col), k) for k in self.tabla.get_children('')]
        try:
            # Intenta ordenar como número (perfecto para ID Pedido y Cantidad)
            l.sort(key=lambda t: float(str(t[0]).replace('$', '').replace(',', '')), reverse=reverso)
        except ValueError:
            # Si es texto (nombres, códigos), ordena alfabéticamente
            l.sort(reverse=reverso)
        
        for index, (val, k) in enumerate(l):
            self.tabla.move(k, '', index)
        # Cambia la dirección para el próximo clic
        self.tabla.heading(col, command=lambda: self.ordenar_columna(col, not reverso))

    # --- OPERACIONES CRUD ---
    def seleccionar_fila(self, event):
        seleccion = self.tabla.selection()
        if seleccion:
            valores = self.tabla.item(seleccion[0], "values")
            self.id_seleccionado = valores[0] 
            self.ent_cli.delete(0, tk.END)
            self.ent_cli.insert(0, valores[1])
            self.ent_prod.delete(0, tk.END)
            self.ent_prod.insert(0, valores[3])
            self.ent_cant.delete(0, tk.END)
            self.ent_cant.insert(0, valores[5])

    #VENTANA EMERGENTE - DETALLE PEDIDO
    def abrir_detalle(self, event):
        seleccion = self.tabla.selection()
        if not seleccion: return
        
        # Extraemos el ID del pedido clickeado
        numero_pedido = self.tabla.item(seleccion[0], "values")[0]
        pedido_db = crud.obtener_pedido_por_numero(numero_pedido)
        
        if not pedido_db:
            messagebox.showerror("Error", "No se pudo cargar el detalle del pedido en la base de datos.")
            return
            
        # 1. CREAR LA VENTANA EMERGENTE (TopLevel)
        top = tk.Toplevel(self.frame)
        top.title(f"Recibo de Pedido N° {numero_pedido}")
        top.geometry("600x450")
        top.configure(bg="#F3F4F6")
        
        # Esto hace que la ventana emergente bloquee la ventana de atrás hasta que la cierres
        top.transient(self.frame.winfo_toplevel()) 
        top.grab_set() 
        
        # 2. PANEL SUPERIOR: INFORMACIÓN DEL CLIENTE
        frame_info = ttk.LabelFrame(top, text=" Datos del Cliente y Facturación ")
        frame_info.pack(fill="x", padx=15, pady=10)
        
        cod_cli = pedido_db.get("codigo_cliente", "")
        cliente_db = crud.obtener_cliente_por_codigo(cod_cli)
        
        if cliente_db:
            nom_cli = f"{cliente_db.get('nombre', '')} {cliente_db.get('apellido_paterno', '')}"
            fono = cliente_db.get("fono", "Sin teléfono")
            domicilio = f"{cliente_db.get('domicilio', {}).get('calle', '')} {cliente_db.get('domicilio', {}).get('numero', '')}"
        else:
            nom_cli = "Desconocido"
            fono = "N/A"
            domicilio = "N/A"
            
        total_pedido = pedido_db.get("total", 0)
        
        ttk.Label(frame_info, text=f"👤 Cliente: {cod_cli} - {nom_cli}").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        ttk.Label(frame_info, text=f"📞 Fono: {fono}").grid(row=0, column=1, padx=10, pady=5, sticky="w")
        ttk.Label(frame_info, text=f"📍 Domicilio: {domicilio}").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        ttk.Label(frame_info, text=f"💰 Total Boleta: ${total_pedido:,.0f}").grid(row=1, column=1, padx=10, pady=5, sticky="w")
        
        # 3. PANEL INFERIOR: TABLA DE PRODUCTOS
        frame_prods = ttk.LabelFrame(top, text=" Artículos Comprados ")
        frame_prods.pack(fill="both", expand=True, padx=15, pady=5)
        
        tabla_prods = ttk.Treeview(frame_prods, columns=("Cod", "Nom", "Cant", "Total"), show="headings", height=5)
        tabla_prods.heading("Cod", text="Código")
        tabla_prods.heading("Nom", text="Producto")
        tabla_prods.heading("Cant", text="Cant.")
        tabla_prods.heading("Total", text="Total")
        
        tabla_prods.column("Cod", width=80, anchor="center")
        tabla_prods.column("Nom", width=250, anchor="w")
        tabla_prods.column("Cant", width=60, anchor="center")
        tabla_prods.column("Total", width=100, anchor="center")
        
        tabla_prods.pack(fill="both", expand=True, padx=10, pady=10)
        
        # 4. LLENAR LA TABLA LEYENDO EL ARREGLO "DETALLE"
        for det in pedido_db.get("detalle", []):
            c_prod = det.get("codigo_producto", "")
            cant = det.get("cantidad", 0)
            t_linea = det.get("total_linea", 0)
            
            p_db = crud.obtener_producto_por_codigo(c_prod)
            n_prod = p_db.get("nombre", "Desconocido") if p_db else "Desconocido"
            
            # Se inserta cada artículo que compone el pedido
            tabla_prods.insert("", "end", values=(c_prod, n_prod, cant, f"${t_linea:,.0f}"))
            
        # Botón para cerrar la ventana
        ttk.Button(top, text="Cerrar Detalle", command=top.destroy).pack(pady=10)

    def crear(self):
        # Validar que no haya un pedido seleccionado para evitar duplicados accidentales
        if self.id_seleccionado is not None:
            messagebox.showwarning("Acción Denegada", "Tiene un pedido seleccionado en la tabla.\n\nPara registrar uno nuevo, presione el botón 'Limpiar' primero.")
            return
            
        try:
            if crud.registrar_pedido(self.ent_cli.get(), self.ent_prod.get(), int(self.ent_cant.get())):
                self.actualizar_tabla()
                self.limpiar()
            else: messagebox.showerror("Error", "Cliente o Producto no encontrado en la base de datos.")
        except ValueError: messagebox.showerror("Error", "La cantidad debe ser un número entero.")

    def eliminar(self):
        if self.id_seleccionado:
            if messagebox.askyesno("Confirmar", f"¿Estás seguro de eliminar el pedido N° {self.id_seleccionado}?"):
                if crud.eliminar_pedido(self.id_seleccionado):
                    messagebox.showinfo("Éxito", "Pedido eliminado correctamente.")
                    self.limpiar()
                else:
                    messagebox.showerror("Error", "No se encontró el pedido para eliminar.")
        else:
            messagebox.showwarning("Atención", "Por favor, selecciona un pedido de la tabla primero.")

    def limpiar(self):
        self.id_seleccionado = None
        self.ent_cli.delete(0, tk.END)
        self.ent_prod.delete(0, tk.END)
        self.ent_cant.delete(0, tk.END)
        self.ent_buscar.delete(0, tk.END)
        
        for item in self.tabla.selection():
            self.tabla.selection_remove(item)
            
        # Refrescamos para quitar el filtro del buscador si lo había
        self.actualizar_tabla()

    def actualizar_tabla(self):
        for row in self.tabla.get_children(): self.tabla.delete(row)
        self.datos_memoria = crud.obtener_pedidos()
        for f in self.datos_memoria: self.tabla.insert("", "end", values=f)