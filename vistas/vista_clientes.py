import tkinter as tk
from tkinter import ttk, messagebox
import cogs.crud as crud

class VistaClientes:
    def __init__(self, parent):
        self.frame = parent
        self.datos_memoria = [] # Para el buscador
        self.crear_interfaz()

    def crear_interfaz(self):
        # 1. BARRA DE BÚSQUEDA
        frame_busqueda = ttk.Frame(self.frame)
        frame_busqueda.pack(fill="x", padx=10, pady=5)
        ttk.Label(frame_busqueda, text="🔎 Buscar Cliente (Cualquier campo):").pack(side="left", padx=5)
        self.ent_buscar = ttk.Entry(frame_busqueda, width=40)
        self.ent_buscar.pack(side="left", padx=5)
        self.ent_buscar.bind("<KeyRelease>", self.filtrar_tabla) # Filtra al escribir

        # 2. FORMULARIO
        frame_form = ttk.LabelFrame(self.frame, text=" Gestión de Clientes ")
        frame_form.pack(fill="x", padx=10, pady=5)
        for i in range(4): frame_form.columnconfigure(i, weight=1)
        
        ttk.Label(frame_form, text="Código (Auto):").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.ent_cod = ttk.Entry(frame_form)
        self.ent_cod.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.ent_cod.insert(0, "Auto-generado")
        self.ent_cod.config(state="readonly") # Bloqueado para el usuario
        
        ttk.Label(frame_form, text="Fono:").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.ent_fono = ttk.Entry(frame_form)
        self.ent_fono.grid(row=0, column=3, padx=5, pady=5, sticky="ew")

        ttk.Label(frame_form, text="Nombre:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.ent_nom = ttk.Entry(frame_form)
        self.ent_nom.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        
        ttk.Label(frame_form, text="Apellido:").grid(row=1, column=2, padx=5, pady=5, sticky="w")
        self.ent_ape = ttk.Entry(frame_form)
        self.ent_ape.grid(row=1, column=3, padx=5, pady=5, sticky="ew")

        ttk.Label(frame_form, text="Calle:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.ent_calle = ttk.Entry(frame_form)
        self.ent_calle.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        
        ttk.Label(frame_form, text="Número:").grid(row=2, column=2, padx=5, pady=5, sticky="w")
        self.ent_num = ttk.Entry(frame_form)
        self.ent_num.grid(row=2, column=3, padx=5, pady=5, sticky="ew")
        
        ttk.Label(frame_form, text="Comuna:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.ent_com = ttk.Entry(frame_form)
        self.ent_com.grid(row=3, column=1, padx=5, pady=5, sticky="ew")
        
        # BOTONES
        frame_btns = ttk.Frame(frame_form)
        frame_btns.grid(row=4, column=0, columnspan=4, pady=10)
        ttk.Button(frame_btns, text="Crear", command=self.crear).pack(side="left", padx=5)
        ttk.Button(frame_btns, text="Modificar", command=self.modificar).pack(side="left", padx=5)
        tk.Button(frame_btns, text="Eliminar", command=self.eliminar, bg="#d9534f", fg="white", relief="flat", padx=10, pady=2, cursor="hand2").pack(side="left", padx=5)
        ttk.Button(frame_btns, text="Limpiar", command=self.limpiar).pack(side="left", padx=5)
        ttk.Button(frame_btns, text="Refrescar Tabla", command=self.actualizar_tabla).pack(side="left", padx=5)
        
        # TABLA
        self.tabla = ttk.Treeview(self.frame, columns=("Codigo", "Nombre", "Apellido", "Domicilio", "Fono"), show="headings", height=8)
        
        # Configurar cabeceras con comando de ordenamiento
        for col in self.tabla["columns"]:
            self.tabla.heading(col, text=col, command=lambda c=col: self.ordenar_columna(c, False))
            
        self.tabla.column("Codigo", width=80, anchor="center")
        self.tabla.column("Nombre", width=120, anchor="w")
        self.tabla.column("Apellido", width=120, anchor="w")
        self.tabla.column("Domicilio", width=250, anchor="w")
        self.tabla.column("Fono", width=100, anchor="center")
        
        self.tabla.pack(fill="both", expand=True, padx=10, pady=5)
        self.tabla.bind("<ButtonRelease-1>", self.seleccionar_fila)
        
        self.actualizar_tabla()

    # --- LÓGICA DE INTERFAZ INTELIGENTE ---
    def filtrar_tabla(self, event):
        texto_busqueda = self.ent_buscar.get().lower()
        for row in self.tabla.get_children():
            self.tabla.delete(row)
        for fila in self.datos_memoria:
            # Si el texto escrito está dentro de cualquier dato de la fila, lo muestra
            if any(texto_busqueda in str(item).lower() for item in fila):
                self.tabla.insert("", "end", values=fila)

    def ordenar_columna(self, col, reverso):
        l = [(self.tabla.set(k, col), k) for k in self.tabla.get_children('')]
        # Intenta ordenar como número, si falla, ordena alfabéticamente
        try:
            l.sort(key=lambda t: float(t[0]), reverse=reverso)
        except ValueError:
            l.sort(reverse=reverso)
        
        for index, (val, k) in enumerate(l):
            self.tabla.move(k, '', index)
        # Cambia la dirección para el próximo clic
        self.tabla.heading(col, command=lambda: self.ordenar_columna(col, not reverso))

    # --- OPERACIONES CRUD ---
    def seleccionar_fila(self, event):
        seleccion = self.tabla.selection()
        if seleccion:
            codigo = self.tabla.item(seleccion[0], "values")[0]
            cliente = crud.obtener_cliente_por_codigo(codigo)
            if cliente:
                self.limpiar()
                self.ent_cod.config(state="normal")
                self.ent_cod.delete(0, tk.END)
                self.ent_cod.insert(0, cliente.get("codigo", ""))
                self.ent_cod.config(state="readonly")
                
                self.ent_nom.insert(0, cliente.get("nombre", ""))
                self.ent_ape.insert(0, cliente.get("apellido_paterno", ""))
                self.ent_fono.insert(0, cliente.get("fono", ""))
                domicilio = cliente.get("domicilio", {})
                self.ent_calle.insert(0, domicilio.get("calle", ""))
                self.ent_num.insert(0, domicilio.get("numero", ""))
                self.ent_com.insert(0, domicilio.get("comuna", ""))

    def crear(self):
        if self.ent_cod.get() != "Auto-generado": return messagebox.showwarning("Denegado", "Limpie los campos primero.")
        
        # VALIDACIÓN N°9: Campos vacíos
        if not all([self.ent_nom.get().strip(), self.ent_ape.get().strip(), self.ent_calle.get().strip(), self.ent_num.get().strip(), self.ent_com.get().strip(), self.ent_fono.get().strip()]):
            return messagebox.showwarning("Campos Vacíos", "Por favor, complete todos los campos del cliente. No se permiten datos vacíos.")

        if crud.registrar_cliente(self.ent_nom.get(), self.ent_ape.get(), self.ent_calle.get(), self.ent_num.get(), self.ent_com.get(), self.ent_fono.get()):
            self.limpiar(); self.actualizar_tabla()

    def modificar(self):
        # VALIDACIÓN N°9: Campos vacíos
        if not all([self.ent_nom.get().strip(), self.ent_ape.get().strip(), self.ent_calle.get().strip(), self.ent_num.get().strip(), self.ent_com.get().strip(), self.ent_fono.get().strip()]):
            return messagebox.showwarning("Campos Vacíos", "Por favor, complete todos los campos del cliente. No se permiten datos vacíos.")

        self.ent_cod.config(state="normal"); cod = self.ent_cod.get().strip(); self.ent_cod.config(state="readonly")
        if crud.actualizar_cliente(cod, self.ent_nom.get(), self.ent_ape.get(), self.ent_calle.get(), self.ent_num.get(), self.ent_com.get(), self.ent_fono.get()):
            self.limpiar(); self.actualizar_tabla()

    def eliminar(self):
        self.ent_cod.config(state="normal")
        cod = self.ent_cod.get().strip()
        self.ent_cod.config(state="readonly")
        
        if cod != "Auto-generado" and messagebox.askyesno("Confirmar", f"¿Eliminar el cliente {cod}?"):
            # Recibimos el estado y el mensaje
            exito, mensaje = crud.eliminar_cliente(cod)
            
            if exito:
                messagebox.showinfo("Éxito", mensaje)
                self.limpiar()
                self.actualizar_tabla()
            else:
                # Si falla por integridad referencial, lanzamos el error
                messagebox.showerror("Acción Denegada", mensaje)

    def limpiar(self):
        self.ent_cod.config(state="normal")
        self.ent_cod.delete(0, tk.END)
        self.ent_cod.insert(0, "Auto-generado")
        self.ent_cod.config(state="readonly")
        for ent in [self.ent_nom, self.ent_ape, self.ent_calle, self.ent_num, self.ent_com, self.ent_fono]:
            ent.delete(0, tk.END)
        self.ent_buscar.delete(0, tk.END)
        
        # Quitar la selección azul de la tabla
        for item in self.tabla.selection():
            self.tabla.selection_remove(item)
            
        self.actualizar_tabla()

    def actualizar_tabla(self):
        for row in self.tabla.get_children(): self.tabla.delete(row)
        self.datos_memoria = crud.obtener_clientes()
        for f in self.datos_memoria: self.tabla.insert("", "end", values=f)