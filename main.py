import json

from Datos.Especie import Especie
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

        vehiculos_ex = json.load(open("vehiculos.json"))
        for vehiculo in vehiculos_ex:
            vehi = Vehiculo(vehiculo["codigo"], vehiculo["nombre"], vehiculo["tipo"], vehiculo["pelicula"])
            vehiculos.append(vehi)


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


def add_personaje(personajes):
    codigo = input("Introduzca el codigo del personaje: ")
    nombre = input("Introduzca el nombre del personaje: ")
    genero = input("Introduzca el genero del personaje: ")
    edad = input("Introduzca la edad del personaje: ")
    pelicula = input("Introduzca la pelicula del personaje: ")
    especie = input("Introduzca la especie del personaje: ").lower()
    personaje = Personaje(codigo, nombre, genero, edad, pelicula, Especie(especie))
    if personaje.codigo in personajes:
        print("Ya existe un personaje con ese codigo")
    else:
        personajes.append(personaje)


def add_vehiculo(vehiculos):
    codigo = input("Introduzca el codigo del vehiculo: ")
    nombre = input("Introduzca el nombre del vehiculo: ")
    tipo = input("Introduzca el tipo del vehiculo: ")
    pelicula = input("Introduzca la pelicula del vehiculo: ")
    vehiculo = Vehiculo(codigo, nombre, tipo, pelicula)
    if vehiculo.codigo in vehiculos:
        print("Ya existe un vehiculo con ese codigo")
    else:
        vehiculos.append(vehiculo)


def añadir(peliculas, personajes, vehiculos):
    opcion = input("Que desea añadir? (Pelicula/Personaje/Vehiculo): ").lower()
    if opcion == "pelicula":
        add_pelicula(peliculas, personajes, vehiculos)
    elif opcion == "personaje":
        add_personaje(personajes)
    elif opcion == "vehiculo":
        add_vehiculo(vehiculos)
    else:
        print("Opcion no valida")


def buscar_objeto(lista_objetos, codigo):
    for objeto in lista_objetos:
        if objeto.codigo == codigo:
            return objeto
    print("No existe")
    return None


def crear_objetos(lista_objetos):
    objs = []
    print("Introduce el codigo, deja en blanco para terminar")
    codigo = input("Codigo: ")
    while codigo != "":
        vehiculo = buscar_objeto(lista_objetos, codigo)
        if vehiculo is not None:
            objs.append(vehiculo)
        codigo = input("Codigo: ")
    return objs


def add_pelicula(peliculas, personajes, vehiculos):
    codigo = input("Introduzca el codigo de la pelicula: ")
    titulo = input("Introduzca el titulo de la pelicula: ")
    fecha_salida = input("Introduzca la fecha de salida de la pelicula: ")
    director = input("Introduzca el director de la pelicula: ")
    personajes = crear_objetos(personajes)
    vehiculos = crear_objetos(vehiculos)
    pelicula = Pelicula(codigo, titulo, fecha_salida, director, personajes, vehiculos)
    if pelicula.codigo in peliculas:
        print("Ya existe una pelicula con ese codigo")
    else:
        peliculas.append(pelicula)


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
                añadir(peliculas, personajes, vehiculos)
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
