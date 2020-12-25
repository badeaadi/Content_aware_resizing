"""
    PROIECT
    REDIMENSIONEAZA IMAGINI.
    Implementarea a proiectului Redimensionare imagini
    dupa articolul "Seam Carving for Content-Aware Iamge Resizing", autori S. Avidan si A. Shamir
    
    Badea Adrian Catalin, grupa 334, anul III, FMI
    
"""

import sys
import numpy as np
import pdb


def select_random_path(E):
    # pentru linia 0 alegem primul pixel in mod aleator
    line = 0
    col = np.random.randint(low=0, high=E.shape[1], size=1)[0]
    path = [(line, col)]
    for i in range(E.shape[0]):
        # alege urmatorul pixel pe baza vecinilor
        line = i
        # coloana depinde de coloana pixelului anterior
        if path[-1][1] == 0:  # pixelul este localizat la marginea din stanga
            opt = np.random.randint(low=0, high=2, size=1)[0]
        elif path[-1][1] == E.shape[1] - 1:  # pixelul este la marginea din dreapta
            opt = np.random.randint(low=-1, high=1, size=1)[0]
        else:
            opt = np.random.randint(low=-1, high=2, size=1)[0]
        col = path[-1][1] + opt
        path.append((line, col))

    return path


def select_greedy_path(E):
    
    # pentru linia 0 alegem cea mai buna coloana
    line = 0
    col = 0
    for j in range(1, E.shape[1]):
        if E[line][j] < E[line][col]:
            col = j
                                    
    path = [(line, col)]
    for i in range(E.shape[0]):
        
        line = i
        col = path[i][1]
        # Alegem cea mai mica coloana dintre cele 3
        col_chosen = col
        
        if col - 1 >= 0 and E[line][col - 1] < E[line][col_chosen]:
            col_chosen = col - 1
        
        if col + 1 < E.shape[1] and E[line][col + 1] < E[line][col_chosen]: 
            col_chosen = col + 1
            
        path.append((line, col_chosen))

    return path


def select_dynamic_programming_path(E):
    
    
    n, m = E.shape
    
    dp = np.zeros((n, m), np.int32)
    last = np.zeros((n, m, 2), np.uint32)
    
    for j in range(m):
        dp[0][j] = E[0][j]
    
    for i in range(1, n):
        for j in range(m):
            
            dp[i][j] = dp[i - 1][j]
            last[i][j] = (i - 1, j)
            
            if j - 1 >= 0 and dp[i - 1][j - 1] < dp[i][j]:
                dp[i][j] = dp[i - 1][j - 1]
                last[i][j] = (i - 1, j - 1)
            
            if j + 1 < m and dp[i - 1][j + 1] < dp[i][j]:
                dp[i][j] = dp[i - 1][j + 1]
                last[i][j] = (i - 1, j + 1)
            
            dp[i][j] += E[i][j]
        
    
    path = [(n - 1, 0)]
    
    for j in range(1, m):
        if (dp[n - 1][j] < dp[path[0]]):
            path[0] = (n - 1, j)
    
    
    i = 0
    while path[i][0] > 0:
        lin, col = path[i]
        path.append((last[lin][col][0], last[lin][col][1]))
        i += 1
    
    path.reverse()
    
    return path


def select_path(E, method):
    
    if method == 'aleator':
        return select_random_path(E)
    
    elif method == 'greedy':
        return select_greedy_path(E)
    
    elif method == 'programareDinamica':
        return select_dynamic_programming_path(E)
    else:
        print('The selected method %s is invalid.' % method)
        sys.exit(-1)