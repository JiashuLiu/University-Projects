#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fichero principal de la entrega.
El objetivo es crear un número de matrices aleatorias y multiplicarlas usando el algoritmo de Strassen.

El tiempo de cada una de las multiplicaciones es guardado en una lista para, posteriormente,
  generar un gráfico de duración de cada una de las ejecuciones.
"""

import numpy as np

import matplotlib.pyplot as plt
import time
import math

# Constantes para definir el tamaño de matrices que vamos a multiplicar
MIN_MATRIX_SIZE = 1000
MAX_MATRIX_SIZE = 2000
SIZE_STEP = 100
BASE_CASE_SIZE = 64  # Tamaño que la matriz debe tener para


# Listas con los resultados de las ejecuciones (para los gráficos)
n_count = []
t_count = []
n_log = []
t_log = []


def create_random_matrix(N):
    """
    Función auxiliar que crea una matriz cuadrada del tamaño recibido como parámetro
    Los elementos de la matriz son números float entre 0.5 y 99.9
    """
    return np.random.uniform(low=0.5, high=99.9, size=(N, N))


def plot_tiempos():
    """
    Función para generar un gráfico con los tiempos tras las ejecuciones
    """
    plt.plot(n_count, t_count, "b-")
    plt.grid(b=True, which='major', axis='both',
             color='r', linestyle='--', linewidth=0.5)
    plt.xlabel('Tamaño de la matriz')
    plt.ylabel('tiempo [seg]')
    plt.savefig("strassen_tiempos.png")
    # plt.show()
    plt.clf()


def plot_log():
    """
    Función para generar un gráfico con los tiempos (a escala logarítmica)
    """
    plt.plot(n_log, t_log, "b-")
    plt.grid(b=True, which='major', axis='both',
             color='r', linestyle='--', linewidth=0.5)
    plt.xlabel('log(Tamaño de la matriz)')
    plt.ylabel('log(tiempo [seg])')
    plt.savefig("strassen-log-log.png")
    # plt.show()
    plt.clf()


def blocks(mat):
    """
    Divide una matriz dada en cuatro bloques.
    Por simplicidad en el código, se espera que la entrada sea del tipo matrix de la librería numpy,
      aunque se intenta convertir en una al principio del método por si acaso.
    Se devuelve una tupla con las cuatro submatrices (también del tipo matrix de numpy)
    """
    matriz = np.matrix(mat)
    filas, columnas = matriz.shape
    # calculamos la mitad de filas y columnas para hacer la división en 4 bloques
    filas2, columnas2 = filas // 2, columnas // 2
    return (
        # primera mitad de filas, primera mitad de columnas (A11)
        matriz[:filas2, :columnas2],
        # primera mitad de filas, segunda mitad de columnas (A12)
        matriz[:filas2, columnas2:],
        # segunda mitad de filas, primera mitad de columnas (A21)
        matriz[filas2:, :columnas2],
        # segunda mitad de filas, segunda mitad de columnas (A11)
        matriz[filas2:, columnas2:]
    )


def mult_base(mat1, mat2):
    """
    Este método realiza la multiplación de dos matrices recibidas como parámetro
    Se usa en esta práctica para la multiplicación del caso base, cuando el tamaño de la matriz es
      tan pequeño que no merece la pena aplicar dividirla en trozos más pequeños usando el algoritmo
      de Strassen

    Por simplicidad del código, se usa la función matmul, presente en la librería numpy
    """
    return np.matmul(mat1, mat2)


def mult_blocks(A, B):
    """
    Método auxiliar para realizar el algoritmo de Strassen
    Se realiza la división en sub-bloques y la recomposición posterior, tras llamar recursivamente a la función mult_strassen
    """
    # División de las matrices en bloques
    A11, A12, A21, A22 = blocks(A)
    B11, B12, B21, B22 = blocks(B)

    # Multiplicaciones de los subbloques
    M1 = mult_strassen(A11+A22, B11+B22)
    M2 = mult_strassen(A21 + A22, B11)
    M3 = mult_strassen(A11, B12-B22)
    M4 = mult_strassen(A22, B21-B11)
    M5 = mult_strassen(A11+A12, B22)
    M6 = mult_strassen(A21-A11, B11 + B12)
    M7 = mult_strassen(A12-A22, B21+B22)

    # Combinamos las multiplicaciones en nuevos subbloques
    C11 = M1 + M4 - M5 + M7
    C12 = M3 + M5
    C21 = M2 + M4
    C22 = M1 - M2 + M3 + M6

    # Combinación de la matriz definitiva como resultado
    return np.vstack((np.hstack((C11, C12)), np.hstack((C21, C22))))


def add_fila_col(mat):
    """
    Funcion auxiliar que añade una fila y una columna al final de la matriz recibida como parámetro
    """
    newMat = np.matrix(mat)
    n, m = newMat.shape  # Dimensiones actuales de la matriz

    # Añadir una fila con todo ceros
    newRow = np.zeros(n)

    # Añadir una columana con todo ceros (hay que tener en cuenta que habrá una fila extra al añadir)
    newCol = np.zeros((m+1, 1))

    # Componer la matriz definitiva
    newMat = np.vstack([newMat, newRow])
    newMat = np.hstack([newMat, newCol])

    return newMat


def del_fila_col(mat):
    """
    Funcion auxiliar que elimina la última fila y columna de la matriz recibida como parámetro
    Su finalidad es eliminar la fila y columna incluida previamente usando add_fila_col
    """
    return mat[:-1, :-1]


def mult_strassen(A, B):
    """
    Función principal. Multiplica dos matrices utilizando el algoritmo de Strassen.
    Precondición: ambas matrices se suponen cuadradas y del mismo tamaño. En caso contrario, el progama no funcionará correctamente

    Si el tamaño de las matrices es menor o igual al definido como caso base, se multiplicarán de forma normal.
    En caso contrario, se partirán en cuatro submatrices y se llamará de manera recursiva a esta función para resolver el programa más pequeño
    """
    if len(A) <= BASE_CASE_SIZE:
        result = mult_base(A, B)
    else:
        if (len(A) % 2 == 0):
            result = mult_blocks(A, B)
        else:
            # Añadimos fila y columna a las matrices para que la división en cuatro partes sea correcta
            exp_result = mult_blocks(add_fila_col(A), add_fila_col(B))
            # Eliminamos la fila y columna añadida previamente antes de devolver el resultado
            result = del_fila_col(exp_result)
    return result


n = MIN_MATRIX_SIZE
while n <= MAX_MATRIX_SIZE:

    # Creamos dos matrices aleatorias para multiplicar
    A = create_random_matrix(n)
    B = create_random_matrix(n)

    # Se toma tiempo antes y después de llamar a la función mult_strassen
    tim_ini = time.time()
    result = mult_strassen(A, B)
    tim_fin = time.time()
    
    # Se guardan resultados para hacer los gráficos
    n_count.append(n)
    t_count.append(tim_fin - tim_ini)
    n_log.append(math.log(n))
    t_log.append(math.log(tim_fin - tim_ini))

    n += SIZE_STEP

plot_tiempos()
plot_log()
