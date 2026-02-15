import json
import logging

# funcion de logging
# Esto crea el fichero 'registro.log' donde se apuntará todo lo que pase
logging.basicConfig(
    filename='registro.log',
    level=logging.INFO,  # Guardará info, warnings y errores
    format='%(asctime)s - %(levelname)s - %(message)s',  # Formato: Fecha - Nivel - Mensaje
    filemode='a'  # 'a' significa append (añadir al final sin borrar lo anterior, como en tema 5 de cliente)
)

"""
PLANIFICACIÓN DEL PROYECTO Y NOTAS:

Valores de Transfermarkt: con un scraper o alguna api de github (gratuita) puedo conseguir los datos (datos en millones de euros).
Posición: catalogaré todos los jugadores que tengan "extremo" como delanteros con un .split o algo parecido. Igual con laterales y carrileros como defensas y demás posiciones en mediocampo.
Extracomunitarios: máximo 3 por equipo.
Puedo crear un conjunto con los países comunitarios que vaya clasificando a los jugadores según su país de nacimiento (o si tienen doble nacionalidad) en comunitarios o no recorriendo el conjunto con el país del jugador como valor.


Nota: si bien ahora mismo el ejercicio cumple más o menos con lo estipulado, de cara al final del proyecto quiero que sea de otra manera, más bien como explico arriba, 
es decir, ahora mismo es un organizador de jugadores que tú mismo añades, con alguna floritura. Lo que yo busco que acabe siendo es una especie de buscador de jugadores con
filtros y búsquedas en google que ayuden a que los datos sean veraces y actualizados. Pero eso ahora mismo es, de momento, inviable. Para enero o febrero ya estará como quiero que
esté, además añadiendo todo lo que se ha pedido en la propia asignatura y en la tarea, claro.
"""

comunitarios = ["España", "Alemania", "Austria", "Bélgica", "Bulgaria", "Chequia", "Chipre", "Croacia", "Dinamarca",
                "Eslovaquia", "Eslovenia", "Estonia", "Finlandia", "Francia", "Grecia", "Hungría", "Irlanda", "Italia",
                "Letonia", "Lituania", "Luxemburgo", "Malta", "Países Bajos", "Polonia", "Portugal", "Rumanía",
                "Suecia"]

# Lista principal donde guardaremos todos los jugadores
plantilla = []
ARCHIVO_JSON = "plantilla.json"

# --- FUNCIONES AUXILIARES (Movidas arriba para que las Clases puedan usarlas) ---

def esCom(pais):
    """ Verifica si un país es extracomunitario o no basándose en la lista. """
    if pais in comunitarios:
        return False
    else:
        return True

def posicionGeneral(posEspecifica):
    """ Calcula la demarcación general. """
    pos = posEspecifica.lower()

    if "defensa" in pos or "lateral" in pos or "carrilero" in pos or "central" in pos:
        return "Defensa"
    elif "medio" in pos or "pivote" in pos or "interior" in pos or "volante" in pos:
        return "Centrocampista"
    elif "delantero" in pos or "extremo" in pos or "punta" in pos or "delantero" in pos:
        return "Delantero"
    else:
        return "Desconocido"

# --- CLASES Y HERENCIA ---

class Jugador:
    def __init__(self, nombre, edad, valorMercado, posicion, nacionalidad):
        self.nombre = nombre
        self.edad = edad
        self.valorMercado = valorMercado
        self.posicion = posicion
        self.nacionalidad = nacionalidad
        # Calculamos atributos derivados automáticamente al crear el objeto
        self.esComunitario = not esCom(nacionalidad) # True si es comunitario (False si esCom devuelve True)
        self.demarcacion = posicionGeneral(posicion)

    def __str__(self):
        return f"Nombre: {self.nombre}\nEdad: {self.edad}\nValor: {self.valorMercado}"
    
    # Necesario para que funcione el .sort() en generar_reporte
    def __lt__(self, other):
        return self.valorMercado < other.valorMercado

"""Pregunta 1 herencia y especialización"""
class Crack(Jugador):
    def __init__(self, nombre, edad, valorMercado, posicion, nacionalidad, esCrack):
        # Llamamos al constructor del padre (Jugador) para inicializar lo básico
        super().__init__(nombre, edad, valorMercado, posicion, nacionalidad)
        self.esCrack = esCrack # Atributo específico de esta subclase

    def __str__(self):
        # Sobreescribimos el string para mostrar que es un crack
        return f"Nombre: {self.nombre}\nEdad: {self.edad}\nValor: {self.valorMercado}\n🌟 Estatus: {self.esCrack}"

"""Pregunta 3 Gestión de datos"""

