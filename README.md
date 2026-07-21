# 🛒 Documentación del Proyecto: ComercioTech (Ev4)

Sistema de gestión de base de datos no relacional (MongoDB) con interfaz gráfica en Python (Tkinter). Implementa un patrón de diseño MVC (Modelo-Vista-Controlador) para separar la lógica de negocio del diseño visual.

---

## 📂 1. Estructura del Proyecto

El proyecto está modularizado para garantizar un código limpio y escalable. Asegúrate de mantener esta jerarquía de carpetas:

```text
Ev4-base-de-datos-no-estructuradas/
├── cogs/
│   ├── Conexion.py          # Script de conexión al servidor MongoDB
│   └── Crud.py              # Lógica de operaciones CRUD y consultas
├── vistas/
│   ├── __init__.py          # Archivo de inicialización del paquete
│   ├── vista_clientes.py    # Interfaz de gestión de clientes
│   ├── vista_productos.py   # Interfaz de inventario
│   └── vista_pedidos.py     # Interfaz de transacciones y recibos
├── main.py                  # Archivo principal de ejecución
└── requirements.txt         # Lista de dependencias del proyecto
```

---

## 🚀 2. Instalación y Ejecución (Entorno Virtual)

Para ejecutar este proyecto de forma aislada y evitar conflictos con otras bibliotecas de tu sistema, sigue estos pasos desde la terminal de tu proyecto:

**1. Crear el entorno virtual:**

```bash
python -m venv venv
```

**2. Activar el entorno virtual (Windows):**

```bash
venv\Scripts\activate
```

**3. Instalar las bibliotecas requeridas:**

Asegúrate de tener tu archivo `requirements.txt` creado (debe contener `pymongo`). Luego ejecuta:

```bash
pip install -r requirements.txt
```

**4. Ejecutar la aplicación:**

Con el entorno activado y tu máquina virtual de MongoDB encendida, inicia el sistema con:

```bash
python main.py
```

---

## 📖 3. Resumen y Funcionamiento del Código

El sistema está diseñado para operar de manera inteligente, automatizando procesos y validando acciones del usuario. Así funciona cada módulo principal:

### ⚙️ Backend (Logica y Controladores)

**`cogs/Conexion.py`**: Es el puente de comunicación. Intenta conectarse a la IP de la máquina virtual (puerto 27017). Si el servidor no responde (timeout), bloquea el inicio de la app para evitar caídas inesperadas y avisa al usuario.

**`cogs/Crud.py`**: El corazón de la aplicación.

- **Auto-incremento**: lee el último código registrado en MongoDB (`CLI-X` o `PROD-X`) y le suma 1 matemáticamente para crear nuevos registros sin intervención manual.
- **Cruce de datos (NoSQL)**: en lugar de guardar nombres duplicados en la colección de Pedidos, guarda sub-documentos y arreglos (detalle). Al consultar, viaja a las otras colecciones para traer los nombres reales en tiempo real.
- **Agrupación**: si un pedido contiene múltiples artículos en su arreglo interno, los agrupa bajo la etiqueta "Varios" para mantener la tabla visual limpia.

### 🖥️ Frontend (Vistas)

**`main.py`**: configura la ventana raíz, aplica un tema visual moderno (estilo Dashboard) usando `ttk.Style` e inicializa un sistema de pestañas (Notebook) que carga las vistas de forma modular.

**Módulo `vistas/`**: cada archivo controla su propia pestaña de manera independiente.

- **Interactividad**: tienen una barra de búsqueda que filtra la tabla en memoria (`KeyRelease`), y las cabeceras de las columnas ordenan los datos (alfabética o numéricamente) al hacer clic.
- **Seguridad UI**: bloquean la creación de registros si hay un ítem seleccionado, previniendo duplicaciones accidentales. Los botones destructivos (Eliminar) requieren confirmación.
- **Ventanas emergentes (modals)**: la vista de pedidos escucha el evento de "Doble Clic" (`<Double-1>`) para generar una ventana flotante estilo recibo, iterando sobre el arreglo interno del pedido para mostrar el detalle de compra sin saturar la pantalla principal.

---

## 📚 Documentación Adicional

Para una explicación funcional del sistema orientada al uso diario (sin detalles técnicos de código), consulta [`DOCUMENTACION.md`](./DOCUMENTACION.md).