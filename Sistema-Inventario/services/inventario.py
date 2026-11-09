
from database.conexion import conectar
from models.producto import Producto


class InventarioService:

    def registrar_producto(self, producto: Producto):
        if producto.precio < 0 or producto.cantidad < 0:
            raise ValueError("El precio y la cantidad no pueden ser negativos.")

        with conectar() as conexion:
            conexion.execute("""
                INSERT INTO productos
                (codigo, nombre, categoria, precio, cantidad)
                VALUES (?, ?, ?, ?, ?)
            """, (
                producto.codigo,
                producto.nombre,
                producto.categoria,
                producto.precio,
                producto.cantidad
            ))

    def listar_productos(self):
        with conectar() as conexion:
            conexion.row_factory = __import__("sqlite3").Row
            cursor = conexion.execute(
                "SELECT * FROM productos ORDER BY id DESC"
            )
            return [dict(fila) for fila in cursor.fetchall()]

    def buscar_productos(self, texto):
        with conectar() as conexion:
            conexion.row_factory = __import__("sqlite3").Row
            cursor = conexion.execute("""
                SELECT * FROM productos
                WHERE codigo LIKE ? OR nombre LIKE ?
                ORDER BY nombre
            """, (f"%{texto}%", f"%{texto}%"))
            return [dict(fila) for fila in cursor.fetchall()]

    def actualizar_producto(self, producto: Producto):
        if producto.id is None:
            raise ValueError("Debes indicar el ID del producto.")

        if producto.precio < 0 or producto.cantidad < 0:
            raise ValueError("El precio y la cantidad no pueden ser negativos.")

        with conectar() as conexion:
            cursor = conexion.execute("""
                UPDATE productos
                SET codigo = ?, nombre = ?, categoria = ?,
                    precio = ?, cantidad = ?
                WHERE id = ?
            """, (
                producto.codigo,
                producto.nombre,
                producto.categoria,
                producto.precio,
                producto.cantidad,
                producto.id
            ))
            return cursor.rowcount > 0

    def eliminar_producto(self, producto_id):
        with conectar() as conexion:
            cursor = conexion.execute(
                "DELETE FROM productos WHERE id = ?",
                (producto_id,)
            )
            return cursor.rowcount > 0

    def registrar_movimiento(self, producto_id, tipo, cantidad):
        if tipo not in ("entrada", "salida"):
            raise ValueError("Tipo de movimiento no válido.")

        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor que cero.")

        with conectar() as conexion:
            cursor = conexion.execute(
                "SELECT cantidad FROM productos WHERE id = ?",
                (producto_id,)
            )
            producto = cursor.fetchone()

            if producto is None:
                raise ValueError("Producto no encontrado.")

            existencia = producto[0]

            if tipo == "salida" and cantidad > existencia:
                raise ValueError("No hay suficiente mercancía.")

            nueva_cantidad = (
                existencia + cantidad
                if tipo == "entrada"
                else existencia - cantidad
            )

            conexion.execute("""
                UPDATE productos SET cantidad = ?
                WHERE id = ?
            """, (nueva_cantidad, producto_id))

    def obtener_estadisticas(self):
        with conectar() as conexion:
            cursor = conexion.execute("""
                SELECT
                    COUNT(*),
                    COALESCE(SUM(cantidad), 0),
                    COALESCE(SUM(precio * cantidad), 0),
                    COALESCE(SUM(
                        CASE WHEN cantidad <= 5 THEN 1 ELSE 0 END
                    ), 0)
                FROM productos
            """)
            total, unidades, valor, stock_bajo = cursor.fetchone()

            return {
                "productos": total,
                "unidades": unidades,
                "valor": valor,
                "stock_bajo": stock_bajo
            }
