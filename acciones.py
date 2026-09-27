# acciones de un agente y cuáles puede hacer desde una celda
from enum import Enum
from mapa import transitable

class Accion(Enum):
    ARRIBA = (-1, 0)
    ABAJO = (1, 0)
    IZQUIERDA = (0, -1)
    DERECHA = (0, 1)
    ESPERAR = (0, 0)

MOVIMIENTOS = [a for a in Accion if a is not Accion.ESPERAR]

def destino(pos, accion):
    df, dc = accion.value
    return (pos[0] + df, pos[1] + dc)

# la congestión sube el costo
def acciones_validas(grilla, pos, fuego):
    validas = []
    for accion in Accion:
        d = destino(pos, accion)
        if transitable(grilla, d) and d not in fuego:
            validas.append(accion)
    return validas
