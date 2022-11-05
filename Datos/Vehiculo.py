from Datos.Personaje import Personaje


class Vehiculo:
    def __init__(self, codigo, nombre,
                 piloto: Personaje) -> None:
        self.codigo = codigo
        self.nombre = nombre
        self.piloto = piloto
