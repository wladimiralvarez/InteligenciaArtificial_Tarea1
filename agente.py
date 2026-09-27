# estado de cada persona
from collections import Counter
from dataclasses import dataclass
from enum import Enum
from acciones import Accion, acciones_validas, destino

class Estado(Enum):
    ACTIVO = "activo"
    EVACUADO = "evacuado"
    BAJA = "baja"

@dataclass
class Agente:
    id: int
    pos: tuple
    estado: Estado = Estado.ACTIVO
    turno_fin: int = None  # turno en que evacuó o fue baja
    espera: int = 0  # turnos atascado por congestión

def crear_agentes(inicios):
    return [Agente(i, pos) for i, pos in enumerate(inicios)]

def mover(agente, accion, grilla, fuego, ocupacion=None):
    if agente.estado is not Estado.ACTIVO:
        raise ValueError(f"el agente {agente.id} ya no está activo")
    if accion not in acciones_validas(grilla, agente.pos, fuego):
        raise ValueError(f"el agente {agente.id} no puede hacer {accion.name} desde {agente.pos}")
    agente.pos = destino(agente.pos, accion)
    # entrar donde ya hay n personas cuesta n turnos parado
    if ocupacion is not None and accion is not Accion.ESPERAR:
        agente.espera = ocupacion[agente.pos]

def actualizar(agente, salida, fuego, turno):
    if agente.estado is not Estado.ACTIVO:
        return
    if agente.pos in fuego:
        agente.estado = Estado.BAJA
        agente.turno_fin = turno
    elif agente.pos == salida:
        agente.estado = Estado.EVACUADO
        agente.turno_fin = turno

# solo activos
def ocupacion(agentes):
    return Counter(a.pos for a in agentes if a.estado is Estado.ACTIVO)
