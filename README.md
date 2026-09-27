# Tarea 1: Escape de la Torre

Simulación de la evacuación de un piso en llamas. Un grupo de personas debe alcanzar la única
salida antes de que el fuego las alcance.

**Asignatura:** Inteligencia Artificial
**Integrante:** Leandro Wladimir Placencia Alvarez

El modelo del entorno, los algoritmos y los resultados están en el informe.

## Requisitos

Python 3.10 o superior. No usa librerías externas, solo la biblioteca estándar.

## Cómo ejecutar

Validar que los mapas estén bien formados y que cada persona pueda llegar a la salida:

```bash
python verificar.py
```

Ver una run en consola, con el mapa dibujado al principio y al final:

```bash
python main.py mapas/mapa1.txt astar
```

Estrategias disponibles: `bfs`, `dfs`, `astar`, `voraz`, `genetico` y `azar`, esta última sin planificación. Si no se indica mapa ni estrategia, usa `mapas/mapa1.txt` y
`azar`.

Correr el benchmark completo, 3 mapas × 6 estrategias × 200 runs:

```bash
python benchmark.py
```

Acepta la cantidad de runs como argumento:

```bash
python benchmark.py 10
```


