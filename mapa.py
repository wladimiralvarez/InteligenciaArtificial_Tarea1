# lectura y validación de mapas de texto
from dataclasses import dataclass

MURO = "M"
LIBRE = "L"
SALIDA = "S"
INICIO = "P"  # posición inicial
FUEGO = "F"

SIMBOLOS = {MURO, LIBRE, SALIDA, INICIO, FUEGO}


@dataclass
class Mapa:
    grilla: list  # solo M, L y S
    salida: tuple
    inicios: list
    fuego: set


def leer_mapa(ruta):
    with open(ruta, encoding="utf-8") as archivo:
        filas = [linea.strip() for linea in archivo if linea.strip()]

    if not filas:
        raise ValueError(f"{ruta} está vacío")

    ancho = len(filas[0])
    salidas = []
    inicios = []
    fuego = set()

    for f, fila in enumerate(filas):
        if len(fila) != ancho:
            raise ValueError(f"la fila {f} mide {len(fila)}, se esperaba {ancho}")
        for c, simbolo in enumerate(fila):
            if simbolo not in SIMBOLOS:
                raise ValueError(f"símbolo desconocido '{simbolo}' en ({f}, {c})")
            if simbolo == SALIDA:
                salidas.append((f, c))
            elif simbolo == INICIO:
                inicios.append((f, c))
            elif simbolo == FUEGO:
                fuego.add((f, c))

    if len(salidas) != 1:
        raise ValueError(f"se esperaba 1 salida y hay {len(salidas)}")

    # la grilla guarda solo lo fijo
    grilla = [fila.replace(INICIO, LIBRE).replace(FUEGO, LIBRE) for fila in filas]
    return Mapa(grilla, salidas[0], inicios, fuego)


# el fuego va aparte
def transitable(grilla, pos):
    f, c = pos
    return 0 <= f < len(grilla) and 0 <= c < len(grilla[0]) and grilla[f][c] != MURO
