import json

from Datos.Pelicula import Pelicula


def cargar():
    opcion_carga = input("Cargar los datos borrara el registro local, ¿desea continuar? (S/N): ")
    if opcion_carga == "S":
        data = json.load(open("peliculas.json"))
        peli = Pelicula(data["codigo"], data["titulo"], data["fecha_salida"], data["director"], data["personajes"],
                        data["vehiculos"])
        peliculas.append(peli)


def guardar(peliculas):
    for pelicula in peliculas:
        if type(pelicula) is Pelicula:
            with open("peliculas.json", "w", encoding="utf-8") as f:
                json.dump(pelicula.__dict__, f, ensure_ascii=False, indent=4)


def mostrar(peliculas):
    for pelicula in peliculas:
        print(pelicula.__str__())


def crear_personajes():
    personajes = []
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
    peliculas = [Pelicula] * 0
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
                eliminar(peliculas)
            case 5:
                pass
                modificar(peliculas)
            case 6:
                pass
                mostrar(peliculas)
            case 7:
                print("Saliendo...")
            case _:
                print("Opcion no valida")
