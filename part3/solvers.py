def check_strict_diagonal_dominance(matrix):
    nrows = len(matrix)
    for row in range(nrows):
        diag = abs(matrix[row][row])
        off = sum(abs(matrix[row][col]) for col in range(nrows) if col != row)

        if diag < off:
            return False

    return True

def gauss_seidel(A, b, max_iter=1000, tol=1e-9):
    if not check_strict_diagonal_dominance(A):
        print("Matrix does not follow strict diagonal dominance")
        return None

    # A = [row[:-1] for row in matrix]
    # b = [row[-1] for row in matrix]

    n = len(A)

    # set all value of x to 0 initially 
    x = [0.0 for _ in range(n)]
    
    for iteration in range(max_iter):
        x_old = x.copy()
        
        for i in range(n):
            sum1 = 0.0  # sum for j < i (new values)
            for j in range(i):
                sum1 += A[i][j] * x[j]
            
            sum2 = 0.0  # sum for j > i (old values)
            for j in range(i+1, n):
                sum2 += A[i][j] * x_old[j]
            
            # update x[i]
            x[i] = (b[i] - sum1 - sum2) / A[i][i]
        
        if any(abs(xi) > 1e50 for xi in x):
            raise ValueError(f"Divergent at iteration {iteration + 1}.")

        # check convergence
        error = 0.0
        for i in range(n):
            error += (x[i] - x_old[i])**2
        error = error ** 0.5
        
        if error < tol:
            # print(f"Converged in {iteration+1} iterations")
            return x
    
    print("Did not converge within max_iter")
    return x
