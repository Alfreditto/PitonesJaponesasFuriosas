import datetime
import json

from Datos.Pelicula import Pelicula
from Datos.Personaje import Personaje
from Datos.Vehiculo import Vehiculo


def borrar_bbdd(peliculas):
    peliculas.clear()


def cargar_personajes(list_personajes):
    personajes = []
    for personaje in list_personajes:
        personaje = Personaje(personaje['codigo'], personaje['nombre'], personaje['genero'], personaje['edad'],
                              personaje['especie'])
        personajes.append(personaje)
    return personajes


def cargar_vehiuclos(list_vehiculos):
    vehiculos = []
    for vehiculo in list_vehiculos:
        vehiculo = Vehiculo(vehiculo['codigo'], vehiculo['nombre'], vehiculo['piloto'])
        vehiculos.append(vehiculo)
    return vehiculos


def cargar(peliculas):
    # Esto de borrar la BBDD no me termina de convencer, a ver como lo decides dejar (～￣▽￣)～
    opcion_carga = input("Cargar los datos borrara el registro local, ¿desea continuar? (S/N): ").upper()
    if opcion_carga == "S":
        borrar_bbdd(peliculas)
        try:
            with open('peliculas.json', 'r') as f:
                peli_estr = json.load(f)
                print(type(peli_estr))
                for peli in peli_estr:
                    personajes = cargar_personajes(peli['personajes'])
                    vehiculos = cargar_vehiuclos(peli['vehiculos'])
                    aux = Pelicula(peli['codigo'], peli['titulo'], peli['fecha_salida'], peli['director'],
                                   personajes, vehiculos)
                    peliculas.append(aux)
        except json.decoder.JSONDecodeError:
            print("JSON invalido")
            # Hacemos otra limpieza por si se añadió algo corrupto
            borrar_bbdd(peliculas)

    else:
        print("Carga cancelada")


def guardar(list_peliculas):
    # Serializamos las peliculas
    peliculas_estr = []
    for peli in list_peliculas:
        peliculas_estr.append(peli.__dict__)

    # Luego con las peliculas serializadas, vamos a serializar los personajes y vehiculos
    for peli in peliculas_estr:
        # Serializamos los personajes
        personajes = []
        for personaje in peli['personajes']:
            personajes.append(personaje.__dict__)
        peli['personajes'] = personajes

        # Serializamos los vehiculos
        vehiculos = []
        for vehiculo in peli['vehiculos']:
            vehiculos.append(vehiculo.__dict__)
        peli['vehiculos'] = vehiculos
        # serializamos al piloto del vehiculo
        for vehiculo in peli['vehiculos']:
            if vehiculo['piloto'] is not None:
                vehiculo['piloto'] = vehiculo['piloto'].__dict__

    # Guardamos el JSON
    with open('peliculas.json', 'w') as f:
        json.dump(peliculas_estr, f)


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
            try:
                edad = int(input("Edad: "))
            except ValueError:
                print("La edad debe ser un numero")
                edad = ""
            especie = input("Especie: ")
            if nombre and genero and edad and especie != "":
                personaje = Personaje(codigo, nombre, genero, edad, especie)
                personajes.append(personaje)
            else:
                print("No se puede crear un personaje con campos vacios/invalidos")

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

        try:
            fecha_salida = input("Introduzca la fecha de salida de la pelicula (dd/mm/aaaa): ")
            fecha_salida = datetime.datetime.date(datetime.datetime.strptime(fecha_salida, "%d/%m/%Y")).isoformat()

        except ValueError:
            print("Datos invalidos, por favor, introduzca los datos como se indica")
            print("Se pondra la fecha de hoy")
            fecha_salida = datetime.datetime.date(datetime.datetime.now()).isoformat()

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
        try:
            opcion = int(input("¿Que desea modificar?"
                               "1. Titulo"
                               "2. Fecha de salida"
                               "3. Director"))
            assert isinstance(pelicula, Pelicula)
            match opcion:
                case 1:
                    pelicula.titulo = input("Introduzca el nuevo titulo: ")
                case 2:
                    try:
                        fecha_salida = input("Introduzca la nueva fecha de salida (dd/mm/aaaa): ")
                        pelicula.fecha_salida = datetime.datetime.strptime(fecha_salida, "%d/%m/%Y")
                    except ValueError:
                        print("Fecha invalida, se mantiene la anterior")
                case 3:
                    pelicula.director = input("Introduzca el nuevo director: ")
                case _:
                    print("Opcion no valida")
        except ValueError:
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
            try:
                opcion = int(input("¿Que desea modificar?"
                                   "1. Nombre"
                                   "2. Genero"
                                   "3. Edad"
                                   "4. Especie"))
                assert isinstance(personaje, Personaje)
                match opcion:
                    case 1:
                        personaje.nombre = input("Introduzca el nuevo nombre: ")
                    case 2:
                        personaje.genero = input("Introduzca el nuevo genero: ")
                    case 3:
                        try:
                            personaje.edad = int(input("Introduzca la nueva edad: "))
                        except ValueError:
                            print("Edad invalida, se mantiene la anterior")
                    case 4:
                        personaje.especie = input("Introduzca la nueva especie: ")
                    case _:
                        print("Opcion no valida")
            except ValueError:
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
            try:
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
            except ValueError:
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
        try:
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
                        assert isinstance(pelicula, Pelicula)
                        print(pelicula)

                        print("Personajes:")
                        for personaje in pelicula.personajes:
                            assert isinstance(personaje, Personaje)
                            print(personaje)

                        print("Vehiculos:")
                        for vehiculo in pelicula.vehiculos:
                            assert isinstance(vehiculo, Vehiculo)
                            print(vehiculo)
                case 7:
                    print("Saliendo...")
                case _:
                    print("Opcion no valida")
        except ValueError:
            print("Opcion no valida")
