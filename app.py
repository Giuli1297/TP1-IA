import random
import time
import sys

import asyncio
import sys, math
from flask import Flask, render_template, request

from algorithms.backtracking import tsp_backtracking

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

ALGORTHMS = {'backtracking': 'Backtracking', 'las_vegas': 'Las Vegas'}

@app.route('/', methods=('GET', 'POST'))
def index():
    if request.method == 'GET':
        return render_template('index.html', time=False)
    elif request.method == 'POST':
        algorithm = request.form['algorithm']
        n_nodes = request.form['n_nodes']
        n_arcs = request.form['n_arcs']
        max_arc_cost  = request.form['max_arc_cost']

        if n_arcs:
            nodo_inicial = generateGraph(int(n_nodes), int(n_arcs), int(max_arc_cost))
        else:
            nodo_inicial = genereteGrafoConexo(int(n_nodes), int(max_arc_cost))

        if algorithm == 'backtracking':
            contador = []
            start = time.time()
            solucion = tsp_backtracking(getAdyacencyAsList(nodo_inicial), contador)
            end = time.time()
            costoruta = solucion['costo']
            optimo = 'Si'
        elif algorithm == 'las_vegas':
            contador = []
            nodos_camino = []
            start = time.time()
            datos = vegasTSP(nodo_inicial, [], nodo_inicial, int(n_nodes), contador, nodos_camino)
            end = time.time()
            costoruta = calculateRouteCost(datos)
            optimo = 'No'
        return render_template('index.html',
                               datos=[{"time": end-start,
                                      "cant_nodos_visitados": len(contador),
                                       "costo_ruta": costoruta,
                                       "algoritmo": ALGORTHMS[algorithm],
                                       "optimo": optimo}])


class nodo:
    nombre, aristas = None, None

    def __init__(self, nombre):
        self.nombre = nombre
        self.aristas = []


class arista:
    nodo1, nodo2, costo = None, None, None

    def __init__(self, nodo1, nodo2, costo):
        self.nodo1 = nodo1
        self.nodo2 = nodo2
        self.costo = costo


def printList(lista):
    print("[", end="")
    for el in lista:
        print(el.nombre, end=", ")
    print("]", end="")


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
        # print(tree_node_number)
        # print(str(co) + "Nodo actual: " + nodo_actual.nombre + " - NVisitados: ", end="")
        # printList(nodos_visitados)
        # print(" - Frontera: ", end="")
        # printList(fronteras)
        # print(" - Frontera V: ", end="")
        # printList(froteras_visitadas)
        # print("")
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


def distancia(nodo_1, nodo_2):
    for arista in nodo_1.aristas:
        if arista.nodo2 == nodo_2:
            return arista.costo


def optimizacion2opt(graph):
    cambio_min = 0
    for i in range(len(graph)-2):
        for j in range(i+2, len(graph)-1):
            cambio=0
            costo_actual = distancia(graph[i], graph[i+1])+distancia(graph[j], graph[j+1])

            if distancia(graph[i], graph[j]) is not None and distancia(graph[i + 1], graph[j + 1]) is not None:
                costo_nuevo = distancia(graph[i], graph[j])+distancia(graph[i+1], graph[j+1])
                cambio = costo_nuevo - costo_actual

            if cambio < cambio_min:
                cambio_min = cambio
                i_min = i
                j_min = j
    if cambio_min < 0:
        graph[i_min+1:j_min+1]=graph[i_min+1:j_min+1][::-1]
    return graph

def optimizacion2optIterator(nodo_inicial, graph):
    solucion = graph.copy()
    solucion.append(nodo_inicial)
    cambio = 1
    c = 0
    while cambio != 0:
        c=c+1
        costo_antes = calculateRouteCost(solucion)
        solucion = optimizacion2opt(solucion)
        costo_despues = calculateRouteCost(solucion)

        cambio = costo_antes - costo_despues
    print("Iteraciones "+str(c))
    return solucion



