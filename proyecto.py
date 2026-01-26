import json
import logging

# funcion de logging
# Esto crea el fichero 'registro.log' donde se apuntará todo lo que pase
logging.basicConfig(
    filename='registro.log',
    level=logging.INFO, # Guardará info, warnings y errores
    format='%(asctime)s - %(levelname)s - %(message)s', # Formato: Fecha - Nivel - Mensaje
    filemode='a' # 'a' significa append (añadir al final sin borrar lo anterior, como en tema 5 de cliente)
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

comunitarios = ["España", "Alemania", "Austria", "Bélgica", "Bulgaria", "Chequia", "Chipre", "Croacia", "Dinamarca", "Eslovaquia", "Eslovenia", "Estonia", "Finlandia", "Francia", "Grecia", "Hungría", "Irlanda", "Italia", "Letonia", "Lituania", "Luxemburgo", "Malta", "Países Bajos", "Polonia", "Portugal", "Rumanía", "Suecia"]

# Lista principal donde guardaremos todos los jugadores
plantilla = []
ARCHIVO_JSON = "plantilla.json"

# funciones json

def guardar_json():
    """ Escribe la lista plantilla en el fichero JSON """
    try:
        with open(ARCHIVO_JSON, 'w', encoding='utf-8') as f:
            json.dump(plantilla, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Error al guardar el fichero: {e}")
        logging.error("Fallo crítico al intentar guardar en JSON", exc_info=True)

def cargar_json():
    """ Lee el fichero JSON y rellena la lista plantilla """
    global plantilla
    try:
        with open(ARCHIVO_JSON, 'r', encoding='utf-8') as f:
            plantilla = json.load(f)
            logging.info(f"Datos cargados correctamente. {len(plantilla)} jugadores en memoria.")
    except FileNotFoundError:
        # Si no existe el fichero, usamos el jugador inicial que tenías definido
        logging.warning("Fichero JSON no encontrado. Se inicia con datos por defecto.")
        
        jugador_inicial = {
            "nombre": "Lamine Yamal",
            "edad": 18,
            "valorMercado": 200,
            "posicion": "Extremo derecho",
            "demarcacion": "Delantero",  # Calculado manualmente para el ejemplo inicial
            "nacionalidad": "España",
            "esExtracomunitario": False
        }
        plantilla.append(jugador_inicial)
        guardar_json() # Creamos el fichero por primera vez
    except json.JSONDecodeError:
        logging.error("El fichero JSON está corrupto o mal formado.", exc_info=True)
        print("Error: El archivo de datos está dañado.")

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
        if jugador["esExtracomunitario"] == True:
            nuevos = nuevos + 1

    total = extraCom + nuevos
    
    # Registro el cálculo en el log
    logging.info(f"Cálculo de cupo realizado. Total: {total}")

    if total > 3:
        print("Error, tendrías " + str(total) + " extracomunitarios.")
    else:
        libres = 3 - total
        print("Tendrías " + str(total) + ". Te queda(n) " + str(libres) + " hueco(s).")

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
        return # salgo de la función si falla

    posicion = input("Posición específica (ej. Extremo derecho): ")
    nacionalidad = input("Nacionalidad: ")

    # creo el diccionario llamando a las funciones
    nuevo_jugador = {
        "nombre": nombre,
        "edad": edad,
        "valorMercado": valor,
        "posicion": posicion,
        "demarcacion": posicionGeneral(posicion), 
        "nacionalidad": nacionalidad,
        "esExtracomunitario": esCom(nacionalidad) 
    }

    plantilla.append(nuevo_jugador)
    guardar_json() # Guardamos en el fichero
    
    print("Jugador fichado correctamente.")
    logging.info(f"Jugador insertado: {nombre} ({nacionalidad})")

def buscar_elemento():
    """ Busca un jugador por nombre en la lista local. """
    print("\n--- BUSCAR JUGADOR ---")
    criterio = input("Introduce el nombre del jugador a buscar: ")
    encontrado = False
    
    for jugador in plantilla:
        # uso .lower() para que encuentre "lamine" aunque se guardara como "Lamine"
        if criterio.lower() in jugador["nombre"].lower():
            print("¡JUGADOR ENCONTRADO!")
            print("Nombre: " + jugador["nombre"])
            print("Valor: " + str(jugador["valorMercado"]) + " M")
            print("Posición: " + jugador["posicion"])
            encontrado = True
            
    if encontrado == False:
        print("No se ha encontrado ningún jugador con ese nombre.")
        logging.info(f"Búsqueda fallida: {criterio}")

def modificar_elemento():
    """ Busca un jugador y permite modificar su valor de mercado. """
    print("\n--- MODIFICAR JUGADOR ---")
    nombre_buscar = input("Nombre del jugador a modificar: ")
    
    for jugador in plantilla:
        if nombre_buscar.lower() == jugador["nombre"].lower():
            print("Jugador encontrado: " + jugador["nombre"])
            print("Valor actual: " + str(jugador["valorMercado"]))
            
            try:
                nuevo_valor = float(input("Introduce el nuevo valor de mercado: "))
                jugador["valorMercado"] = nuevo_valor
                
                guardar_json() # Guardamos los cambios
                
                print("Valor actualizado correctamente.")
                logging.info(f"Valor modificado para {jugador['nombre']}: Nuevo valor {nuevo_valor}")
                return # Salimos de la función tras modificar
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
        if nombre_borrar.lower() == jugador["nombre"].lower():
            plantilla.remove(jugador)
            
            guardar_json() # Guardamos los cambios
            
            print("Jugador " + jugador["nombre"] + " eliminado correctamente.")
            logging.warning(f"Jugador eliminado: {jugador['nombre']}")
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
            print("Nombre: " + jugador["nombre"])
            print("Demarcación: " + jugador["demarcacion"] + " (" + jugador["posicion"] + ")")
            print("Valor: " + str(jugador["valorMercado"]) + " M")
            # paso el booleano a texto para que quede bonito
            es_extra = "SÍ" if jugador["esExtracomunitario"] else "NO"
            print("Extracomunitario: " + es_extra)


#el menú principal
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
        print("7. Salir")
        
        opcion = input("Elige una opción: ")

        if opcion == "1":
            insertar_elemento()
        elif opcion == "2":
            buscar_elemento()
        elif opcion == "3":
            modificar_elemento()
        elif opcion == "4":
            eliminar_elemento()
        elif opcion == "5":
            mostrar_todos()
        elif opcion == "6":
            fCupo() 
        elif opcion == "7":
            print("Cerrando aplicación")
            logging.info("Aplicación cerrada.")
            break
        else:
            print("Opción no válida.")


"""esto de aquí me ha dicho la IA que es la mejor manera para controlar cuando se ejecuta el programa"""
if __name__ == "__main__":
    menu()