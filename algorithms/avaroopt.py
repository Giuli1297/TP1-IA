import random
import time
import sys
import math

import asyncio
import sys, math

def calculateRouteCost(camino):
    costo = 0
    for i in range(len(camino)-1):
        for arc in camino[i].aristas:
            if arc.nodo1 == camino[i] and arc.nodo2 == camino[i+1]:
                costo += arc.costo
    return costo


def avaroTSP(nodo_actual, n_visitados, nodo_inicial, N, co, ruta):
    nodos_visitados = n_visitados.copy()
    fronteras = []
    froteras_visitadas = []
    co.append(1)
    tree_node_number = len(co)
    def getCost(e):
        return e.costo+distanciaRecta(nodo_inicial, e.nodo2)
    nodo_actual.aristas.sort(key=getCost)
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
        target = fronterasv2[0]
        froteras_visitadas.append(target)
        solution = avaroTSP(target, nodos_visitados, nodo_inicial, N, co, ruta)
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
    #print("Iteraciones "+str(c))
    return solucion


def distanciaRecta(nodo_1, nodo_2):
    return math.sqrt(((nodo_2.cord[0]-nodo_1.cord[0])**2)+((nodo_2.cord[1]-nodo_1.cord[1])**2))