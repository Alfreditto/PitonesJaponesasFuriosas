import json

import jsonpickle as jsonpickle

from Datos.Especie import Especie
from Datos.Pelicula import Pelicula
from Datos.Personaje import Personaje
from Datos.Vehiculo import Vehiculo


def borrar_bbdd(peliculas):
    peliculas.clear()


def cargar(peliculas):
    # Esto de borrar la BBDD no me termina de convencer, a ver como lo decides dejar (～￣▽￣)～
    opcion_carga = input("Cargar los datos borrara el registro local, ¿desea continuar? (S/N): ").upper()
    if opcion_carga == "S":
        borrar_bbdd(peliculas)
        try:
            with open('peliculas.json', 'r') as f:
                peli_estr = jsonpickle.decode(f.read())
            for peli in peli_estr:
                assert isinstance(peli, Pelicula)
                peliculas.append(peli)
        except json.decoder.JSONDecodeError:
            print("JSON invalido")
            # Hacemos otra limpieza por si se añadió algo corrupto
            borrar_bbdd(peliculas)

    else:
        print("Carga cancelada")


def guardar(list_peliculas):
    with open('peliculas.json', 'w') as f:
        f.write(jsonpickle.encode(list_peliculas))


def buscar_objeto(lista, codigo):
    for objeto in lista:
        if objeto.codigo == codigo:
            return objeto
    return None


def crear_objetos(lista_objetos):
    objs = []
    print("Introduce el codigo, deja en blanco para terminar")
    codigo = input("Codigo: ")
    while codigo != "":
        objeto = buscar_objeto(lista_objetos, codigo)
        if objeto is not None:
            objs.append(objeto)
        codigo = input("Codigo: ")
    return objs


def crear_personajes():
    personajes = []
    print("Introduce el codigo del personaje, deja en blanco para terminar")
    codigo = input("Codigo: ")
    while codigo != "":
        if buscar_objeto(personajes, codigo) is not None:
            print("Ya existe un personaje con ese codigo")
        else:
            nombre = input("Nombre: ")
            genero = input("Genero: ")
            edad = input("Edad: ")
            especie = None
            while especie is None:
                try:
                    especie = Especie(input("Especie: (Humano, Espiritu, Dios, Totoro, Gato)").lower())
                except ValueError:
                    print("Especie invalida")
                    especie = None
            if nombre and genero and edad != "":
                personaje = Personaje(codigo, nombre, genero, edad, especie)
                personajes.append(personaje)
            else:
                print("No se puede crear un personaje con campos vacios")

        codigo = input("Codigo: ")

    return personajes


def crear_vehiculos(personajes_peli):
    vehiculos = []
    print("Introduce el codigo del vehiculo, deja en blanco para terminar")
    codigo = input("Codigo: ")
    while codigo != "":
        if buscar_objeto(vehiculos, codigo) is not None:
            print("Ya existe un vehiculo con ese codigo")
        else:
            nombre = input("Nombre: ")
            piloto = None
            while piloto is None:
                codigo_piloto = input("Codigo del piloto: ")
                personaje = buscar_objeto(personajes_peli, codigo_piloto)
                if personaje is not None:
                    piloto = personaje
                else:
                    print("No existe un personaje con ese codigo")
            if nombre != "":
                vehiculo = Vehiculo(codigo, nombre, piloto)
                vehiculos.append(vehiculo)
            else:
                print("No se puede crear un vehiculo con campos vacios")

        codigo = input("Codigo: ")

    return vehiculos


def add_pelicula(list_peliculas):
    codigo = input("Introduzca el codigo de la pelicula: ")
    if buscar_objeto(list_peliculas, codigo) is not None:
        print("Ya existe una pelicula con ese codigo")
    else:
        titulo = input("Introduzca el titulo de la pelicula: ")
        fecha_salida = input("Introduzca la fecha de salida de la pelicula: ")
        director = input("Introduzca el director de la pelicula: ")
        print("Vamos a crear a los personajes")
        personajes = crear_personajes()
        print("Vamos a crear a los vehiculos")
        vehiculos = crear_vehiculos(personajes)
        pelicula = Pelicula(codigo, titulo, fecha_salida, director, personajes, vehiculos)
        list_peliculas.append(pelicula)


