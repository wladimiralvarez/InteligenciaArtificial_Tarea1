# algoritmo genético
import random
from acciones import MOVIMIENTOS, Accion, destino
from costo import costo_paso
from mapa import transitable

POBLACION = 60
ELITE = 20
GENERACIONES = 40
PACIENCIA = 10  # generaciones sin mejorar antes de cortar
PROB_MUTACION = 0.15
LLEGADA = 1000


# aptitud y cuántos genes alcanzó a usar
def _evaluar(cromosoma, grilla, inicio, salida, fuego, ocupacion, dist):
    pos = inicio
    turnos = 0
    for i, gen in enumerate(cromosoma):
        d = destino(pos, gen)
        if not transitable(grilla, d) or d in fuego:
            turnos += 1  # choca y pierde el turno
            continue
        turnos += costo_paso(ocupacion, d)
        pos = d
        if pos == salida:
            return LLEGADA - turnos, i + 1
    return -10 * dist.get(pos, 99), len(cromosoma)


# los genes que chocan pasan a ESPERAR, así la ruta siempre se puede ejecutar
def _limpiar(cromosoma, grilla, inicio, fuego):
    pos = inicio
    ruta = []
    for gen in cromosoma:
        d = destino(pos, gen)
        if not transitable(grilla, d) or d in fuego:
            ruta.append(Accion.ESPERAR)
        else:
            ruta.append(gen)
            pos = d
    return ruta


def genetico(grilla, inicio, salida, fuego, ocupacion, dist, rng=random):
    if inicio == salida:
        return []

    largo = dist.get(inicio, 20) * 2 + 10
    poblacion = [[rng.choice(MOVIMIENTOS) for _ in range(largo)] for _ in range(POBLACION)]
    mejor, mejor_apt, mejor_pasos = poblacion[0], float("-inf"), largo
    sin_mejorar = 0

    for _ in range(GENERACIONES):
        evaluados = sorted(
            (
                (*_evaluar(c, grilla, inicio, salida, fuego, ocupacion, dist), c)
                for c in poblacion
            ),
            key=lambda e: e[0],
            reverse=True,
        )

        if evaluados[0][0] > mejor_apt:
            mejor_apt, mejor_pasos, mejor = evaluados[0]
            sin_mejorar = 0
        else:
            sin_mejorar += 1
            if sin_mejorar >= PACIENCIA:
                break

        elite = [e[2] for e in evaluados[:ELITE]]
        poblacion = list(elite)
        while len(poblacion) < POBLACION:
            padre, madre = rng.sample(elite, 2)
            corte = rng.randrange(1, largo)
            hijo = padre[:corte] + madre[corte:]
            if rng.random() < PROB_MUTACION:
                hijo[rng.randrange(largo)] = rng.choice(MOVIMIENTOS)
            poblacion.append(hijo)

    return _limpiar(mejor[:mejor_pasos], grilla, inicio, fuego)
