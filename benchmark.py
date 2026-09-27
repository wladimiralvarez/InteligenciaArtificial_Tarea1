# corre todas las combinaciones de mapa y estrategia y muestra las métricas
import statistics
import sys
from pathlib import Path
from mapa import leer_mapa
from simulacion import simular

CARPETA = Path(__file__).parent / "mapas"
MAPAS = ["mapa1", "mapa2", "mapa3"]
ESTRATEGIAS = ["azar", "bfs", "dfs", "astar", "voraz", "genetico"]
CORRIDAS = 200

def main():
    corridas = int(sys.argv[1]) if len(sys.argv) > 1 else CORRIDAS

    for nombre_mapa in MAPAS:
        mapa = leer_mapa(CARPETA / f"{nombre_mapa}.txt")
        print(f"\n{nombre_mapa}, {len(mapa.inicios)} personas, {corridas} corridas")
        print(f"{'estrategia':<11}{'superv.':>9}{'media':>8}{'desv':>7}{'mín':>6}{'máx':>6}")

        for estrategia in ESTRATEGIAS:
            tasas = []
            tiempos = []
            for i in range(corridas):
                # solo cambia la semilla del fuego
                r = simular(mapa, estrategia, semilla_fuego=i, semilla_agentes=i)
                tasas.append(r.evacuados / r.total)
                if r.despeje is not None:
                    tiempos.append(r.despeje)

            superv = 100 * statistics.mean(tasas)
            media = statistics.mean(tiempos) if tiempos else 0
            desv = statistics.stdev(tiempos) if len(tiempos) > 1 else 0
            print(
                f"{estrategia:<11}{superv:>8.1f}%{media:>8.1f}{desv:>7.1f}"
                f"{min(tiempos, default=0):>6}{max(tiempos, default=0):>6}"
            )


if __name__ == "__main__":
    main()
