#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
La actividad 8 consiste en implementar el método de Schönhage-Strassen para multiplicar dos polinomios.
Se compone principalmente de las funciones mult_ss_mod(f,g,k,p) y mult_pol_mod(f,g,p).
"""




def mult_ss_mod(f,g,k,p):
    """
    Programa principal para multiplicar polinomios en el anillo (Z/pZ)[x]/<x^2^k+1>, con el método de Schönhage-Strassen.
    Parámetros de entrada:
        f. Polinomio 1 en formato lista de coeficientes
        g. Polinomio 2 en formato lista de coeficientes
        k, p. Coeficientes usados para la descripción del anillo en el que se realiza la multiplicación.
    """
    ## datos del problema
    k1 = k//2
    k2 = k-k1
    n1,n2 = 2**k1, 2**k2
    n = 2**k   
    f += [0] * (n - len(f))
    g += [0] * (n - len(g))
    
    ## caso base
    if   k == 0:
        return [(f[0]*g[0]) % p]
    elif k == 1:
        res = [0] * 2
        res[0] = (f[0]*g[0] - f[1]*g[1])  %p
        res[1] = (f[1]*g[0] + f[0]*g[1])  %p
        return res
    elif k == 2:
        res = [0] * 4
        res[0] = (f[0]*g[0]-f[1]*g[3]-f[3]*g[1]-f[2]*g[2]) %p
        res[1] = (f[1]*g[0]+f[0]*g[1]-f[2]*g[3]-f[3]*g[2]) %p
        res[2] = (f[0]*g[2]+f[2]*g[0]+f[1]*g[1]-f[3]*g[3]) %p
        res[3] = (f[2]*g[1]+f[1]*g[2]+f[0]*g[3]+f[3]*g[0]) %p
        return res
    
    ## caso recursivo
    else:
        ftilde , gtilde = [],[]
        i=0
        while i < n:
            ftilde.append (f[i:i+n1] + [0]*n1)
            gtilde.append (g[i:i+n1] + [0]*n1)
            i += n1
        coef = (2*n1)//n2   
        beta_shift_f = [shift(ftilde[i],coef*i) for i in range(n2)]
        beta_shift_g = [shift(gtilde[i],coef*i) for i in range(n2)]
        fft_f = fft(beta_shift_f,coef*2,p)
        fft_g = fft(beta_shift_g,coef*2,p)
        transformed = [mult_ss_mod(fft_f[i],fft_g[i],k1+1,p) for i in range(n2)] 
        invtemp = ifft(transformed,coef*2,p)
        htilde = [shift(invtemp[i],coef*(-i)) for i in range(n2)]
        
        ## reconstruir los resultados:
        h = []
        h.append(htilde[0][:n1])
        for i in range(n2-1):
            h.append( [x+y for x,y in zip(htilde[i][n1::],htilde[i+1][:n1])]  )     
        h.append(htilde[n2-1][n1:])
        final = [x %p for sub in h for x in sub] 
        final = clear_degree(final,n,p)       
        return final 
    

def mult_pol_mod(f,g,p):
    """
    Función principal. Dados dos polinomios en forma de lista f y g, se calcula su productos en el anillo (Z/pZ)[x].
    Si el resultado es polinomio nulo, devluelve una lista vacía.
    """
    l1 = count_degree(f)
    l2 = count_degree(g)
    k = 0
    while l1+l2 >= 2**k:
        k+=1
    res = mult_ss_mod(f,g,k,p)
    while (len(res) > 0 and res[-1] == 0):    
        res.pop(-1)
    return res
    

def clear_degree(lis,target,p):
    """
    Función auxiliar. al recibir un polinomio en formato lista de grado más alto que n, se lo convierte en un polinomio
    en su grado correspondiente en el anillo A[x]/<x^n+1>,
    """
    a = len(lis)
    if a == target:
        return lis
    else:
        left = lis[:target]
        right = lis[target::]+[0]*(2*target-a)
#        print(right)
        m = [(x +(-1)*y ) %p for (x,y) in zip(left,right)]
    return m
    

def shift(lis, index):
    """
    Función auxiliar que al recibir un polinomio con sus coeficientes en lista en el anillo A[x]/<x^n+1>,
     devuelve el resulltado del polinimio multiplicado por x^(index) en el anillo A[x]/<x^n+1>.
    """
    n = len(lis)
    index = index %(2*n)
    if index == 0:
        return lis
    if index <=n:
            left = [x*(-1) for x in lis[-index:]]
            lis = left+lis[:-index]
            return lis
    else:
        index = index % n
        left = lis[-index:]
        lis = left+[x*(-1) for x in lis[:n-index]]
        return lis


def fft(pol,coef,p):
    """
    Función auxiliar. Implementa el algoritmo de la Transformada Rápida de Fourier (FFT)
    """
    n = len(pol)
    if n == 1:
        return pol
    pol_even = pol[::2]
    pol_odd  = pol[1::2]
    a_even = fft(pol_even,coef*2,p)
    a_odd = fft(pol_odd,coef*2,p)
    a = [0]*n
    for i in range(n//2):
        first = a_even[i]
        second = (shift(a_odd[i],(coef)*i))
        a[i] = [(x + y) % p for x, y in zip(first, second)]
        a[i+n//2] = [(x - y) % p for x, y in zip(first, second)]
    return a


def ifft(a,coef,p):
    """
    Función auxiliar. Implementa el algoritmo de la Transformada Rápida de Fourier Inversa (IFFT)
    """
    n = len(a)
    inv = pow(n,p-2,p)
    matrix = fft(a,coef*(-1),p)  #DFT(xi^(-1))
    res = [[ (i * inv) % p for i in sub ] for sub in matrix]
    return res


def count_degree(lis):
    """
    Función auxiliar. Devuelve el grado del polinomio (en formato lista de coeficientes) recibido como parámetro.
    """
    if all(x == 0 for x in lis):
        return 0
    else:      
        n = len(lis)
        pos = len(lis)
        i = 0
        while lis[pos-1] == 0:
            pos-=1
            i+=1
        return n-i
