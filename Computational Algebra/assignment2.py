#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
La práctica consiste en iterar una lista de 100 posiciones en el que cada una de ellas hay una bola
 Se representa el número de bolas con un número entero y, en cada iteración, 
  se reparten todas las bolas de una posición entre las siguientes.
El objetivo de la práctica es determinar el número de iteraciones necesarias para volver al escenario incial.
'''


def box_rotation(n):
    '''
    Función que realiza las rotaciones necesarias dependiendo del número de cajas pasadas por parámetro
    Devuelve el número de iteraciones necesarias para volver al estado inicial.
    '''
    l = [1] * n
    # Se realiza de forma manual la primera iteración
    iteration = 1
    i = 1
    l[0] = 0
    l[1] = 2

    # Mientras la lista no haya vuelto al estado inicial (todos los valores en 1), seguimos iterando
    while(l.count(1) != n):
        n_balls = l[i]
        l[i] = 0
        # Se reparten todas las bolas de la posición actual en las siguientes
        for j in range(n_balls):
            l[(i+j+1) % n] += 1
        iteration += 1
        i = (i+n_balls) % n
    return iteration


result = box_rotation(100)
print(result)
