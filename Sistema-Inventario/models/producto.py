
from dataclasses import dataclass

@dataclass
class Producto:
    codigo: str
    nombre: str
    categoria: str
    precio: float
    cantidad: int
    id: int | None = None
