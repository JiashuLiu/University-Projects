#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 22 14:41:40 2021

@author: jiashu
"""


def es_posible_ganar(m):
    # lista en la que guardaremos todos los resultados encadenados que calculemos
    estados = [1]*(m+1)

    # Introducimos los valores de los casos base (1 = false, 2 = true)
    estados[0] = False  # Sabiendo que cuando hay una piedra, no hay estrategia ganadora
    estados[1] = True  # Cuando hay dos piedras, si hay estrategia ganadora
    n = 2

    # Generamos los valores de la cadena hasta llegar a m
    while n <= m-1:
        # Si todos los valores previos son verdaderos, el estado es falso. En caso contrario, añadimos un true.
        if n < 6:
            a1 = estados[n-1]
            a2 = estados[n-2]
            estados[n] = not(a1 and a2)
            n += 1
        else:
            a1 = estados[n-1]
            a2 = estados[n-2]
            a6 = estados[n-6]
            estados[n] = not (a1 and a2 and a6)
            n += 1

    # Por último, devolvemos el estado de la lista para el valor m.
    return estados[m-1]


print (es_posible_ganar(10**6))
