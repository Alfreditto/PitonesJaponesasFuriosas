from Datos.Especie import Especie


class Personaje:
    def __init__(self, codigo, nombre,
                 genero, edad, especie: Especie) -> None:
        self.codigo = codigo
        self.nombre = nombre
        self.genero = genero
        self.edad = edad
        self.especie = especie

    def __str__(self) -> str:
        return f"Codigo: {self.codigo}, Nombre: {self.nombre}, Genero: {self.genero}, Edad: {self.edad}, Especie: {self.especie}"
