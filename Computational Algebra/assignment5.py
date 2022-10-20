# -*- coding: utf-8 -*-
"""
Created on Fri Oct 15 02:14:58 2021

@author: shshs
"""


def es_Carmichael(N):
    """
    Función para calcular si un número dado es un número de Carmichael
    """
    if es_primo(N):  # queremos los números que cumplen la condición pero no son primos
        return False
    to_ret = True
    for y in range(N):  # es suficiente mirar todos los números que son menores que N
        if gcd_binario(N, y) == 1:  # y que son coprimos con N
            if potencia_mod(y, N-1, N) != 1:
                return False
            else:
                continue
    return to_ret


def multiplicar_mod(a, b, N):
    c = a*b
    c %= N
    return c


def potencia_mod(a, k, N):
    if k == 0:
        r = 1
    elif k % 2 == 0:
        r = potencia_mod(a, k//2, N)
        r = multiplicar_mod(r, r, N)
    else:
        r = potencia_mod(a, k-1, N)
        r = multiplicar_mod(a, r, N)
    return r


def gcd_binario(x, y):    # (x,y) != (0,0)
    x = abs(x)
    y = abs(y)
    xespar = x % 2 == 0
    yespar = y % 2 == 0
    if x == 0:           # caso base: gcd(0,y)=y
        m = y
    elif y == 0:         # caso base: gcd(x,0)=x
        m = x
    elif xespar and yespar:
        m = 2 * gcd_binario(x//2, y//2)
    elif xespar:
        m = gcd_binario(x//2, y)
    elif yespar:
        m = gcd_binario(x, y//2)
    elif x > y:
        m = gcd_binario(y, x-y)
    else:
        m = gcd_binario(x, y-x)
    return m


def es_primo(n):
    # Casos directos, para evitar entrar en bucle si es necesario
    if n in (2, 3):
        return True
    if n % 2 == 0:
        return False
    if n % 3 == 0:
        return False
    if n < 9:
        return True

    # Todos los primos mayores que 3, presentan la forma 6n ± 1
    r = int(n**0.5)
    f = 5 # Inicializamos el contador a 5 (que es primo)
    while f <= r:
        # Comprobamos si n es divisible por f y f+2. Si lo es, descartamos que sea primo.
        if n % f == 0:
            return False
        if n % (f+2) == 0:
            return False
        f += 6
    return True


def getnumbers(M):
    """
    Funcion que calcula tantos números de Charmichael como se pasa como parámetro (M)
    Cada vez que encuentra un nuevo número, éste se muestra por pantalla hasta tener los
     M números solicitados.
    """
    count = 0
    N = 2
    while count < M:
        if es_Carmichael(N):
            print(N)
            count += 1
        N += 1


getnumbers(10)
