# corre una evacuación completa y devuelve el resultado
import random
from dataclasses import dataclass

from acciones import Accion, acciones_validas, destino
from agente import Estado, actualizar, crear_agentes, mover, ocupacion
from algoritmos import ALGORITMOS
from distancias import distancias_a
from fuego import propagar

K = 3  # turnos entre avances del fuego
MAX_TURNOS = 100  


@dataclass
class Resultado:
    evacuados: int
    total: int
    despeje: int  # turno del último que salió, None si no salió nadie
    turnos: int
    fuego: set
    agentes: list


def simular(mapa, nombre, semilla_fuego=2, semilla_agentes=1, eventos=False):
    rng_agentes = random.Random(semilla_agentes)
    rng_fuego = random.Random(semilla_fuego)
    random.seed(semilla_agentes)  # el genético usa el azar global
    agentes = crear_agentes(mapa.inicios)
    fuego = set(mapa.fuego)
    dist = distancias_a(mapa.grilla, mapa.salida)
    rutas = {}  # solo lo usa el genético, que no replanifica cada turno

    turno = 0
    while turno < MAX_TURNOS and any(a.estado is Estado.ACTIVO for a in agentes):
        turno += 1
        activos = [a for a in agentes if a.estado is Estado.ACTIVO]
        ocup = ocupacion(agentes)

        for a in activos:
            if a.espera > 0:
                a.espera -= 1
                continue
            if nombre == "azar":
                accion = rng_agentes.choice(acciones_validas(mapa.grilla, a.pos, fuego))
            elif nombre == "genetico":
                # planifica una vez y repite solo si el fuego le corta el paso
                if not rutas.get(a.id) or destino(a.pos, rutas[a.id][0]) in fuego:
                    rutas[a.id] = ALGORITMOS[nombre](mapa.grilla, a.pos, mapa.salida, fuego, ocup, dist)
                accion = rutas[a.id].pop(0) if rutas[a.id] else Accion.ESPERAR
            else:
                # replanifica cada turno
                ruta = ALGORITMOS[nombre](mapa.grilla, a.pos, mapa.salida, fuego, ocup, dist)
                accion = ruta[0] if ruta else Accion.ESPERAR
            mover(a, accion, mapa.grilla, fuego, ocup)

        for a in activos:
            actualizar(a, mapa.salida, fuego, turno)
        if turno % K == 0:
            fuego = propagar(mapa.grilla, fuego, mapa.salida, rng=rng_fuego)
        for a in activos:
            actualizar(a, mapa.salida, fuego, turno)

        if eventos:
            for a in activos:
                if a.estado is not Estado.ACTIVO:
                    print(f"turno {turno}, agente {a.id} {a.estado.value} en {a.pos}")

    evacuados = [a for a in agentes if a.estado is Estado.EVACUADO]
    despeje = max((a.turno_fin for a in evacuados), default=None)
    return Resultado(len(evacuados), len(agentes), despeje, turno, fuego, agentes)
