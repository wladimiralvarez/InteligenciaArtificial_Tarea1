# avance del fuego hacia las celdas vecinas
import random
from acciones import MOVIMIENTOS, destino
from mapa import transitable

# prob es la probabilidad de que cada vecina se encienda 
def propagar(grilla, fuego, salida=None, prob=0.5, rng=random):
    nuevo = set(fuego)
    for pos in fuego:
        for mov in MOVIMIENTOS:
            vecino = destino(pos, mov)
            # la salida no se quema
            if vecino == salida or not transitable(grilla, vecino) or vecino in nuevo:
                continue
            # con prob 1 no hay rng
            if prob >= 1 or rng.random() < prob:
                nuevo.add(vecino)
    return nuevo
