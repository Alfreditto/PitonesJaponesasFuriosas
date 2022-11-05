import json

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
            peliculas.append(json.loads(open("peliculas.json", "r").read()))
        except json.decoder.JSONDecodeError:
            print("JSON invalido")
            # Hacemos otra limpieza por si se añadió algo corrupto
            borrar_bbdd(peliculas)
    else:
        print("Carga cancelada")


def guardar(peliculas):
    pelis_g = []

    for pelicula in peliculas:
        pelis_g.append(pelicula.__dict__)
    json.dump(pelis_g, open("peliculas.json", "w"))


def mostrar(peliculas):
    for pelicula in peliculas:
        print(pelicula.__str__())


def add_personaje(personajes, peli):
    codigo = input("Introduzca el codigo del personaje: ")
    nombre = input("Introduzca el nombre del personaje: ")
    genero = input("Introduzca el genero del personaje: ")
    edad = input("Introduzca la edad del personaje: ")
    pelicula = input("Introduzca el codigo de la pelicula del personaje: ")
    especie = input("Introduzca la especie del personaje: ").lower()
    personaje = Personaje(codigo, nombre, genero, edad, pelicula, Especie(especie))
    if personaje.codigo in personajes:
        print("Ya existe un personaje con ese codigo")
    else:
        pelicula = buscar_objeto(peli, pelicula)
        if pelicula is not None:
            peli.personajes.append(personaje)
            personajes.append(personaje)
        else:
            print("No existe la pelicula")


def add_vehiculo(vehiculos, peli, pers):
    codigo = input("Introduzca el codigo del vehiculo: ")
    nombre = input("Introduzca el nombre del vehiculo: ")
    pelicula = input("Introduzca el codigo de la pelicula del personaje: ")
    piloto = input("Introduzca el codigo del piloto del vehiculo (Personaje): ")
    vehiculo = Vehiculo(codigo, nombre, pelicula, piloto)
    pelicula = buscar_objeto(peli, pelicula)
    piloto = buscar_objeto(pers, piloto)
    if pelicula is not None and piloto is not None:
        vehiculos.append(vehiculo)
        peli.vehiculos.append(vehiculo)
        pers.vehiculos.append(vehiculo)
    else:
        print("No existe la pelicula o el personaje")


def añadir(peliculas, personajes, vehiculos):
    opcion = input("Que desea añadir? (Pelicula/Personaje/Vehiculo): ").lower()
    if opcion == "pelicula":
        add_pelicula(peliculas, personajes, vehiculos)
    elif opcion == "personaje":
        add_personaje(personajes, peliculas)
    elif opcion == "vehiculo":
        add_vehiculo(vehiculos, peliculas, personajes)
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
        objeto = buscar_objeto(lista_objetos, codigo)
        if objeto is not None:
            objs.append(objeto)
        codigo = input("Codigo: ")
    return objs


def add_pelicula(peliculas, personajes, vehiculos):
    codigo = input("Introduzca el codigo de la pelicula: ")
    titulo = input("Introduzca el titulo de la pelicula: ")
    fecha_salida = input("Introduzca la fecha de salida de la pelicula: ")
    director = input("Introduzca el director de la pelicula: ")
    print("Vamos a crear a los personajes")
    personajes = crear_objetos(personajes)
    print("Vamos a crear a los vehiculos")
    vehiculos = crear_objetos(vehiculos)
    pelicula = Pelicula(codigo, titulo, fecha_salida, director, personajes, vehiculos)
    if pelicula.codigo in peliculas:
        print("Ya existe una pelicula con ese codigo")
    else:
        peliculas.append(pelicula)


def eliminar_pelicula(peliculas):
    codigo = input("Introduzca el codigo de la pelicula a eliminar: ")
    pelicula = buscar_objeto(peliculas, codigo)
    if pelicula is not None:
        if len(pelicula.personajes) == 0 and len(pelicula.vehiculos) == 0:
            peliculas.remove(pelicula)
        else:
            print("No se puede eliminar una pelicula con personajes o vehiculos")