def generateGraph(size, aristas, max_cost):
    if size <= 0 or aristas > (((size * (size - 1)) / 2) - size):
        print("Cantidad de aristas no valido")
        return 0
    nodos = []
    for i in range(size):
        nodos.append(nodo(str(i)))
    for i in range(size):
        costo = random.randint(1, max_cost)
        if i == 0:
            nodos[i].aristas.append(arista(nodos[i], nodos[1], costo))
            nodos[i].aristas.append(arista(nodos[i], nodos[size - 1], costo))
        elif i == size - 1:
            nodos[i].aristas.append(arista(nodos[i], nodos[0], costo))
            nodos[i].aristas.append(arista(nodos[i], nodos[i - 1], costo))
        else:
            nodos[i].aristas.append(arista(nodos[i], nodos[i + 1], costo))
            nodos[i].aristas.append(arista(nodos[i], nodos[i - 1], costo))

    for i in range(aristas):
        costo = random.randint(1, max_cost)
        n_gen1 = random.randint(0, size - 1)
        n_gen2 = random.randint(0, size - 1)
        rtry = False
        for arist in nodos[n_gen1].aristas:
            if arist.nodo2.nombre == str(n_gen2):
                rtry = True
        while n_gen1 == n_gen2 or rtry:
            n_gen1 = random.randint(0, size - 1)
            n_gen2 = random.randint(0, size - 1)
            rtry = False
            for arist in nodos[n_gen1].aristas:
                if arist.nodo2.nombre == str(n_gen2):
                    rtry = True
        nodos[n_gen1].aristas.append(arista(nodos[n_gen1], nodos[n_gen2], costo))
        nodos[n_gen2].aristas.append(arista(nodos[n_gen2], nodos[n_gen1], costo))

    return nodos[0]


def genereteGrafoConexo(size, max_cost):
    nodos = []
    for i in range(size):
        nodos.append(nodo(str(i)))
    for i in range(size):
        for j in range(size):
            costo = random.randint(1, max_cost)
            if i != j:
                if distancia(nodos[i], nodos[j]) is None:
                    nodos[i].aristas.append(arista(nodos[i], nodos[j], costo))
                    nodos[j].aristas.append(arista(nodos[j], nodos[i], costo))
    return nodos[0]


def printGraphMatrix(nodoInicial):
    visitedNodes = []
    n_queue = [nodoInicial]
    matrix = {}
    while n_queue:
        actual_node = n_queue.pop(0)
        visitedNodes.append(actual_node)
        matrix[actual_node.nombre] = {}
        for arista in actual_node.aristas:
            if arista.nodo2 not in visitedNodes:
                n_queue.append(arista.nodo2)
            matrix[actual_node.nombre][arista.nodo2.nombre] = arista.costo
    return matrix

def getAdyacencyAsList(nodoInicial):
    matrix = printGraphMatrix(nodoInicial)
    matriz_adyacencia = []
    index = 0
    for row in matrix.values():
        transformed_row = list(map(lambda x: int(x), row.values()))
        transformed_row.insert(index, index)
        matriz_adyacencia.append(transformed_row)
        index += 1
    return matriz_adyacencia


def calculateRouteCost(camino):
    costo = 0
    for i in range(len(camino)-1):
        for arc in camino[i].aristas:
            if arc.nodo1 == camino[i] and arc.nodo2 == camino[i+1]:
                costo += arc.costo
    # for arc in camino[len(camino)-1].aristas:
    #     if arc.nodo1 == camino[len(camino)-1] and arc.nodo2 == camino[0]:
    #         costo += arc.costo
    return costo

# N = 20
# nodo_inicial = generateGraph(N, 10, max_cost=10)
# # nodo_inicial = genereteGrafoConexo(N, max_cost=10)
# print(printGraphMatrix(nodo_inicial))

# start = time.time()
# contador = []
# nodosCamin = []
# datos = vegasTSP(nodo_inicial, [], nodo_inicial, N, contador, nodosCamin)
# datosv2 = datos.copy()
# printList(datosv2)
# print()
# print(calculateRouteCost(datosv2))
# datos = optimizacion2optIterator(nodo_inicial, datos)
# printList(datos)
# print()
# datos.pop(len(datos)-1)
# print(calculateRouteCost(datos))
# # print(len(contador))
# # print(nodosCamin)
# end = time.time()
# print()
# print(end - start)



