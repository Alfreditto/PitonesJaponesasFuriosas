import json


class Pelicula:
    def __init__(self, codigo, titulo, fecha_salida, director, personajes, vehiculos) -> None:
        self.codigo = codigo
        self.titulo = titulo
        self.fecha_salida = fecha_salida
        self.director = director
        self.personajes = personajes
        self.vehiculos = vehiculos


    def __str__(self) -> str:
        return f"Codigo: {self.codigo}, Titulo: {self.titulo}, Fecha de salida: {self.fecha_salida}, Director: {self.director}, Personajes: {self.personajes}, Vehiculos: {self.vehiculos}"