def generar_reporte():
    # Creamos una copia para no alterar el orden de la lista original
    plantilla_ordenada = plantilla.copy()
    plantilla_ordenada.sort() # Usa el método __lt__ de la clase para ordenar por precio
    
    print("\n--- REPORTE ORDENADO POR VALOR ---")
    contador = 0
    acumulado = 0
    for jugador in plantilla_ordenada:
        print("----------------")
        print(jugador) # Llama automáticamente a __str__
        contador = contador+1
        acumulado = acumulado + jugador.valorMercado # Acceso por punto
    print("----------------")
    print(f"El valor acumulado de los jugadores en plantilla es de: {acumulado} M")


# funciones json

def guardar_json():
    """ Escribe la lista plantilla en el fichero JSON convirtiendo objetos a dicts """
    try:
        with open(ARCHIVO_JSON, 'w', encoding='utf-8') as f:
            # Convertimos cada OBJETO a diccionario usando .__dict__ antes de guardar
            lista_para_guardar = [j.__dict__ for j in plantilla]
            json.dump(lista_para_guardar, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Error al guardar el fichero: {e}")
        logging.error("Fallo crítico al intentar guardar en JSON", exc_info=True)


def cargar_json():
    """ Lee el fichero JSON y convierte los diccionarios de vuelta a Objetos """
    global plantilla
    plantilla = [] # Limpiamos la lista antes de cargar
    try:
        with open(ARCHIVO_JSON, 'r', encoding='utf-8') as f:
            datos_brutos = json.load(f) # Esto es una lista de diccionarios
            
            # Reconstruimos los objetos
            for d in datos_brutos:
                # Comprobamos si tiene el campo 'esCrack' para saber qué clase crear
                if "esCrack" in d:
                    nuevo_j = Crack(d["nombre"], d["edad"], d["valorMercado"], d["posicion"], d["nacionalidad"], d["esCrack"])
                else:
                    nuevo_j = Jugador(d["nombre"], d["edad"], d["valorMercado"], d["posicion"], d["nacionalidad"])
                
                plantilla.append(nuevo_j)
                
            logging.info(f"Datos cargados correctamente. {len(plantilla)} jugadores en memoria.")

    except FileNotFoundError:
        logging.warning("Fichero JSON no encontrado. Se inicia con datos por defecto.")
        # Creamos el objeto inicial usando la Clase
        jugador_inicial = Jugador("Lamine Yamal", 18, 200, "Extremo derecho", "España")
        plantilla.append(jugador_inicial)
        guardar_json()
    except json.JSONDecodeError:
        logging.error("JSON corrupto.", exc_info=True)


def fCupo():
    """ Calcula si la plantilla cumple el cupo  """
    try:
        extraCom = int(input("¿Cuántos extracomunitarios tienes YA en el equipo (fuera de esta app)? "))
    except ValueError:
        print("Error: Debes introducir un número.")
        logging.error("Error en fCupo: El usuario introdujo un valor no numérico.", exc_info=True)
        return

    nuevos = 0
    for jugador in plantilla:
        # Usamos el atributo calculado en la clase
        if not jugador.esComunitario:
            nuevos = nuevos + 1

    total = extraCom + nuevos

    # Registro el cálculo en el log
    logging.info(f"Cálculo de cupo realizado. Total: {total}")

    if total > 3:
        print("Error, tendrías " + str(total) + " extracomunitarios.")
    else:
        libres = 3 - total
        print("Tendrías " + str(total) + ". Te queda(n) " + str(libres) + " hueco(s).")

""" otra parte de la pregunta 1"""
def insertar_elemento():
    """ Pide datos al usuario, calcula campos y guarda el jugador. """
    print("\n--- NUEVO FICHAJE ---")
    nombre = input("Nombre del jugador: ")

    # control de errores para la edad
    try:
        edad = int(input("Edad: "))
        valor = float(input("Valor de mercado (millones): "))
    except ValueError:
        print("Error: La edad y el valor deben ser números.")
        logging.error(f"Fallo al insertar a {nombre}: Datos numéricos incorrectos.", exc_info=True)
        return  # salgo de la función si falla

    posicion = input("Posición específica (ej. Extremo derecho): ")
    nacionalidad = input("Nacionalidad: ")

    esCrack = input("¿Es tu jugador un CRACK mediático? (si/no): ").lower()

    if(esCrack == "si"):
        detalle_crack = input("Introduce su estatus (ej. Balón de Oro, Leyenda): ")
        # Instanciamos la SUBCLASE Crack
        nuevo_jugador = Crack(nombre, edad, valor, posicion, nacionalidad, detalle_crack)
    else: 
        # Instanciamos la CLASE BASE Jugador
        nuevo_jugador = Jugador(nombre, edad, valor, posicion, nacionalidad)

    plantilla.append(nuevo_jugador)
    guardar_json()  # Guardamos en el fichero

    print("Jugador fichado correctamente.")
    logging.info(f"Jugador insertado: {nuevo_jugador.nombre} ({nuevo_jugador.nacionalidad})")


"""def buscar_elemento():
    print("\n--- BUSCAR JUGADOR ---")
    criterio = input("Introduce el nombre del jugador a buscar: ")
    encontrado = False

    for jugador in plantilla:
        # uso .lower() para que encuentre "lamine" aunque se guardara como "Lamine"
        if criterio.lower() in jugador.nombre.lower():
            print("¡JUGADOR ENCONTRADO!")
            print("Nombre: " + jugador.nombre)
            print("Valor: " + str(jugador.valorMercado) + " M")
            print("Posición: " + jugador.posicion)
            encontrado = True

    if encontrado == False:
        print("No se ha encontrado ningún jugador con ese nombre.")
        logging.info(f"Búsqueda fallida: {criterio}")"""

"""Pregunta 4 Búsqueda avanzada y filtrado"""

def buscar_elemento_examen():
    """ Busca un jugador por nombre en la lista local. """
    print("\n--- BUSCAR JUGADOR ---")
    criterio = input("Introduce el nombre del jugador a buscar: ")
    encontrado = False

    for jugador in plantilla:
        # Accedemos con punto .nombre
        if criterio.lower() in jugador.nombre.lower():
            print("\n¡JUGADOR ENCONTRADO!")
            print(jugador) # Esto usa el __str__ de la clase (polimorfismo)
            encontrado = True

    if not encontrado:
        print("No se ha encontrado ningún jugador con ese nombre.")
        logging.info(f"Búsqueda fallida: {criterio}")


def modificar_elemento():
    """ Busca un jugador y permite modificar su valor de mercado. """
    print("\n--- MODIFICAR JUGADOR ---")
    nombre_buscar = input("Nombre del jugador a modificar: ")

    for jugador in plantilla:
        if nombre_buscar.lower() == jugador.nombre.lower():
            print("Jugador encontrado: " + jugador.nombre)
            print("Valor actual: " + str(jugador.valorMercado))

            try:
                nuevo_valor = float(input("Introduce el nuevo valor de mercado: "))
                # Modificamos el atributo del objeto directamente
                jugador.valorMercado = nuevo_valor

                guardar_json()  # Guardamos los cambios

                print("Valor actualizado correctamente.")
                logging.info(f"Valor modificado para {jugador.nombre}: Nuevo valor {nuevo_valor}")
                return  # Salimos de la función tras modificar
            except ValueError:
                print("Error: El valor debe ser numérico.")
                logging.error("Intento de modificación fallido: valor no numérico.", exc_info=True)
                return

    print("Error: Jugador no encontrado.")


def eliminar_elemento():
    """ Busca un jugador por nombre y lo elimina de la lista. """
    print("\n--- ELIMINAR JUGADOR ---")
    nombre_borrar = input("Nombre del jugador a eliminar: ")

    for jugador in plantilla:
        if nombre_borrar.lower() == jugador.nombre.lower():
            plantilla.remove(jugador)

            guardar_json()  # Guardamos los cambios

            print("Jugador " + jugador.nombre + " eliminado correctamente.")
            logging.warning(f"Jugador eliminado: {jugador.nombre}")
            return

    print("Error: Jugador no encontrado.")


def mostrar_todos():
    """ Recorre la lista plantilla e imprime los datos. """
    print("\n--- PLANTILLA ACTUAL ---")
    if len(plantilla) == 0:
        print("La plantilla está vacía.")
    else:
        for jugador in plantilla:
            print("----------------")
            # Usamos el __str__ de la clase, que es diferente para Jugador y Crack
            print(jugador)
            
            # Mostramos info extra calculada
            es_extra = "SÍ" if not jugador.esComunitario else "NO"
            print("Extracomunitario: " + es_extra)


# el menú principal
def menu():
    # Cargar datos al iniciar la app
    cargar_json()
    logging.info("Aplicación iniciada por el usuario.")

    while True:
        print("\n--- SCOUT MANAGER ---")
        print("1. Añadir jugador")
        print("2. Buscar jugador")
        print("3. Modificar valor")
        print("4. Eliminar jugador")
        print("5. Ver plantilla")
        print("6. Comprobar cupo extracomunitarios")
        print("7. Reporte Financiero (Pregunta 3)") # Actualizado texto menú
        print("8. Salir")

        opcion = input("Elige una opción: ")

        if opcion == "1":
            insertar_elemento()
        elif opcion == "2":
            buscar_elemento_examen()
        elif opcion == "3":
            modificar_elemento()
        elif opcion == "4":
            eliminar_elemento()
        elif opcion == "5":
            mostrar_todos()
        elif opcion == "6":
            fCupo()
        elif opcion == "7": # Cambiado a opción numérica para el menú
            generar_reporte()
        elif opcion == "8":
            print("Cerrando aplicación")
            logging.info("Aplicación cerrada.")
            break
        else:
            print("Opción no válida.")


"""esto de aquí me ha dicho la IA que es la mejor manera para controlar cuando se ejecuta el programa"""
if __name__ == "__main__":
    menu()