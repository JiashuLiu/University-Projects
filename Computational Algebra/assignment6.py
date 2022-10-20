#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Utilizar el método p − 1 de Pollard para factorizar el número N dado en el final de la entrega. Imprime una tupla de factores
p y q como resultado.

"""
import random
import math

def pollard(N,B):
    """
    Función principal que escoge un a aleatoriamente y corre el algoritmo. 
    Se reitera este proceso hasta sacar un factor p no trivial.
    """
    have_result=False
    while have_result == False:
        a = random.randrange(2, N)
        x = gcd_binario(a,N)
        if x !=1:
            have_result = True
            p = x
            q = N//x
        else:
            y = gcd_binario((betamod(a,B,N)-1)%N, N)
            if y != N and y!= 1:
                have_result = True
                p = y
                q = N//y    #usa floor division 
            else:
                continue
    return (p,q)

                
               

def get_beta(N,B):   
    """
    Función auxiliar para calcular todos los factores de beta, y les guarda en una lista.
    
    """
    list1 = []
    for i in range(2,B):
        if es_primo(i):
            list1.append( i**math.ceil( math.log(N,i)) )
        else:
            continue
    return  list1


def betamod(a,B,N): 
    """
    Función auxiliar para calcular a**beta modulo N. Usa las función potencia_mod vista en clase.
    
    """
    res = 1
    list1 = get_beta(N,B)   
    first = list1[0]
    rest = list1[1:]
    res = potencia_mod(a,first,N) 
    for i in rest:
        res = potencia_mod(res,i,N)
    return res
        
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
       
def multiplicar_mod(a, b, N):
    c = a*b
    c %= N
    return c
def gcd_binario(x,y):    # (x,y) != (0,0)
    x = abs(x)
    y = abs(y)
    xespar = x%2 == 0
    yespar = y%2 == 0
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


N = 1542201487980564464479858919567403438179217763219681634914787749213
B = 100

print(pollard(N,B))


        
        
            

