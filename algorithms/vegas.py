import random, sys

def vegasTSP(nodo_actual, n_visitados, nodo_inicial, N, co, ruta):
    nodos_visitados = n_visitados.copy()
    fronteras = []
    froteras_visitadas = []
    co.append(1)
    tree_node_number = len(co)
    for ar in nodo_actual.aristas:
        if (ar.nodo2 not in nodos_visitados or ar.nodo2 == nodo_inicial) and ar.nodo2 != nodo_actual:
            fronteras.append(ar.nodo2)
        if (ar.nodo1 not in nodos_visitados or ar.nodo1 == nodo_inicial) and ar.nodo1 != nodo_actual:
            fronteras.append(ar.nodo1)
    nodos_visitados.append(nodo_actual)
    while True:
        if nodo_inicial in fronteras:
            fronteras.remove(nodo_inicial)
            if len(nodos_visitados) == N:
                # print(nodos_visitados, file=sys.stdout)
                print("x", file=sys.stdout)
                ruta.extend(nodos_visitados)
                return nodos_visitados
        fronterasv2 = [x for x in fronteras if x not in froteras_visitadas]
        if not fronterasv2:
            return []
        target = random.choice(fronterasv2)
        froteras_visitadas.append(target)
        solution = vegasTSP(target, nodos_visitados, nodo_inicial, N, co, ruta)
        if solution:
            return solution