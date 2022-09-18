def checkConnection(grafo, x, y=0):
    print("Checking connection: " + str(x) + ", " + str(y))
    return grafo[x][y] != 0

# Se llega a una solución cuando se recorren todos los nodos y existe una conexión entre el último nodo recorrido y el nodo inicial
def traverse(grafo, n, v, camino, soluciones, current, count, costo):
	if count == n and checkConnection(grafo, current):
		found_path = camino.copy()
		found_path.append(1)
		soluciones.append({'costo': costo + grafo[current][0], 'camino': found_path})
		return

	for i in range(n):
		if v[i] == False and checkConnection(grafo, current, i):
			v[i] = True
			camino.append(i+1)
			traverse(grafo, n, v, camino, soluciones, i, count + 1, costo + grafo[current][i])
			camino.pop()
			v[i] = False

def tsp_backtracking(grafo):
    print(grafo)
    n = len(grafo)
    v = [False for i in range(n)]
    soluciones = []
    v[0] = True
    camino = [1,]
    traverse(grafo, n, v, camino, soluciones, 0, 1, 0)

    if len(soluciones) == 0:
        raise Exception("No se ha encontrado una solución")

    def cmp_key(e):
        return e["costo"]

    return min(soluciones, key=cmp_key)

"""
mapa = [[ 0, 10, 15, 20 ],
		[ 10, 0, 35, 25 ],
		[ 15, 35, 0, 30 ],
		[ 20, 25, 30, 0 ]]

try:
	minimo = tsp(mapa)
	print("Costo minimo: " + str(minimo))
except Exception as e:
	print(e)
"""
