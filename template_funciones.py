def construye_adyacencia(D,m): 
    # Función que construye la matriz de adyacencia del grafo de museos
    # D matriz de distancias, m cantidad de links por nodo
    # Retorna la matriz de adyacencia como un numpy.
    D = D.copy()
    l = [] # Lista para guardar las filas
    for fila in D: # recorriendo las filas, anexamos vectores lógicos
        l.append(fila<=fila[np.argsort(fila)[m]] ) # En realidad, elegimos todos los nodos que estén a una distancia menor o igual a la del m-esimo más cercano
    A = np.asarray(l).astype(int) # Convertimos a entero
    np.fill_diagonal(A,0) # Borramos diagonal para eliminar autolinks
    return(A)

def calculaLU(A):
    # matriz es una matriz de NxN
    # Retorna la factorización LU a través de una lista con dos matrices L y U de NxN.
    # Completar! Have fun
    m=A.shape[0]
    n=A.shape[1]
    Ac = A.copy()
    
    if m!=n:
        print('Matriz no cuadrada')
        return
    

    for j in range(n):
        if Ac[j, j] == 0:
            raise ValueError(f"Pivote nulo en columna {j}. No se puede continuar sin pivoteo.")
        for i in range(j + 1, n):
            multiplicador = Ac[i, j] / Ac[j, j]
            Ac[i, j] = multiplicador  # <-- lo guardás acá
            Ac[i, j + 1:] = Ac[i, j + 1:] - multiplicador * Ac[j, j + 1:]
                
            
    L = np.tril(Ac,-1) + np.eye(A.shape[0]) 
    U = np.triu(Ac)
    
    return L, U

def calcula_matriz_C(A): 
    # Función para calcular la matriz de trancisiones C
    # A: Matriz de adyacencia
    # Retorna la matriz C
    k = A.sum(axis=1)  # suma por filas: grado de cada página
    Kinv = np.diag([1/ki if ki != 0 else 0 for ki in k])
    C = A.T @ Kinv
    return C

    
def calcula_pagerank(A,alfa):
    # Función para calcular PageRank usando LU
    # A: Matriz de adyacencia
    # d: coeficientes de damping
    # Retorna: Un vector p con los coeficientes de page rank de cada museo
    C = calcula_matriz_C(A)
    N = ... # Obtenemos el número de museos N a partir de la estructura de la matriz A
    M = ...
    L, U = calculaLU(M) # Calculamos descomposición LU a partir de C y d
    b = ... # Vector de 1s, multiplicado por el coeficiente correspondiente usando d y N.
    Up = scipy.linalg.solve_triangular(L,b,lower=True) # Primera inversión usando L
    p = scipy.linalg.solve_triangular(U,Up) # Segunda inversión usando U
    return p

def calcula_matriz_C_continua(D): 
    # Función para calcular la matriz de trancisiones C
    # A: Matriz de adyacencia
    # Retorna la matriz C en versión continua
    D = D.copy()
    F = 1/D
    np.fill_diagonal(F,0)
    Kinv = ... # Calcula inversa de la matriz K, que tiene en su diagonal la suma por filas de F 
    C = ... # Calcula C multiplicando Kinv y F
    return C

def calcula_B(C, cantidad_de_visitas):
    B = np.eye(C.shape[0])  # C^0
    C_potencia = np.eye(C.shape[0])
    for _ in range(1, cantidad_de_visitas):
        C_potencia = np.dot(C_potencia, C)  # C^k
        B += C_potencia
    return B