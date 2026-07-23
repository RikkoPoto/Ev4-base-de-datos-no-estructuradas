import tkinter as tk
from tkinter import ttk, messagebox
import cogs.crud as crud

class VistaPedidos:
    def __init__(self, parent):
        self.frame = parent
        self.id_seleccionado = None
        self.datos_memoria = []
        self.carrito = [] # Almacenará [{"codigo": "PROD-XXX", "nombre": "...", "cantidad": X}]
        self.crear_interfaz()

    def crear_interfaz(self):
        # 1. BARRA DE BÚSQUEDA
        fb = ttk.Frame(self.frame)
        fb.pack(fill="x", padx=10, pady=5)
        ttk.Label(fb, text="🔎 Buscar Pedido:").pack(side="left", padx=5)
        self.ent_buscar = ttk.Entry(fb, width=40)
        self.ent_buscar.pack(side="left", padx=5)
        self.ent_buscar.bind("<KeyRelease>", self.filtrar_tabla)

        # 2. FORMULARIO PRINCIPAL
        ff = ttk.LabelFrame(self.frame, text=" Generar Nuevo Pedido ")
        ff.pack(fill="x", padx=10, pady=5)
        for i in range(4): ff.columnconfigure(i, weight=1)
        
        # Fila 0: ID Pedido (NUEVO) y Cód. Cliente
        ttk.Label(ff, text="ID Pedido:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.ent_id = ttk.Entry(ff)
        self.ent_id.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.ent_id.insert(0, "Auto-generado")
        self.ent_id.config(state="readonly")

        ttk.Label(ff, text="Cód. Cliente:").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.ent_cli = ttk.Entry(ff)
        self.ent_cli.grid(row=0, column=3, padx=5, pady=5, sticky="ew")
        
        # Fila 1: Selección de Productos interactiva
        ttk.Label(ff, text="Productos:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.ent_prod = ttk.Entry(ff, cursor="hand2")
        self.ent_prod.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        self.ent_prod.insert(0, "Haz clic aquí para seleccionar...")
        self.ent_prod.config(state="readonly")
        # Vinculamos el clic a la ventana emergente
        self.ent_prod.bind("<Button-1>", self.abrir_selector_productos)
        
        ttk.Label(ff, text="Cant. Total:").grid(row=1, column=2, padx=5, pady=5, sticky="w")
        self.ent_cant = ttk.Entry(ff)
        self.ent_cant.grid(row=1, column=3, padx=5, pady=5, sticky="ew")
        self.ent_cant.insert(0, "0")
        self.ent_cant.config(state="readonly")
        
        # 3. BOTONES
        fbtn = ttk.Frame(ff)
        fbtn.grid(row=2, column=0, columnspan=4, pady=10)
        ttk.Button(fbtn, text="Crear Pedido", command=self.crear).pack(side="left", padx=5)
        tk.Button(fbtn, text="Eliminar Pedido", command=self.eliminar, bg="#d9534f", fg="white", relief="flat", padx=10, pady=2, cursor="hand2").pack(side="left", padx=5)
        ttk.Button(fbtn, text="Limpiar", command=self.limpiar).pack(side="left", padx=5)
        ttk.Button(fbtn, text="Refrescar", command=self.actualizar_tabla).pack(side="left", padx=5)
        
        # 4. TABLA PRINCIPAL
        self.tabla = ttk.Treeview(self.frame, columns=("ID", "CodCli", "Cliente", "CodProd", "Producto", "Cant"), show="headings", height=8)
        for c in self.tabla["columns"]: self.tabla.heading(c, text=c, command=lambda x=c: self.ordenar_columna(x, False))
        self.tabla.column("ID", width=80, anchor="center"); self.tabla.column("CodCli", width=80, anchor="center")
        self.tabla.column("Cliente", width=150, anchor="w"); self.tabla.column("CodProd", width=80, anchor="center")
        self.tabla.column("Producto", width=180, anchor="w"); self.tabla.column("Cant", width=50, anchor="center")
        
        self.tabla.pack(fill="both", expand=True, padx=10, pady=5)
        self.tabla.bind("<ButtonRelease-1>", self.seleccionar_fila)
        self.tabla.bind("<Double-1>", self.abrir_detalle)
        self.actualizar_tabla()

    # --- VENTANA EMERGENTE PARA SELECCIONAR PRODUCTOS ---
    def abrir_selector_productos(self, event):
        if self.id_seleccionado:
            return messagebox.showinfo("Lectura", "Está visualizando un pedido antiguo.\nPresione 'Limpiar' primero para crear un pedido nuevo.")
            
        top = tk.Toplevel(self.frame)
        top.title("🛒 Carrito - Seleccionar Productos")
        top.geometry("650x450")
        top.configure(bg="#F3F4F6")
        top.transient(self.frame.winfo_toplevel())
        top.grab_set() 
        
        # Panel superior: Lista de la base de datos
        fp = ttk.LabelFrame(top, text=" Inventario Disponible ")
        fp.pack(fill="both", expand=True, padx=10, pady=5)
        
        tv_inv = ttk.Treeview(fp, columns=("Cod", "Nom", "Precio", "Stock"), show="headings", height=5)
        for c in tv_inv["columns"]: tv_inv.heading(c, text=c)
        tv_inv.column("Cod", width=80); tv_inv.column("Nom", width=250); tv_inv.column("Precio", width=80); tv_inv.column("Stock", width=60)
        tv_inv.pack(fill="both", expand=True, padx=5, pady=5)
        
        for p in crud.obtener_productos():
            tv_inv.insert("", "end", values=p)
            
        # Panel central: Controles para agregar cantidad
        fc = ttk.Frame(top)
        fc.pack(fill="x", padx=10, pady=5)
        ttk.Label(fc, text="Cantidad:").pack(side="left", padx=5)
        spin_cant = ttk.Spinbox(fc, from_=1, to=999, width=10)
        spin_cant.set(1)
        spin_cant.pack(side="left", padx=5)
        
        def agregar_al_carrito():
            sel = tv_inv.selection()
            if not sel: return messagebox.showwarning("Atención", "Seleccione un producto del inventario.")
            
            valores = tv_inv.item(sel[0], "values")
            cod, nom, stock_disp = valores[0], valores[1], int(valores[3])
            try: cant = int(spin_cant.get())
            except ValueError: return
            
            if cant <= 0 or cant > stock_disp:
                return messagebox.showerror("Error", f"Cantidad inválida o supera el stock ({stock_disp}).")
                
            # Evitar duplicados en el carrito, sumar cantidad si ya existe
            existe = False
            for item in self.carrito:
                if item["codigo"] == cod:
                    item["cantidad"] += cant
                    existe = True
                    break
            if not existe:
                self.carrito.append({"codigo": cod, "nombre": nom, "cantidad": cant})
                
            actualizar_vista_carrito()
            
        ttk.Button(fc, text="➕ Añadir", command=agregar_al_carrito).pack(side="left", padx=10)
        
        # Panel inferior: Productos ya seleccionados
        fc_car = ttk.LabelFrame(top, text=" Tu Carrito Actual ")
        fc_car.pack(fill="both", expand=True, padx=10, pady=5)
        
        tv_car = ttk.Treeview(fc_car, columns=("Cod", "Nom", "Cant"), show="headings", height=4)
        for c in tv_car["columns"]: tv_car.heading(c, text=c)
        tv_car.pack(fill="both", expand=True, padx=5, pady=5)
        
        def actualizar_vista_carrito():
            for r in tv_car.get_children(): tv_car.delete(r)
            for item in self.carrito:
                tv_car.insert("", "end", values=(item["codigo"], item["nombre"], item["cantidad"]))
                
        def confirmar_seleccion():
            if not self.carrito:
                return messagebox.showwarning("Vacío", "El carrito está vacío.")
                
            total_items = sum(i["cantidad"] for i in self.carrito)
            
            self.ent_prod.config(state="normal")
            self.ent_prod.delete(0, tk.END)
            if len(self.carrito) == 1: self.ent_prod.insert(0, self.carrito[0]["codigo"])
            else: self.ent_prod.insert(0, f"Varios seleccionados ({len(self.carrito)} prod.)")
            self.ent_prod.config(state="readonly")
            
            self.ent_cant.config(state="normal")
            self.ent_cant.delete(0, tk.END)
            self.ent_cant.insert(0, str(total_items))
            self.ent_cant.config(state="readonly")
            
            top.destroy()
            
        actualizar_vista_carrito() # Carga inicial si el carrito ya tenía algo
        ttk.Button(top, text="✅ Confirmar Productos", command=confirmar_seleccion).pack(pady=10)

    # --- UTILIDADES DE TABLA Y CRUD ---
    def filtrar_tabla(self, event):
        t = self.ent_buscar.get().lower()
        for r in self.tabla.get_children(): self.tabla.delete(r)
        for f in self.datos_memoria:
            if any(t in str(i).lower() for i in f): self.tabla.insert("", "end", values=f)

    def ordenar_columna(self, col, rev):
        l = [(self.tabla.set(k, col), k) for k in self.tabla.get_children('')]
        try: l.sort(key=lambda t: float(str(t[0]).replace('$', '').replace(',', '')), reverse=rev)
        except: l.sort(reverse=rev)
        for i, (v, k) in enumerate(l): self.tabla.move(k, '', i)
        self.tabla.heading(col, command=lambda: self.ordenar_columna(col, not rev))

    def seleccionar_fila(self, event):
        sel = self.tabla.selection()
        if sel:
            v = self.tabla.item(sel[0], "values")
            self.id_seleccionado = v[0]
            
            self.ent_id.config(state="normal")
            self.ent_id.delete(0, tk.END)
            self.ent_id.insert(0, v[0])
            self.ent_id.config(state="readonly")
            
            self.ent_cli.delete(0, tk.END); self.ent_cli.insert(0, v[1])
            
            self.ent_prod.config(state="normal")
            self.ent_prod.delete(0, tk.END)
            self.ent_prod.insert(0, "(Ver Detalles con Doble Clic)")
            self.ent_prod.config(state="readonly")
            
            self.ent_cant.config(state="normal")
            self.ent_cant.delete(0, tk.END); self.ent_cant.insert(0, v[5])
            self.ent_cant.config(state="readonly")

    def abrir_detalle(self, event):
        if not self.tabla.selection(): return
        num = self.tabla.item(self.tabla.selection()[0], "values")[0]
        pdb = crud.obtener_pedido_por_numero(num)
        if not pdb: return messagebox.showerror("Error", "No se cargó detalle.")
            
        top = tk.Toplevel(self.frame)
        top.title(f"Recibo N° {num}"); top.geometry("600x450"); top.configure(bg="#F3F4F6")
        top.transient(self.frame.winfo_toplevel()); top.grab_set() 
        
        fi = ttk.LabelFrame(top, text=" Datos del Cliente "); fi.pack(fill="x", padx=15, pady=10)
        cdb = crud.obtener_cliente_por_codigo(pdb.get("codigo_cliente", ""))
        
        nc = f"{cdb.get('nombre', '')} {cdb.get('apellido_paterno', '')}" if cdb else "Desconocido"
        fn = cdb.get("fono", "N/A") if cdb else "N/A"
        dm = f"{cdb.get('domicilio', {}).get('calle', '')} {cdb.get('domicilio', {}).get('numero', '')}" if cdb else "N/A"
        
        ttk.Label(fi, text=f"👤 Cliente: {nc}").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        ttk.Label(fi, text=f"📞 Fono: {fn}").grid(row=0, column=1, padx=10, pady=5, sticky="w")
        ttk.Label(fi, text=f"📍 Domicilio: {dm}").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        ttk.Label(fi, text=f"💰 Total: ${pdb.get('total', 0):,.0f}").grid(row=1, column=1, padx=10, pady=5, sticky="w")
        
        fp = ttk.LabelFrame(top, text=" Artículos Comprados "); fp.pack(fill="both", expand=True, padx=15, pady=5)
        tp = ttk.Treeview(fp, columns=("C", "N", "Cant", "T"), show="headings", height=5)
        for i, c in enumerate(["Código", "Producto", "Cant.", "Total Línea"]): tp.heading(("C", "N", "Cant", "T")[i], text=c)
        tp.pack(fill="both", expand=True, padx=10, pady=10)
        
        for d in pdb.get("detalle", []):
            pr = crud.obtener_producto_por_codigo(d.get("codigo_producto", ""))
            tp.insert("", "end", values=(d.get("codigo_producto", ""), pr.get("nombre", "Desconocido") if pr else "Desconocido", d.get("cantidad", 0), f"${d.get('total_linea', 0):,.0f}"))
        ttk.Button(top, text="Cerrar", command=top.destroy).pack(pady=10)

    def crear(self):
        if self.id_seleccionado: return messagebox.showwarning("Denegado", "Limpie campos primero para crear uno nuevo.")
        if not self.ent_cli.get().strip(): return messagebox.showwarning("Campos Vacíos", "Ingrese un código de cliente.")
        if not self.carrito: return messagebox.showwarning("Carrito Vacío", "Haga clic en 'Productos' para añadir artículos al pedido.")

        exito, mensaje = crud.registrar_pedido(self.ent_cli.get(), self.carrito)
        
        if exito: 
            messagebox.showinfo("Éxito", mensaje)
            self.actualizar_tabla()
            self.limpiar()
        else: 
            messagebox.showerror("Error al crear pedido", mensaje)

    def eliminar(self):
        if self.id_seleccionado and messagebox.askyesno("Confirmar", f"¿Eliminar pedido N° {self.id_seleccionado}? Se devolverá el stock."):
            exito, mensaje = crud.eliminar_pedido(self.id_seleccionado)
            if exito:
                messagebox.showinfo("Éxito", mensaje)
                self.limpiar(); self.actualizar_tabla()
            else:
                messagebox.showerror("Error", mensaje)

    def limpiar(self):
        self.id_seleccionado = None
        self.carrito = [] # Vaciamos el carrito
        
        self.ent_id.config(state="normal")
        self.ent_id.delete(0, tk.END)
        self.ent_id.insert(0, "Auto-generado")
        self.ent_id.config(state="readonly")
        
        self.ent_cli.delete(0, tk.END)
        
        self.ent_prod.config(state="normal")
        self.ent_prod.delete(0, tk.END)
        self.ent_prod.insert(0, "Haz clic aquí para seleccionar...")
        self.ent_prod.config(state="readonly")
        
        self.ent_cant.config(state="normal")
        self.ent_cant.delete(0, tk.END)
        self.ent_cant.insert(0, "0")
        self.ent_cant.config(state="readonly")
        
        self.ent_buscar.delete(0, tk.END)
        for i in self.tabla.selection(): self.tabla.selection_remove(i)
        self.actualizar_tabla()

    def actualizar_tabla(self):
        for r in self.tabla.get_children(): self.tabla.delete(r)
        self.datos_memoria = crud.obtener_pedidos()
        for f in self.datos_memoria: self.tabla.insert("", "end", values=f)