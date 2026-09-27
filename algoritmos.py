# los algoritmos de búsqueda
import heapq
from collections import deque
from acciones import MOVIMIENTOS, destino
from costo import costo_paso
from genetico import genetico
from mapa import transitable

def _vecinos(grilla, pos, fuego):
    for mov in MOVIMIENTOS:
        d = destino(pos, mov)
        if transitable(grilla, d) and d not in fuego:
            yield mov, d

def _reconstruir(padres, salida):
    ruta = []
    pos = salida
    while padres[pos] is not None:
        anterior, accion = padres[pos]
        ruta.append(accion)
        pos = anterior
    ruta.reverse()
    return ruta

def bfs(grilla, inicio, salida, fuego, ocupacion, dist):
    padres = {inicio: None}
    cola = deque([inicio])
    while cola:
        pos = cola.popleft()
        if pos == salida:
            return _reconstruir(padres, salida)
        for mov, vecino in _vecinos(grilla, pos, fuego):
            if vecino not in padres:
                padres[vecino] = (pos, mov)
                cola.append(vecino)
    return []

def dfs(grilla, inicio, salida, fuego, ocupacion, dist):
    padres = {inicio: None}
    pila = [inicio]
    while pila:
        pos = pila.pop()
        if pos == salida:
            return _reconstruir(padres, salida)
        for mov, vecino in _vecinos(grilla, pos, fuego):
            if vecino not in padres:
                padres[vecino] = (pos, mov)
                pila.append(vecino)
    return []

def a_estrella(grilla, inicio, salida, fuego, ocupacion, dist):
    padres = {inicio: None}
    g = {inicio: 0}
    cola = [(dist.get(inicio, 0), 0, inicio)]
    while cola:
        _, costo, pos = heapq.heappop(cola)
        if pos == salida:
            return _reconstruir(padres, salida)
        if costo > g[pos]:
            continue
        for mov, vecino in _vecinos(grilla, pos, fuego):
            nuevo = costo + costo_paso(ocupacion, vecino)
            if vecino not in g or nuevo < g[vecino]:
                g[vecino] = nuevo
                padres[vecino] = (pos, mov)
                heapq.heappush(cola, (nuevo + dist.get(vecino, 0), nuevo, vecino))
    return []

def voraz(grilla, inicio, salida, fuego, ocupacion, dist):
    padres = {inicio: None}
    vistos = {inicio}
    cola = [(dist.get(inicio, 0), inicio)]
    while cola:
        _, pos = heapq.heappop(cola)
        if pos == salida:
            return _reconstruir(padres, salida)
        for mov, vecino in _vecinos(grilla, pos, fuego):
            if vecino not in vistos:
                vistos.add(vecino)
                padres[vecino] = (pos, mov)
                heapq.heappush(cola, (dist.get(vecino, 0), vecino))
    return []

ALGORITMOS = {"bfs": bfs, "dfs": dfs, "astar": a_estrella, "voraz": voraz, "genetico": genetico}
