from Datos.Pelicula import Pelicula
from Datos.Personaje import Personaje


class Vehiculo:
    def __init__(self, codigo, nombre,
                 pelicula: Pelicula, piloto: Personaje) -> None:
        self.codigo = codigo
        self.nombre = nombre
        self.pelicula = pelicula
        self.piloto = piloto
