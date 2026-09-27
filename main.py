# punto de entrada, muestra una corrida
import sys
from pathlib import Path

from agente import Estado
from algoritmos import ALGORITMOS
from mapa import FUEGO, INICIO, leer_mapa
from simulacion import simular

# corre desde cualquier carpeta
MAPA_POR_DEFECTO = Path(__file__).parent / "mapas" / "mapa1.txt"


def dibujar(grilla, fuego, personas=()):
    for f, fila in enumerate(grilla):
        linea = ""
        for c, celda in enumerate(fila):
            if (f, c) in fuego:
                linea += FUEGO
            elif (f, c) in personas:
                linea += INICIO
            else:
                linea += celda
        print(linea)

def main():
    ruta = sys.argv[1] if len(sys.argv) > 1 else MAPA_POR_DEFECTO
    nombre = sys.argv[2] if len(sys.argv) > 2 else "azar"

    if nombre != "azar" and nombre not in ALGORITMOS:
        print(f"error: no conozco '{nombre}', hay azar, {', '.join(ALGORITMOS)}")
        sys.exit(1)

    try:
        mapa = leer_mapa(ruta)
    except (OSError, ValueError) as error:
        print(f"error: {error}")
        sys.exit(1)

    print(f"{nombre}, turno 0")
    dibujar(mapa.grilla, mapa.fuego, mapa.inicios)
    print()

    resultado = simular(mapa, nombre, eventos=True)

    print(f"\nfin en el turno {resultado.turnos}")
    activos = [a.pos for a in resultado.agentes if a.estado is Estado.ACTIVO]
    dibujar(mapa.grilla, resultado.fuego, activos)
    print(f"{nombre}: {resultado.evacuados}/{resultado.total} evacuados")
    if resultado.despeje is not None:
        print(f"despeje en {resultado.despeje} turnos")


if __name__ == "__main__":
    main()
