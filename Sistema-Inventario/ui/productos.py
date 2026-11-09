
import sqlite3
import customtkinter as ctk
from tkinter import messagebox

from models.producto import Producto
from services.inventario import InventarioService


class FormularioProducto(ctk.CTkToplevel):

    def __init__(self, parent, al_guardar, producto=None):
        super().__init__(parent)

        self.producto = producto
        self.servicio = InventarioService()
        self.al_guardar = al_guardar

        self.editando = producto is not None

        titulo = "Editar producto" if self.editando else "Nuevo producto"

        self.title(titulo)
        self.geometry("450x560")
        self.resizable(False, False)
        self.configure(fg_color="#F3F6FB")

        self.transient(parent)

        ctk.CTkLabel(
            self,
            text=titulo,
            font=("Arial", 25, "bold"),
            text_color="#172B4D"
        ).pack(pady=(25, 20))

        self.campos = {}

        for nombre in [
            "Código", "Nombre", "Categoría",
            "Precio", "Cantidad"
        ]:
            ctk.CTkLabel(
                self,
                text=nombre,
                text_color="#172B4D"
            ).pack(anchor="w", padx=40)

            entrada = ctk.CTkEntry(
                self,
                width=370,
                height=35
            )
            entrada.pack(padx=40, pady=(3, 12))

            self.campos[nombre] = entrada

        if self.editando:
            valores = {
                "Código": producto["codigo"],
                "Nombre": producto["nombre"],
                "Categoría": producto["categoria"],
                "Precio": producto["precio"],
                "Cantidad": producto["cantidad"]
            }

            for campo, valor in valores.items():
                self.campos[campo].insert(0, str(valor))

        ctk.CTkButton(
            self,
            text="Guardar cambios" if self.editando else "Registrar producto",
            height=42,
            command=self.guardar
        ).pack(pady=15)

        self.after(100, self.grab_set)

    def guardar(self):
        try:
            codigo = self.campos["Código"].get().strip()
            nombre = self.campos["Nombre"].get().strip()
            categoria = self.campos["Categoría"].get().strip()
            precio = float(self.campos["Precio"].get())
            cantidad = int(self.campos["Cantidad"].get())

            if not codigo or not nombre or not categoria:
                raise ValueError("Completa todos los campos.")

            producto = Producto(
                codigo=codigo,
                nombre=nombre,
                categoria=categoria,
                precio=precio,
                cantidad=cantidad,
                id=self.producto["id"] if self.editando else None
            )

            if self.editando:
                actualizado = self.servicio.actualizar_producto(producto)
                if not actualizado:
                    raise ValueError("El producto ya no existe.")
                mensaje = "Producto actualizado correctamente."
            else:
                self.servicio.registrar_producto(producto)
                mensaje = "Producto registrado correctamente."

            self.al_guardar()

            messagebox.showinfo(
                "Éxito",
                mensaje,
                parent=self
            )

            self.destroy()

        except sqlite3.IntegrityError:
            messagebox.showerror(
                "Error",
                "Ya existe un producto con ese código.",
                parent=self
            )

        except ValueError as error:
            messagebox.showerror(
                "Datos incorrectos",
                str(error),
                parent=self
            )
