import tkinter as tk
from tkinter import ttk, messagebox
import cogs.crud as crud

class VistaClientes:
    def __init__(self, parent):
        self.frame = parent
        self.crear_interfaz()

    def crear_interfaz(self):
        frame_form = ttk.LabelFrame(self.frame, text=" Gestión de Clientes ")
        frame_form.pack(fill="x", padx=10, pady=5)
        for i in range(4): frame_form.columnconfigure(i, weight=1)
        
        ttk.Label(frame_form, text="Código:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.ent_cod = ttk.Entry(frame_form)
        self.ent_cod.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        
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
        
        # Botones de Acción
        frame_btns = ttk.Frame(frame_form)
        frame_btns.grid(row=4, column=0, columnspan=4, pady=10)
        ttk.Button(frame_btns, text="Crear", command=self.crear).pack(side="left", padx=5)
        ttk.Button(frame_btns, text="Modificar", command=self.modificar).pack(side="left", padx=5)
        ttk.Button(frame_btns, text="Eliminar", command=self.eliminar).pack(side="left", padx=5)
        ttk.Button(frame_btns, text="Limpiar Campos", command=self.limpiar).pack(side="left", padx=5)
        
        self.tabla = ttk.Treeview(self.frame, columns=("Codigo", "Nombre", "Apellido", "Domicilio", "Fono"), show="headings", height=8)
        for col in self.tabla["columns"]: self.tabla.heading(col, text=col)
        self.tabla.pack(fill="both", expand=True, padx=10, pady=5)
        self.tabla.bind("<ButtonRelease-1>", self.seleccionar_fila)
        
        self.actualizar_tabla()

    def seleccionar_fila(self, event):
        seleccion = self.tabla.selection()
        if seleccion:
            codigo = self.tabla.item(seleccion[0], "values")[0]
            cliente = crud.obtener_cliente_por_codigo(codigo)
            if cliente:
                self.limpiar()
                self.ent_cod.insert(0, cliente.get("codigo", ""))
                self.ent_cod.config(state="readonly") # No permitir cambiar el ID
                self.ent_nom.insert(0, cliente.get("nombre", ""))
                self.ent_ape.insert(0, cliente.get("apellido_paterno", ""))
                self.ent_fono.insert(0, cliente.get("fono", ""))
                
                domicilio = cliente.get("domicilio", {})
                self.ent_calle.insert(0, domicilio.get("calle", ""))
                self.ent_num.insert(0, domicilio.get("numero", ""))
                self.ent_com.insert(0, domicilio.get("comuna", ""))

    def crear(self):
        if crud.registrar_cliente(self.ent_cod.get(), self.ent_nom.get(), self.ent_ape.get(), self.ent_calle.get(), self.ent_num.get(), self.ent_com.get(), self.ent_fono.get()):
            messagebox.showinfo("Éxito", "Cliente creado.")
            self.limpiar()
            self.actualizar_tabla()
        else: messagebox.showerror("Error", "No se pudo crear. Verifique que el código no exista.")

    def modificar(self):
        if crud.actualizar_cliente(self.ent_cod.get(), self.ent_nom.get(), self.ent_ape.get(), self.ent_calle.get(), self.ent_num.get(), self.ent_com.get(), self.ent_fono.get()):
            messagebox.showinfo("Éxito", "Cliente modificado.")
            self.limpiar()
            self.actualizar_tabla()
        else: messagebox.showerror("Error", "Seleccione un cliente para modificar o asegúrese de que hubo cambios.")

    def eliminar(self):
        cod = self.ent_cod.get().strip()
        if cod:
            # Primero pedimos confirmación
            if messagebox.askyesno("Confirmar", f"¿Estás seguro de eliminar al cliente {cod}?"):
                # Intentamos eliminar en la base de datos
                if crud.eliminar_cliente(cod):
                    messagebox.showinfo("Éxito", "Cliente eliminado correctamente.")
                    self.limpiar()
                    self.actualizar_tabla()
                else:
                    messagebox.showerror("Error", "No se encontró el cliente en la base de datos para eliminar.")
        else:
            messagebox.showwarning("Atención", "Por favor, selecciona un cliente de la tabla primero.")

    def limpiar(self):
        self.ent_cod.config(state="normal")
        for ent in [self.ent_cod, self.ent_nom, self.ent_ape, self.ent_calle, self.ent_num, self.ent_com, self.ent_fono]:
            ent.delete(0, tk.END)

    def actualizar_tabla(self):
        for row in self.tabla.get_children(): self.tabla.delete(row)
        for f in crud.obtener_clientes(): self.tabla.insert("", "end", values=f)