def eliminar_personaje(personajes):
    codigo = input("Introduzca el codigo del personaje a eliminar: ")
    personaje = buscar_objeto(personajes, codigo)
    if personaje is not None:
        for pelicula in personaje.peliculas:
            pelicula.personajes.remove(personaje)
        for vehiculo in personaje.vehiculos:
            vehiculo.piloto = None
        personajes.remove(personaje)


def eliminar_vehiculo(vehiculos):
    codigo = input("Introduzca el codigo del vehiculo a eliminar: ")
    vehiculo = buscar_objeto(vehiculos, codigo)
    if vehiculo is not None:
        if vehiculo.piloto is None:
            for pelicula in vehiculo.peliculas:
                pelicula.vehiculos.remove(vehiculo)
            vehiculos.remove(vehiculo)
        else:
            print("No se puede eliminar un vehiculo con piloto")


def eliminar(peliculas, personajes, vehiculos):
    opcion = input("Que desea eliminar? (Pelicula/Personaje/Vehiculo): ").lower()
    if opcion == "pelicula":
        eliminar_pelicula(peliculas)
    elif opcion == "personaje":
        eliminar_personaje(personajes)
    elif opcion == "vehiculo":
        eliminar_vehiculo(vehiculos)
    else:
        print("Opcion no valida")


def modificar_pelicula(peliculas):
    codigo = input("Introduzca el codigo de la pelicula a modificar: ")
    pelicula = buscar_objeto(peliculas, codigo)
    if pelicula is not None:
        pelicula.titulo = input("Introduzca el nuevo titulo de la pelicula: ")
        pelicula.fecha_salida = input("Introduzca la nueva fecha de salida de la pelicula: ")
        pelicula.director = input("Introduzca el nuevo director de la pelicula: ")


def modificar_personaje(personajes):
    codigo = input("Introduzca el codigo del personaje a modificar: ")
    personaje = buscar_objeto(personajes, codigo)
    if personaje is not None:
        personaje.nombre = input("Introduzca el nuevo nombre del personaje: ")
        personaje.fecha_nacimiento = input("Introduzca la nueva fecha de nacimiento del personaje: ")
        print("Vamos a añadir peliculas al personaje")
        personaje.peliculas = crear_objetos(personajes)
        print("Vamos a añadir vehiculos al personaje")
        personaje.vehiculos = crear_objetos(vehiculos)


def modificar_vehiculo(vehiculos):
    codigo = input("Introduzca el codigo del vehiculo a modificar: ")
    vehiculo = buscar_objeto(vehiculos, codigo)
    if vehiculo is not None:
        vehiculo.nombre = input("Introduzca el nuevo nombre del vehiculo: ")
        vehiculo.fecha_creacion = input("Introduzca la nueva fecha de creacion del vehiculo: ")
        vehiculo.piloto = buscar_objeto(personajes, input("Introduzca el codigo del nuevo piloto: "))
        print("Vamos a añadir peliculas al vehiculo")
        vehiculo.peliculas = crear_objetos(peliculas)


def modificar(peliculas, personajes, vehiculos):
    opcion = input("Que desea modificar? (Pelicula/Personaje/Vehiculo): ").lower()
    if opcion == "pelicula":
        modificar_pelicula(peliculas)
    elif opcion == "personaje":
        modificar_personaje(personajes)
    elif opcion == "vehiculo":
        modificar_vehiculo(vehiculos)
    else:
        print("Opcion no valida")


if __name__ == '__main__':
    peliculas = [Pelicula] * 0
    personajes = [Personaje] * 0
    vehiculos = [Vehiculo] * 0
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
                guardar(peliculas, personajes, vehiculos)
            case 3:
                pass
                añadir(peliculas, personajes, vehiculos)
            case 4:
                pass
                eliminar(peliculas, personajes, vehiculos)
            case 5:
                pass
                modificar(peliculas, personajes, vehiculos)
            case 6:
                pass
                mostrar(peliculas)
            case 7:
                print("Saliendo...")
            case _:
                print("Opcion no valida")