def add_personaje(list_peliculas):
    codigo_pelicula = input("Introduzca el codigo de la pelicula: ")
    pelicula = buscar_objeto(list_peliculas, codigo_pelicula)
    if pelicula is not None:
        personajes = crear_personajes()
        for personaje in personajes:
            assert isinstance(pelicula, Pelicula)
            pelicula.personajes.append(personaje)
    else:
        print("No existe una pelicula con ese codigo")


def add_vehiculo(list_peliculas):
    codigo_pelicula = input("Introduzca el codigo de la pelicula: ")
    pelicula = buscar_objeto(list_peliculas, codigo_pelicula)
    if pelicula is not None:
        vehiculos = crear_vehiculos(pelicula.personajes)
        for vehiculo in vehiculos:
            assert isinstance(pelicula, Pelicula)
            pelicula.vehiculos.append(vehiculo)
    else:
        print("No existe una pelicula con ese codigo")


def annadir(peliculas):
    print("¿Que desea añadir? (Pelicula, Personaje, Vehiculo)")
    opcion = input("Opcion: ").lower()
    match opcion:
        case "pelicula":
            add_pelicula(peliculas)
        case "personaje":
            add_personaje(peliculas)
        case "vehiculo":
            add_vehiculo(peliculas)
        case _:
            print("Opcion invalida")


def eliminar_pelicula(list_peliculas):
    codigo = input("Introduzca el codigo de la pelicula a eliminar: ")
    pelicula = buscar_objeto(list_peliculas, codigo)
    if pelicula is None:
        print("No existe una pelicula con ese codigo")
    else:
        if len(pelicula.personajes) == 0 and len(pelicula.vehiculos) == 0:
            list_peliculas.remove(pelicula)
        else:
            print("No se puede eliminar una pelicula con personajes o vehiculos")


def buscar_vehiculo_pilotado(vehiculos, codigo):
    for vehiculo in vehiculos:
        if vehiculo.piloto.codigo == codigo:
            return vehiculo
    return None


def eliminar_personaje(list_peliculas):
    codigo_peli = input("Introduzca el codigo de la pelicula: ")
    pelicula = buscar_objeto(list_peliculas, codigo_peli)
    if pelicula is None:
        print("No existe una pelicula con ese codigo")
    else:
        codigo = input("Introduzca el codigo del personaje a eliminar: ")
        assert isinstance(pelicula, Pelicula)
        personaje = buscar_objeto(pelicula.personajes, codigo)
        if personaje is None:
            print("No existe un personaje con ese codigo")
        else:
            if pelicula.vehiculos is None:
                pelicula.personajes.remove(personaje)
            else:
                vehiculo = buscar_vehiculo_pilotado(pelicula.vehiculos, personaje.codigo)
                if vehiculo is not None:
                    print("No se puede eliminar un personaje que pilotea un vehiculo")
                else:
                    pelicula.personajes.remove(personaje)


def eliminar_vehiculo(list_peliculas):
    codigo_peli = input("Introduzca el codigo de la pelicula: ")
    pelicula = buscar_objeto(list_peliculas, codigo_peli)
    if pelicula is None:
        print("No existe una pelicula con ese codigo")
    else:
        codigo = input("Introduzca el codigo del vehiculo a eliminar: ")
        assert isinstance(pelicula, Pelicula)
        vehiculo = buscar_objeto(pelicula.vehiculos, codigo)
        if vehiculo is None:
            print("No existe un vehiculo con ese codigo")
        else:
            pelicula.vehiculos.remove(vehiculo)


def eliminar(list_peliculas):
    opcion = input("Que desea eliminar? (Pelicula/Personaje/Vehiculo): ").lower()
    if opcion == "pelicula":
        eliminar_pelicula(list_peliculas)
    elif opcion == "personaje":
        eliminar_personaje(list_peliculas)
    elif opcion == "vehiculo":
        eliminar_vehiculo(list_peliculas)
    else:
        print("Opcion no valida")


