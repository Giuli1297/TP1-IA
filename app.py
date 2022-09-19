import random
import time
import sys
import math

import asyncio
import sys, math
from flask import Flask, render_template, request

from algorithms.backtracking import tsp_backtracking
from algorithms.vegas import *
from algorithms.avaroopt import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

ALGORTHMS = {'backtracking': 'Backtracking', 'las_vegas': 'Las Vegas', 'AvaroOpt': "Avaro", 'todos': "Todos"}


@app.route('/', methods=('GET', 'POST'))
def index():
    if request.method == 'GET':
        return render_template('index.html', time=False)
    elif request.method == 'POST':
        starttime = time.time()
        algorithm = request.form['algorithm']
        n_nodes = request.form['n_nodes']
        n_arcs = request.form['n_arcs']
        max_arc_cost  = request.form['max_arc_cost']

        if n_nodes == '' or max_arc_cost == '':
            return render_template('index.html',
                                   message={"NoData": "Argumentos Incompletos"})

        if n_arcs:
            nodo_inicial = generateGraph(int(n_nodes), int(n_arcs), int(max_arc_cost))
        else:
            nodo_inicial = genereteGrafoConexo(int(n_nodes), int(max_arc_cost))
        if algorithm == 'backtracking':
            costoruta = 0
            timeoutflag = False
            contador = []
            start = time.time()
            solucion = tsp_backtracking(getAdyacencyAsList(nodo_inicial), contador, starttime)
            end = time.time()
            if end - start > 60:
                timeoutflag = True
            else:
                costoruta = solucion['costo']
                optimo = 'Si'
            return render_template('index.html',
                                   datos=[{"time": "Timeout" if timeoutflag else end-start,
                                           "cant_nodos_visitados": len(contador),
                                           "costo_ruta": "Timeout" if timeoutflag else costoruta,
                                           "algoritmo": ALGORTHMS[algorithm],
                                           "optimo": "Timeout" if timeoutflag else optimo,
                                           "timeout": timeoutflag}])
        elif algorithm == 'las_vegas':
            contador = []
            nodos_camino = []
            start = time.time()
            datos = vegasTSP(nodo_inicial, [], nodo_inicial, int(n_nodes), contador, nodos_camino)
            end = time.time()
            costoruta = calculateRouteCost(datos)
            optimo = 'No'
            return render_template('index.html',
                                   datos=[{"time": end - start,
                                           "cant_nodos_visitados": len(contador),
                                           "costo_ruta": costoruta,
                                           "algoritmo": ALGORTHMS[algorithm],
                                           "optimo": optimo}])

        elif algorithm == 'AvaroOpt':
            nodos_camino=[]
            contadorAvaro2otp = []
            start = time.time()
            datosAvaro2otp = optimizacion2optIterator(
                nodo_inicial,
                avaroTSP(nodo_inicial, [], nodo_inicial, int(n_nodes), contadorAvaro2otp, nodos_camino)
            )
            end = time.time()
            tiempoAvaro2otp = end - start
            costorutaAvaro2otp = calculateRouteCost(datosAvaro2otp)
            optimo = 'No'
            return render_template('index.html',
                                   datos=[{"time": tiempoAvaro2otp,
                                           "cant_nodos_visitados": len(contadorAvaro2otp),
                                           "costo_ruta": costorutaAvaro2otp,
                                           "algoritmo": "Avaro + 2Opt"}])

        elif algorithm == "todos":
            costoruta = 0
            timeoutflag = False
            contadorBT = []
            start = time.time()
            solucion = tsp_backtracking(getAdyacencyAsList(nodo_inicial), contadorBT, starttime)
            end = time.time()
            if end - start > 60:
                timeoutflag = True
            else:
                costoruta = solucion['costo']
                optimo = 'Si'
            tiempoBT = end - start

            contadorVegas = []
            nodos_camino = []
            start = time.time()
            datosVegas = vegasTSP(nodo_inicial, [], nodo_inicial, int(n_nodes), contadorVegas, nodos_camino)
            datosVegas.append(nodo_inicial)
            end = time.time()
            tiempoVegas = end - start

            contadorAvaro = []
            start = time.time()
            datosAvaro = avaroTSP(nodo_inicial, [], nodo_inicial, int(n_nodes), contadorAvaro, nodos_camino)
            datosAvaro.append(nodo_inicial)
            end = time.time()
            tiempoAvaro = end - start

            contadorAvaro2otp = []
            start = time.time()
            datosAvaro2otp = optimizacion2optIterator(
                nodo_inicial,
                avaroTSP(nodo_inicial, [], nodo_inicial, int(n_nodes), contadorAvaro2otp, nodos_camino)
            )
            end = time.time()
            tiempoAvaro2otp = end - start

            costorutaBT = solucion['costo']
            costorutaVegas = calculateRouteCost(datosVegas)
            costorutaAvaro = calculateRouteCost(datosAvaro)
            costorutaAvaro2otp = calculateRouteCost(datosAvaro2otp)
            return render_template('index.html',
                                   datos=[{"time": "Timeout" if timeoutflag else tiempoBT,
                                           "cant_nodos_visitados": len(contadorBT),
                                           "costo_ruta": "Timeout" if timeoutflag else costorutaBT,
                                           "algoritmo": "BackTracking",
                                           "optimo": "Timeout" if timeoutflag else "Si"},
                                            {"time": tiempoVegas,
                                           "cant_nodos_visitados": len(contadorVegas),
                                           "costo_ruta": costorutaVegas,
                                           "algoritmo": "Las Vegas",
                                           "optimo": "Si" if costorutaBT == costorutaVegas else "No"},
                                          {"time": tiempoAvaro,
                                           "cant_nodos_visitados": len(contadorAvaro),
                                           "costo_ruta": costorutaAvaro,
                                           "algoritmo": "Avaro",
                                           "optimo": "Si" if costorutaBT == costorutaAvaro else "No"},
                                          {"time": tiempoAvaro2otp,
                                           "cant_nodos_visitados": len(contadorAvaro2otp),
                                           "costo_ruta": costorutaAvaro2otp,
                                           "algoritmo": "Avaro + 2otp",
                                           "optimo": "Si" if costorutaBT == costorutaAvaro2otp else "No"}
                                          ])


