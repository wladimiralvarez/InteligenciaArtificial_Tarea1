# costo de entrar a una celda, penaliza la congestión
def costo_paso(ocupacion, celda):
    return 1 + ocupacion[celda]
