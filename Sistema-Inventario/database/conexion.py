
import sqlite3
from pathlib import Path

BASE_DATOS = Path(__file__).resolve().parent / "inventario.db"


def conectar():
    return sqlite3.connect(BASE_DATOS)


def crear_tablas():
    with conectar() as conexion:
        cursor = conexion.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS productos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                codigo TEXT UNIQUE NOT NULL,
                nombre TEXT NOT NULL,
                categoria TEXT NOT NULL,
                precio REAL NOT NULL,
                cantidad INTEGER NOT NULL DEFAULT 0
            )
        """)

        conexion.commit()
