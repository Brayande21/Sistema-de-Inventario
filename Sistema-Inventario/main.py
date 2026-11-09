
from database.conexion import crear_tablas
from ui.ventana_principal import VentanaPrincipal


def main():
    crear_tablas()

    app = VentanaPrincipal()
    app.mainloop()


if __name__ == "__main__":
    main()
