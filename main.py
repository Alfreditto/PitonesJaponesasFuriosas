import json

from Datos.Pelicula import Pelicula
from Datos.Personaje import Personaje
from Datos.Vehiculo import Vehiculo


def cargar():
    opcion_carga = input("Cargar los datos borrara el registro local, ¿desea continuar? (S/N): ")
    if opcion_carga == "S":
        pelis_ex = json.load(open("peliculas.json"))
        for peli in pelis_ex:
            peli = Pelicula(pelis_ex["codigo"], pelis_ex["titulo"], pelis_ex["fecha_salida"], pelis_ex["director"],
                            pelis_ex["personajes"],
                            pelis_ex["vehiculos"])
            peliculas.append(peli)

        personajes_ex = json.load(open("personajes.json"))
        for personaje in personajes_ex:
            pers = Personaje(personaje["codigo"], personaje["nombre"], personaje["genero"], personaje["edad"],
                             personaje["pelicula"], personaje["especie"])
            personajes.append(pers)


def guardar(peliculas, personajes, vehiculos):
    pelis_g = []

    for pelicula in peliculas:
        pelis_g.append(pelicula.__dict__)
    json.dump(pelis_g, open("peliculas.json", "w"))

    personajes_g = []
    for personaje in personajes:
        personajes_g.append(personaje.__dict__)
    json.dump(personajes_g, open("personajes.json", "w"))

    vehiculos_g = []
    for vehiculo in vehiculos:
        vehiculos_g.append(vehiculo.__dict__)
    json.dump(vehiculos_g, open("vehiculos.json", "w"))


def mostrar(peliculas):
    for pelicula in peliculas:
        print(pelicula.__str__())


def crear_personajes():
    personajes = [Personaje] * 0
    print("Introduzca los personajes de la pelicula, dejar en blanco para terminar")
    personaje = input("Personaje: ")
    while personaje != "":
        personajes.append(personaje)
        personaje = input("Personaje: ")
    return personajes


def crear_vehiculos():
    vehiculos = []
    print("Introduzca los vehiculos de la pelicula, dejar en blanco para terminar")
    vehiculo = input("Vehiculo: ")
    while vehiculo != "":
        vehiculos.append(vehiculo)
        vehiculo = input("Vehiculo: ")
    return vehiculos


def añadir(peliculas):
    pelicula = Pelicula(input("Codigo: "), input("Titulo: "), input("Fecha de salida: "), input("Director: "),
                        crear_personajes(), crear_vehiculos())
    if pelicula.codigo not in peliculas:
        peliculas.append(pelicula)
    else:
        print("La pelicula ya existe")


def eliminar(peliculas):
    codigo = input("Introduzca el codigo de la pelicula a eliminar: ")
    for pelicula in peliculas:
        if pelicula.codigo == codigo:
            peliculas.remove(pelicula)
            print("Pelicula eliminada")
            return
    print("La pelicula no existe")


if __name__ == '__main__':
    peliculas = [Pelicula("1", "Star Wars", "1977", "George Lucas", ["Luke Skywalker", "Han Solo", "Leia Organa"],
                          ["Millenium Falcon", "X-Wing", "TIE Fighter"]),
                 Pelicula("2", "Star Wars", "1977", "George Lucas", ["Luke Skywalker", "Han Solo", "Leia Organa"],
                          ["Millenium Falcon", "X-Wing", "TIE Fighter"])]
    personajes = [Personaje] * 0
    vehiculos = [Vehiculo] * 0
    opcion = -1
    while opcion != 7:
        opcion = int(input("1. Cargar Peliculas\n"
                           "2. Guardar Peliculas\n"
                           "3. Añadir Peliculas\n"
                           "4. Eliminar Peliculas\n"
                           "5. Modificar Peliculas\n"
                           "6. Mostrar Peliculas\n"
                           "7. Salir\n"))
        match opcion:
            case 1:
                cargar()
            case 2:
                guardar(peliculas)
            case 3:
                pass
                añadir(peliculas)
            case 4:
                pass
                # eliminar(peliculas)
            case 5:
                pass
                # modificar(peliculas)
            case 6:
                pass
                mostrar(peliculas)
            case 7:
                print("Saliendo...")
            case _:
                print("Opcion no valida")
