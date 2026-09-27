# revisa que cada P llegue a la salida
import sys
from pathlib import Path

from distancias import distancias_a
from mapa import leer_mapa, transitable

CARPETA = Path(__file__).parent / "mapas"


def main():
    rutas = [Path(r) for r in sys.argv[1:]] or sorted(CARPETA.glob("*.txt"))

    for ruta in rutas:
        mapa = leer_mapa(ruta)
        dist = distancias_a(mapa.grilla, mapa.salida)

        sin_ruta = [pos for pos in mapa.inicios if pos not in dist]
        aisladas = [
            (f, c)
            for f in range(len(mapa.grilla))
            for c in range(len(mapa.grilla[0]))
            if transitable(mapa.grilla, (f, c)) and (f, c) not in dist
        ]
        pasos = [dist[pos] for pos in mapa.inicios if pos in dist]

        print(f"{ruta.name}: {len(mapa.inicios)} personas, salida en {mapa.salida}")
        if pasos:
            print(f"  camino más corto entre {min(pasos)} y {max(pasos)} pasos")
        if sin_ruta:
            print(f"  SIN RUTA A LA SALIDA: {sin_ruta}")
        if aisladas:
            print(f"  {len(aisladas)} celdas libres incomunicadas: {aisladas[:5]}")


if __name__ == "__main__":
    main()
