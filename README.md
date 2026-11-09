# Sistema de Inventario

Aplicación de escritorio desarrollada en Python para gestionar productos, controlar existencias y administrar movimientos de inventario mediante una interfaz gráfica moderna e intuitiva.

## Funcionalidades

- Registro de productos con código, nombre, categoría, precio y cantidad.
- Búsqueda de productos.
- Edición y eliminación de registros.
- Panel de estadísticas con indicadores del inventario.
- Registro de entradas y salidas de mercancía.
- Actualización automática de existencias.
- Almacenamiento local mediante SQLite.
- Interfaz gráfica desarrollada con CustomTkinter.

## Tecnologías utilizadas

- **Python:** lenguaje principal de programación.
- **CustomTkinter:** desarrollo de la interfaz gráfica.
- **SQLite:** almacenamiento de productos.
- **Tkinter:** componentes y cuadros de diálogo.

## Estructura del proyecto

```text
Sistema-Inventario/
├── assets/
├── database/
│   ├── __init__.py
│   └── conexion.py
├── models/
│   ├── __init__.py
│   └── producto.py
├── services/
│   ├── __init__.py
│   └── inventario.py
├── ui/
│   ├── __init__.py
│   ├── ventana_principal.py
│   ├── productos.py
│   └── movimientos.py
├── main.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Instalación

1. Clona el repositorio:

```bash
git clone URL_DEL_REPOSITORIO
cd Sistema-Inventario
```

2. Crea un entorno virtual:

```bash
python -m venv .venv
```

3. Activa el entorno virtual en Windows:

```powershell
.\.venv\Scripts\Activate.ps1
```

4. Instala las dependencias:

```bash
python -m pip install -r requirements.txt
```

5. Ejecuta la aplicación:

```bash
python main.py
```

## Capturas de pantalla

<img width="1278" height="787" alt="image" src="https://github.com/user-attachments/assets/9ebdd9e4-0a6d-4d7a-bc9b-52f16e46388f" />
<img width="1277" height="788" alt="image" src="https://github.com/user-attachments/assets/11653eab-304c-4d77-b002-962a74fa5356" />


## Estado del proyecto

**Versión 1.0 — Funcional.**

## Autor

Desarrollado por Brayan como proyecto de portafolio de programación en Python.