def modificar_pelicula(list_peliculas):
    codigo = input("Introduzca el codigo de la pelicula a modificar: ")
    pelicula = buscar_objeto(list_peliculas, codigo)
    if pelicula is None:
        print("No existe una pelicula con ese codigo")
    else:
        opcion = int(input("¿Que desea modificar?"
                           "1. Titulo"
                           "2. Fecha de salida"
                           "3. Director"))
        assert isinstance(pelicula, Pelicula)
        match opcion:
            case 1:
                pelicula.titulo = input("Introduzca el nuevo titulo: ")
            case 2:
                pelicula.fecha_salida = input("Introduzca la nueva fecha de salida: ")
            case 3:
                pelicula.director = input("Introduzca el nuevo director: ")
            case _:
                print("Opcion no valida")


def modificar_personaje(list_peliculas):
    codigo_peli = input("Introduzca el codigo de la pelicula: ")
    pelicula = buscar_objeto(list_peliculas, codigo_peli)
    if pelicula is None:
        print("No existe una pelicula con ese codigo")
    else:
        codigo = input("Introduzca el codigo del personaje a modificar: ")
        assert isinstance(pelicula, Pelicula)
        personaje = buscar_objeto(pelicula.personajes, codigo)
        if personaje is None:
            print("No existe un personaje con ese codigo")
        else:
            opcion = int(input("¿Que desea modificar?"
                               "1. Nombre"
                               "2. Genero"
                               "3. Especie"
                               ))
            assert isinstance(personaje, Personaje)
            match opcion:
                case 1:
                    personaje.nombre = input("Introduzca el nuevo nombre: ")
                case 2:
                    personaje.genero = input("Introduzca el nuevo genero: ")
                case 3:
                    try:
                        personaje.especie = Especie(input("Introduzca la nueva especie: "))
                    except ValueError:
                        print("Especie no valida")
                case _:
                    print("Opcion no valida")


def modificar_vehiculo(list_peliculas):
    codigo_peli = input("Introduzca el codigo de la pelicula: ")
    pelicula = buscar_objeto(list_peliculas, codigo_peli)
    if pelicula is None:
        print("No existe una pelicula con ese codigo")
    else:
        codigo = input("Introduzca el codigo del vehiculo a modificar: ")
        assert isinstance(pelicula, Pelicula)
        vehiculo = buscar_objeto(pelicula.vehiculos, codigo)
        if vehiculo is None:
            print("No existe un vehiculo con ese codigo")
        else:
            opcion = int(input("¿Que desea modificar?"
                               "1. Nombre"
                               "3. Piloto"
                               ))
            assert isinstance(vehiculo, Vehiculo)
            match opcion:
                case 1:
                    vehiculo.nombre = input("Introduzca el nuevo nombre: ")
                case 2:
                    codigo_pilot = input("Introduzca el codigo del nuevo piloto: ")
                    personaje = buscar_objeto(pelicula.personajes, codigo_pilot)
                    if personaje is None:
                        print("No existe un personaje con ese codigo")
                    else:
                        vehiculo.piloto = personaje
                case _:
                    print("Opcion no valida")


def modificar(peliculas):
    opcion = input("Que desea modificar? (Pelicula/Personaje/Vehiculo): ").lower()
    if opcion == "pelicula":
        modificar_pelicula(peliculas)
    elif opcion == "personaje":
        modificar_personaje(peliculas)
    elif opcion == "vehiculo":
        modificar_vehiculo(peliculas)
    else:
        print("Opcion no valida")


if __name__ == '__main__':
    peliculas = [Pelicula] * 0
    opcion = -1
    while opcion != 7:
        opcion = int(input("1. Cargar\n"
                           "2. Guardar\n"
                           "3. Añadir\n"
                           "4. Eliminar\n"
                           "5. Modificar\n"
                           "6. Mostrar\n"
                           "7. Salir\n"))
        match opcion:
            case 1:
                cargar(peliculas)
            case 2:
                guardar(peliculas)
            case 3:
                annadir(peliculas)
            case 4:
                eliminar(peliculas)
            case 5:
                modificar(peliculas)
            case 6:
                for pelicula in peliculas:
                    print(pelicula.__str__())
            case 7:
                print("Saliendo...")
            case _:
                print("Opcion no valida")
