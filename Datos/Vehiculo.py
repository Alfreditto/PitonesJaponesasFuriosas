from Datos.Personaje import Personaje


class Vehiculo:
    def __init__(self, codigo, nombre,
                 piloto: Personaje) -> None:
        self.codigo = codigo
        self.nombre = nombre
        self.piloto = piloto

    def __str__(self) -> str:
        return f"Codigo: {self.codigo}, Nombre: {self.nombre}, Piloto: {self.piloto}"
        