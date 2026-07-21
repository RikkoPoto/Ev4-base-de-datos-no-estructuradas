# 📘 Documentación Práctica del Sistema ComercioTech

> Documento complementario al `README.md`: explica el funcionamiento del sistema en términos prácticos, pensado para cualquier persona que vaya a operarlo (cajero, administrador) o que quiera entender su lógica sin entrar en detalles de código.

## Índice

1. [Introducción y Propósito del Sistema](#introducción-y-propósito-del-sistema)
2. [Explicación de las Clases (Las Pantallas de Trabajo)](#explicación-de-las-clases-las-pantallas-de-trabajo)
3. [Explicación de las Funciones Principales (Los Trabajadores Invisibles)](#explicación-de-las-funciones-principales-los-trabajadores-invisibles)
4. [Características Prácticas y Beneficios para el Usuario](#características-prácticas-y-beneficios-para-el-usuario)
5. [Resumen del Valor del Sistema](#resumen-del-valor-del-sistema)

---

## 🎯 Introducción y Propósito del Sistema

ComercioTech es una herramienta de software diseñada para administrar un negocio de forma centralizada. Su objetivo principal es facilitar el trabajo diario de un cajero o administrador, eliminando el uso de papel o planillas de Excel desordenadas. El sistema guarda todo de forma segura en un servidor de red y ofrece una pantalla amigable dividida en tres grandes áreas de trabajo: **Clientes**, **Inventario** y **Ventas**.

---

## 🧩 Explicación de las Clases (Las Pantallas de Trabajo)

En programación, el sistema utiliza "Clases" para construir cada pantalla. En la práctica, cada clase funciona como un departamento distinto dentro del negocio:

### 👤 1. Clase `VistaClientes` — El mostrador de atención

Esta clase es responsable de gestionar a las personas que interactúan con el negocio.

En la práctica, permite ingresar los datos personales y de contacto de un comprador. Tiene una característica muy útil: cuando el empleado inscribe a alguien nuevo, la clase bloquea la casilla del código y le asigna uno automáticamente. Esto evita que dos clientes terminen con el mismo número de identificación. También permite corregir direcciones si el cliente se muda, o borrarlo del sistema si es necesario, exigiendo siempre una confirmación para evitar que el empleado elimine a alguien por accidente.

### 📦 2. Clase `VistaProductos` — La bodega o inventario

Esta clase controla qué se vende y a qué precio.

Para el usuario, es una tabla que muestra el catálogo completo. Permite a los administradores crear nuevos productos, actualizar los precios cuando hay inflación o cambiar la cantidad de stock disponible. Al igual que con los clientes, la clase genera el código de barras por su cuenta, quitando esa responsabilidad de los hombros del trabajador.

### 💳 3. Clase `VistaPedidos` — La caja registradora

Esta es la clase más avanzada porque es la que conecta a los clientes con los productos.

En la práctica, es el lugar donde el empleado registra una venta. Esta clase hace el trabajo pesado: junta los datos, calcula el total a pagar y genera un número de recibo consecutivo. Si el cliente compró cinco artículos distintos en una sola vez, la clase es lo suficientemente inteligente para no llenar la pantalla principal de registros repetidos; simplemente agrupa la venta mostrando la palabra "Varios" y suma la cantidad total de productos llevados.

---

## ⚙️ Explicación de las Funciones Principales (Los Trabajadores Invisibles)

Las funciones son las órdenes que se ejecutan silenciosamente por detrás cuando el usuario presiona un botón. En la práctica comercial, hacen lo siguiente:

- **Función de conexión segura**: es el guardia de seguridad del sistema. Antes de que el programa se abra en la pantalla, esta función viaja al servidor y revisa si hay acceso. Si el servidor está apagado o el cable de red está desconectado, detiene el inicio y le avisa al usuario: "No hay conexión, encienda el servidor", evitando que el programa colapse de golpe en medio del trabajo.

- **Funciones de auto-incremento**: son las secretarias del sistema. Cuando el usuario presiona "Crear", estas funciones revisan velozmente cuál fue el último archivo guardado en el negocio, miran el número que tiene, le suman uno matemáticamente y se lo asignan al nuevo registro para mantener un orden perfecto.

- **Funciones de traducción y cruce de datos**: son los archivistas. Para ahorrar memoria, el sistema guarda las ventas usando solo códigos (ejemplo: el cliente 001 compró el artículo 101). Cuando el usuario quiere ver la lista de ventas en su pantalla, esta función corre al archivo de clientes para ver cómo se llama el 001, luego corre al archivo de inventario para ver qué es el 101, y le entrega a la pantalla la información traducida en un texto humano (ejemplo: "Juan Pérez compró un Teclado").

---

## ✨ Características Prácticas y Beneficios para el Usuario

El sistema no solo almacena información, sino que está pensado para que trabajar en él sea rápido y a prueba de errores. Sus características destacan por lo siguiente:

- **Buscador inteligente en tiempo real**: cada pantalla tiene una barra de búsqueda. El empleado no necesita especificar si está buscando por nombre, por apellido o por teléfono. Solo empieza a teclear y la tabla comienza a filtrar los resultados en ese mismo instante, lo cual es ideal para agilizar la atención cuando hay filas de espera.

- **Ordenamiento de datos con un clic**: si el administrador quiere saber cuáles son los productos más caros o cuáles se están quedando sin stock, solo debe hacer clic en la palabra "Precio" o "Stock" en la parte superior de la tabla y todo se ordena automáticamente. Si hace clic en "Nombre", la lista se organiza de la A a la Z.

- **El recibo detallado (doble clic)**: es la función estrella para el servicio al cliente. Si un comprador necesita ver el comprobante de un pedido pasado, el empleado simplemente hace doble clic sobre esa venta en la lista. Inmediatamente se abre una ventana flotante, limpia y ordenada, que funciona como una boleta virtual: muestra los datos de facturación, la dirección de despacho y la lista exacta de todos los artículos que llevó, con el valor de cada línea y el costo final de la compra.

- **Protección contra errores humanos (UX)**: el programa asume que el usuario puede equivocarse y lo protege. Si el cajero hace clic en un cliente antiguo e intenta presionar "Crear" por accidente, el sistema lo bloquea y le indica que primero debe limpiar la pantalla para evitar duplicar al cliente. Los botones de acción destructiva están resaltados en color rojo para alertar sobre el peligro de borrarlos, y el sistema impide estrictamente ingresar letras en las casillas donde solo deberían ir precios o cantidades numéricas.

---

## 💡 Resumen del Valor del Sistema

En términos prácticos, este desarrollo transforma un modelo de negocio manual en uno completamente digitalizado. Las clases organizan físicamente el espacio de trabajo en la pantalla, las funciones automatizan las tareas repetitivas de cálculo y numeración, y las características de interfaz garantizan que cualquier trabajador, sin importar su nivel de conocimientos tecnológicos, pueda utilizar la caja registradora y el inventario sin cometer errores que comprometan la información del comercio.