epsilon = 1e-9 

def gaussian_elimination(A, b):
    #Constraints Check
    if len(A) != len(b):
        raise ValueError("Matrix A and b must have the same row length")

    if len(A) == 0 or len(b) == 0:
        raise ValueError("Matrix A or b must not be empty")

    for row in A:
        if len(row) != len(A[0]):
            raise ValueError("All row must have the same length")

    if len(A) != len(A[0]):
        raise ValueError("Matrix A must be a square matrix")


    #Normalize
    A = [[float(x) for x in row] for row in A] 
    b = [float(x) for x in b] 

    print(f"Matrix A: {A}")
    print(f"Matrix b: {b}")

    #Join matrix M(A | b)
    M = [A[i] + [b[i]] for i in range(len(A))]

    print(f"Matrix M: {M}")

    nrows = len(M)
    swap_count = 0

    for k in range(nrows):
        pivot = k
        for row in range (k+1, nrows):
            #Find a row at col k where the value is highest
            if abs(M[row][k]) > abs(M[pivot][k]):
                pivot = row

        #Case where choosen pivot = 0
        if abs(M[pivot][k]) < epsilon:
            raise ValueError(f"Pivot does not exist at column {k}")
        
        #Swap row
        if pivot != k:
            M[k], M[pivot] = M[pivot], M[k]
            swap_count += 1

        #Start to perform elimination
        for row in range (k+1, nrows):
            factor = M[row][k] / M[k][k]

            for col in range (k, nrows + 1): #n + 1 to span over to the b column too
                M[row][col] -= factor * M[k][col]
                if abs(M[row][col]) < epsilon:
                    M[row][col] = 0.0

        print(f"M after {k}: {M}")

    U = [row[:-1] for row in M]
    c = [row[-1] for row in M]

    print(f"Matrix M after REF: {M}")

    return U, c, swap_count

def back_substitution(U, c):
    n = len(U)
    x = [0.0] * n

    for row in range(n-1, -1, -1):
        s = 0.0
        
        for col in range(row+1, n):
            s += U[row][col] * x[col]
        
        x[row] = (c[row] - s) / U[row][col]

    return x



