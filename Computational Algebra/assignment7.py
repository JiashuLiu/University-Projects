#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Entrega 7 consiste en varias funciones, dentro de ellas, la función generar_primo(n,k) y la función generar_histograma().
Tarda dos minutos aprox. en generar el histograma de invocar 100 veces la función generar_primo(n,k).
"""

import random
import matplotlib.pyplot as plt
import numpy as np




def solovay_strassen(N):

    
    '''
    Dado N>=3, cuando N es par, devuelve False porque es compuesto. Si N es compuesto, puede devolver
    False o True depende de varias condiciones.
    Si N es primo, simpre devuelve True.
    '''
    if N %2 == 0:
        return False
    a = random.randint(1, N-1)
    x = gcd(a,N)
    if x != 1
        return False
    elif (pow(a, (N-1)//2, N)- simbolo_jacobi(a,N) )%N != 0:
        return False
    else:
        return True



def generar_primo(n,k):
    """
    Función principal, genera aleatoriamente un número de n dígitos y aplicar el multiple_test de solovay_strassen hasta
    que encuentre un número que pasa el multiple_test (pasa el solovay_strassen k veces).
    Devuelve una tupla (p,cnt) donde p es el número que pasa el test y cnt la cantidad de intentos.
    """
    start = 10**(n-1)
    end = (10**n)-1
    have_result=False
    cnt = 0
    while have_result == False:
        a = random.randint(start, end)
        cnt +=1
        if multiple_test(a,k):
            have_result = True
            p = a
        else:
            continue
    return(p,cnt)
    
def multiple_test(a,k):
    """
    Función auxiliar que para un número a dado, invoka la función solovay_strassen como mucho k veces.
    Si dentro de esas k vececs, alguna vez recibe un False, entonces no pasa el test.
    EL test se considera pasado si recibe k veces True de la función solovay_strassen. y devuelve un True.
    
    """
    res = True
    for i in range(k):
        m = solovay_strassen(a)
        if m == False:
            return False
        else:
            continue
    return res


    
        
        
        
def simbolo_jacobi(a,N): ## N impar no necesariamente primo
    '''
    Función auxliar que dado un número a y N impar, calcular su símbolo de Jacobi, 
    usando la ley de reciprocidad cuadrática y sus suplementos.
    Nota: he adaptado un algoritmo de la página de Wikipedia, se basa en ir reduciendo a mod N, hacer 
    divisiones por dos (ir cambiando el  simbolo de 1 a -1 en caso de que N mod 8 in (3,5)) y luego hacer cambio de a y N
    para caso de que a y N impares, cambia el signo según a y N mod 4.
    '''
    a = a % N              
    temp = 1
    while a != 0:
        while a%2 ==0:       
            a = a//2          
            r = N%8
            if r in(3,5):
                temp = -temp
        a , N = N, a
        if a % 4 == 3 and N % 4 == 3:   
            temp = -temp
        a = a % N
    if N == 1:
        return temp
    else:
        return 0
    

    
        
  
def gcd(a, b):
    """
    Función auxiliar que calcular el gcd de a y b.
    """
    r = a%b
    while r != 0:
        a, b, r = b, r, b%r
    return b
        





def generar_histograma():
    count = []
    for i in range(100):
        count.append(generar_primo(300,20)[1])
    n, bins, patches = plt.hist(x=count, bins='auto', color='#607c8e',
                            alpha=0.7, rwidth=0.85)
    plt.grid(axis='y', alpha=0.75)
    plt.xlabel('Intentos que ha costado')
    plt.ylabel('Frequencia')
    plt.title('Histograma de 100 recorridos')
    maxfreq = n.max()
    # Set a clean upper y-axis limit.
    plt.ylim(ymax=np.ceil(maxfreq / 10) * 10 if maxfreq % 10 else maxfreq + 10)
    plt.savefig("histograma.png",dpi=300)
    
    
    


