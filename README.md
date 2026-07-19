# Ev4-base-de-datos-no-estructuradas

Sistema de gestión para la empresa **ComercioTech** desarrollado en Python y Tkinter, conectado a un clúster local de MongoDB (Community Server) alojado en una máquina virtual.

## 👥 Coordinación del Equipo de Desarrollo

*   **MongoDB:** Configuración del servidor OVA, apertura de puertos (`27017`) y gestión de la librería `pymongo`.
*   **Sistema Operativo:** Desarrollo y compilación en entorno Windows; Servidor de base de datos alojado en máquina virtual Linux.
*   **Documentación:** Redacción del informe final, diagramas de arquitectura y manual de usuario de la aplicación.

---

## ⚠️ Aviso Importante (Entorno de Producción)

Esta aplicación está pensada para su uso general en producción. Para facilitar el despliegue al cliente final, **el software se distribuye compilado**. 

Al empaquetar el sistema mediante herramientas de compilación, el intérprete de Python 3.14 y las dependencias quedan integrados en el binario. **No es necesario automatizar la instalación de Python en la máquina del cliente**, basta con ejecutar el archivo compilado directamente.

---

## 📂 Estructura de la Aplicación

El código utiliza una arquitectura modular para separar la interfaz de la lógica de datos:

```text
ev4_bd-noestructuradas/
├── cogs/               ← Carpeta de configuración y lógica de negocio
│   ├── Crud.py         ← Operaciones NoSQL (Crear, Leer) y validaciones
│   └── Conexion.py     ← Cadena de conexión hacia el servidor MongoDB
├── main.py             ← Iniciador de la app y vistas de Tkinter
├── requirements.txt    ← Manifiesto de dependencias de desarrollo
└── README.md           ← Documentación del proyecto

---

🌐 Configuración de la Base de Datos (VirtualBox)
Para que el aplicativo logre enlazar con MongoDB, la máquina virtual (OVA) debe cumplir con lo siguiente:

Adaptador de Red: Configurado en modo Adaptador Puente para obtener una IP visible en la red local.

Bind IP: El archivo /etc/mongod.conf dentro del servidor debe tener bindIp: 0.0.0.0 para permitir conexiones remotas.

Conexión en App: Actualizar la IP resultante en el archivo cogs/Conexion.py.

---

💻 Uso en Modo Desarrollo (Programadores)
Si deseas modificar el código o ejecutarlo desde consola, sigue estos pasos:

Crear y activar un entorno virtual:

Bash
python -m venv venv
.\venv\Scripts\activate
Instalar dependencias:

Bash
pip install -r requirements.txt
Ejecutar:

Bash
python main.py

---

📦 Compilación para Producción
Para generar el ejecutable final para el usuario:

Instalar PyInstaller en el entorno virtual: pip install pyinstaller

Compilar en un solo archivo ocultando la consola de comandos:

Bash
pyinstaller --noconfirm --onedir --windowed main.py
El archivo listo para producción se encontrará dentro de la carpeta dist/.


<FollowUp label="¿Quieres que te muestre cómo adaptar tu código a Conexion.py y Crud.py?" qu