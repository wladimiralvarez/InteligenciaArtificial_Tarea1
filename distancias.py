# distancia a la salida esquivando muros
from collections import deque
from acciones import MOVIMIENTOS, destino
from mapa import transitable


# ignora fuego y congestión
def distancias_a(grilla, salida):
    dist = {salida: 0}
    cola = deque([salida])
    while cola:
        pos = cola.popleft()
        for mov in MOVIMIENTOS:
            vecino = destino(pos, mov)
            if transitable(grilla, vecino) and vecino not in dist:
                dist[vecino] = dist[pos] + 1
                cola.append(vecino)
    return dist