class nodo:
    nombre, aristas, cord = None, None, None

    def __init__(self, nombre):
        self.nombre = nombre
        self.cord = [random.randint(1, 10000), random.randint(1, 10000)]
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


def generateGraph(size, aristas, max_cost):
    if size <= 0 or aristas > (((size * (size - 1)) / 2) - size):
        print("Cantidad de aristas no valido")
        return 0
    nodos = []
    for i in range(size):
        nodos.append(nodo(str(i)))
    for i in range(size):
        costo = random.randint(int(distanciaRecta(nodos[0], nodos[i]))+1, int(distanciaRecta(nodos[0], nodos[i])+max_cost))
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
        costo = random.randint(int(distanciaRecta(nodos[0], nodos[i]))+1, int(distanciaRecta(nodos[0], nodos[i])+max_cost))
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
            costo = random.randint(int(distanciaRecta(nodos[0], nodos[i]))+1, int(distanciaRecta(nodos[0], nodos[i])+max_cost))
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
    n = len(matrix)
    matriz_adyacencia = [[] for i in range(n)]
    for idx, row in matrix.items():
        transformed_row = [0 for x in range(n)]
        for key, value in row.items():
            transformed_row[int(key)] = int(value)
        matriz_adyacencia[int(idx)] = transformed_row
    return matriz_adyacencia


def calculateRouteCost(camino):
    costo = 0
    for i in range(len(camino)-1):
        for arc in camino[i].aristas:
            if arc.nodo1 == camino[i] and arc.nodo2 == camino[i+1]:
                costo += arc.costo
    return costo
