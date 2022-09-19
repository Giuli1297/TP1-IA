import time


def checkConnection(grafo, x, y=0):
    return grafo[x][y] != 0

# Se llega a una solución cuando se recorren todos los nodos y existe una conexión entre el último nodo recorrido y el nodo inicial
def traverse(grafo, n, v, camino, soluciones, current, count, costo, contador, starttime):
    currenttime = time.time()
    contador.append(1)
    if count == n and checkConnection(grafo, current):
        found_path = camino.copy()
        found_path.append(1)
        soluciones.append({'costo': costo + grafo[current][0], 'camino': found_path})
        return 1

    if currenttime - starttime >= 60:
        return 5

    for i in range(n):
        if v[i] == False and checkConnection(grafo, current, i):
            v[i] = True
            camino.append(i+1)
            traverse(grafo, n, v, camino, soluciones, i, count + 1, costo + grafo[current][i], contador, starttime)
            camino.pop()
            v[i] = False

def tsp_backtracking(grafo, contador, starttime):
    n = len(grafo)
    v = [False for i in range(n)]
    soluciones = []
    v[0] = True
    camino = [1,]
    result = traverse(grafo, n, v, camino, soluciones, 0, 1, 0, contador, starttime)
    if result == 5:
        return []

    if len(soluciones) == 0:
        raise Exception("No se ha encontrado una solución")

    def cmp_key(e):
        return e["costo"]

    if soluciones[0].get("timeout"):
        return soluciones

    return min(soluciones, key=cmp_key)
