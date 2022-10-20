#!/usr/bin/env python3
# -*- coding: utf-8 -*-


'''
La práctica se consiste en encontrar el dígito de la constante de Champernowne para una posición dada. 
Observamos que, al tratarse de una sucesión de números naturales, hay 9 números de un dígito, 
 hay 90 números de 2 dígitos... y así sucesivamente.
Una vez localizado dónde está la posición dada, es decir, la cantidad n de dígitos
  que contiene el número donde encuentra la posición, se calcula el dígito concreto 
  realizando divisiones enteras y de resto sobre el valor de números acumulados para llegar a la posición.
'''

def get_nvalue(n):
    '''
    Función auxiliar para calcular cuantos números hay en total con n dígitos.
    '''
    return (9 * n * 10 ** (n-1))


def find_digit(pos):
    '''
    Función principal que dado una posición en número mayor que 9, devuelve el dígito correspondiente. 
    '''
    # Paso 0: inicializar variables necesarias a 0
    cumulative = 0
    value = 0       
    n = 0

    # Paso 1: Calculamos y acumularmos los números con n dígitos 
    #   hasta que superemos la posición buscada
    while (cumulative < pos):  
        n += 1
        nvalue = get_nvalue(n)
        if (cumulative + nvalue > pos):
            value = pos - cumulative
        cumulative += nvalue     

    # Paso 2: Tras salir del bucle, se realizan las divisiones pertinentes
    #    para calcular número y dígito al que corresponde la posición pasada
    digit = value % n
    subValue = (value // n)
    # Si la división ha sido entera, hay que restar una unidad a la división
    if (digit == 0):
        subValue -= 1
    
    # Paso 3: Por último, se suman al número calculado tantas posiciones
    #    como valores se han dejado atrás en previas iteraciones
    finalValue = subValue + (10 ** (n-1))
    subValueString = str(finalValue)
    return subValueString[digit - 1]



def digit_at(pos):
    '''
    Función general para calcular el dígito de la constante correspondiente a la posición dada
    '''
    to_ret = pos
    # Para un valor de posición menor que 10, el dígito es igual a la posición.
    if (pos >= 10):
        to_ret = find_digit(pos)
    return int(to_ret)



'''
Se definen las posiciones que queremos buscar y se hace la multiplicación.
El resultado final se imprime por pantalla.
'''
to_query = [1, 100, 1000, 10000, 100000,1000000]
result = 1
for i in to_query:
    result *= digit_at(i)
print(result)
