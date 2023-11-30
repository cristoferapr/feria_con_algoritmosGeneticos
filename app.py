import random, sys
from numpy import argmin

# Definir constantes globales
NUM_GENERACIONES = 100
PROBABILIDAD_CRUCE = 0.4
PROBABILIDAD_MUTACION = 0.3

def distancia(i, j, orden, tamanos):
    """
    Calcula la distancia entre dos puestos en la solución actual.

    Args:
        i (int): Índice del primer puesto.
        j (int): Índice del segundo puesto.
        orden (list): Lista que representa la solución actual.
        tamanos (list): Lista que contiene los tamaños de cada puesto.

    Returns:
        float: Distancia entre los puestos i y j en la solución actual.
    """
    Lxi = tamanos[orden[i]]
    Lxj = tamanos[orden[j]]

    suma_intermedia = sum(tamanos[orden[k]] for k in range(i + 1, j))

    return Lxi / 2 + suma_intermedia + Lxj / 2

def evaluar_solucion(orden, preferencias, tamanos):
    """
    Evalúa la calidad de una solución dada.

    Args:
        orden (list): Lista que representa la solución actual.
        preferencias (list): Matriz de preferencias entre pares de puestos.
        tamanos (list): Lista que contiene los tamaños de cada puesto.

    Returns:
        float: Valor de la función objetivo que representa la calidad de la solución.
    """
    n = len(orden)
    esfuerzo = 0

    for i in range(n - 1):
        for j in range(i + 1, n):
            esfuerzo += distancia(i, j, orden, tamanos) * preferencias[i][j]

    return esfuerzo

def inicializar_poblacion(num_puestos):
    """
    Inicializa una población de soluciones aleatorias.

    Args:
        num_puestos (int): Número total de puestos.

    Returns:
        list: Lista de soluciones iniciales.
    """
    porcentaje_tamano_poblacion = 0.5
    tamano_poblacion = int(num_puestos * porcentaje_tamano_poblacion)
    return [list(range(num_puestos)) for _ in range(tamano_poblacion)]

def seleccion_torneo(poblacion, fitness, tamano_torneo):
    """
    Realiza la selección de torneo para elegir individuos de la población.

    Args:
        poblacion (list): Lista de soluciones actuales.
        fitness (list): Lista de valores de la función objetivo para cada solución.
        tamano_torneo (int): Tamaño del torneo.

    Returns:
        list: Individuo seleccionado mediante el torneo.
    """
    torneo = random.sample(range(len(poblacion)), tamano_torneo)
    ganador = min(torneo, key=lambda x: fitness[x])
    return poblacion[ganador][:]  # Clonar para evitar referencias no deseadas

def cruce(padre1, padre2):
    """
    Realiza el cruce de dos padres para producir dos descendientes.

    Args:
        padre1 (list): Primer padre.
        padre2 (list): Segundo padre.

    Returns:
        tuple: Dos descendientes generados a partir de los padres.
    """
    punto_cruce = random.randint(1, len(padre1) - 1)
    # Seleccionar un punto de cruce aleatorio entre 1 y la longitud del padre1 - 1.

    hijo1 = padre1[:punto_cruce] + [gen for gen in padre2 if gen not in padre1[:punto_cruce]]
    # El primer hijo toma los genes hasta el punto de cruce del padre1
    # y luego agrega los genes de padre2 que no están ya en la sección del padre1.

    hijo2 = padre2[:punto_cruce] + [gen for gen in padre1 if gen not in padre2[:punto_cruce]]
    # El segundo hijo toma los genes hasta el punto de cruce del padre2
    # y luego agrega los genes de padre1 que no están ya en la sección del padre2.
    return hijo1, hijo2

def mutacion(individuo):
    """
    Realiza la mutación en un individuo que supero cierta probabilidad.

    Args:
        individuo (list): Solución a mutar.

    Returns:
        list: Individuo mutado.
    """
    indice_1, indice_2 = random.sample(range(len(individuo)), 2)
    individuo[indice_1], individuo[indice_2] = individuo[indice_2], individuo[indice_1]

    return individuo

def leer_datos(archivo):
    """
    Lee los datos desde un archivo.

    Args:
        archivo (str): Nombre del archivo que contiene los datos.

    Returns:
        tuple: Tupla con el número de puestos, tamaños y preferencias.
    """
    with open(archivo, 'r') as f:
        num_puestos = int(f.readline())
        tamanos = list(map(int, f.readline().split(',')))
        preferencias = [list(map(int, line.split(','))) for line in f]

    return num_puestos, tamanos, preferencias

def main():
    """
    Función principal que ejecuta el algoritmo genético.

    """
    if len(sys.argv) != 2:
        print("Uso: python app.py <nombre_archivo>")
        sys.exit(1)

    archivo = sys.argv[1]

    num_puestos, tamanos, preferencias = leer_datos(archivo)

    num_generaciones = NUM_GENERACIONES
    probabilidad_cruce = PROBABILIDAD_CRUCE
    probabilidad_mutacion = PROBABILIDAD_MUTACION

    poblacion = inicializar_poblacion(num_puestos)
    
    for generacion in range(num_generaciones):
        # Evaluar la calidad de cada individuo en la población
        fitness = [evaluar_solucion(individuo, preferencias, tamanos) for individuo in poblacion]

        # Crear una nueva población mediante el proceso evolutivo
        nueva_poblacion = []
        while len(nueva_poblacion) < len(poblacion):
            # Seleccionar dos padres mediante el método del torneo
            padre1 = seleccion_torneo(poblacion, fitness, 3)
            padre2 = seleccion_torneo(poblacion, fitness, 3)

            # Realizar el cruce si se cumple la probabilidad de cruce
            if random.random() < probabilidad_cruce:
                hijo1, hijo2 = cruce(padre1, padre2)
            else:
                # Si no se cruza, los hijos son copias de los padres
                hijo1, hijo2 = padre1[:], padre2[:]

            # Aplicar la mutación a los hijos
            if random.random() < probabilidad_mutacion:
                nueva_poblacion.append(mutacion(hijo1))
            else:
                nueva_poblacion.append(hijo1)

            if random.random() < probabilidad_mutacion:
                nueva_poblacion.append(mutacion(hijo2))
            else:
                nueva_poblacion.append(hijo2)

        # Reemplazar la población anterior con la nueva generación
        poblacion = nueva_poblacion

    mejor_orden = poblacion[argmin(fitness)]
    mejor_esfuerzo = evaluar_solucion(mejor_orden, preferencias, tamanos)
    
    print("Mejor orden:", mejor_orden)
    print("Valor de funcion:", mejor_esfuerzo)

if __name__ == "__main__":
    main()