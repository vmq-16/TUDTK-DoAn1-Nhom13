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

    #Normalize
    A = [[float(x) for x in row] for row in A] 
    b = [float(x) for x in b] 

    #Join matrix M(A | b)
    M = [A[i] + [b[i]] for i in range(len(A))]

    nrows = len(M)
    ncols = len(M[0])
    swap_count = 0

    print(f"M: {M}")
    cur_row = 0
    
    for k in range(ncols-1):
        if cur_row >= nrows:
            break

        pivot = (cur_row, k)
        #Finding the row with the largest number within the same col
        for row in range(cur_row + 1, nrows):
            # print(f"Checking {row, k}, value: {M[row][k]} compare with pivot at {pivot} with value {M[pivot[0]][pivot[1]]}")
            if abs(M[row][k]) > abs(M[pivot[0]][pivot[1]]):
                pivot = (row, k)

        # print(f"Max value is {M[pivot[0]][pivot[1]]} at point {pivot}")

        if abs(M[pivot[0]][pivot[1]]) < epsilon:
            # print(f"Pivot does not exist at {(cur_row, k)}")
            continue

        if pivot[0] != cur_row:
            # print(f"Swapping row {pivot[0]} with row {cur_row}")
            M[cur_row], M[pivot[0]] = M[pivot[0]], M[cur_row]
            swap_count += 1

        # print(f"at k = {k}, before elim M = {M}")

        for row in range(cur_row + 1, nrows):
            factor = M[row][k] / M[cur_row][k]

            for col in range(k, ncols):
                M[row][col] -= factor * M[cur_row][col]
                if abs(M[row][col]) < epsilon:
                    M[row][col] = 0
        

        # print(f"at k = {k} after elim, M = {M}")
        cur_row += 1

    U = [row[:-1] for row in M]
    c = [row[-1] for row in M]

    print(f"U: {U}")
    print(f"c: {c}")

    for row in range(nrows):
        if all(abs(M[row][col]) < epsilon for col in range(ncols - 1)) and abs(M[row][ncols-1]) >= epsilon:
            raise ValueError("No solution")

    x = back_substitution(U, c)
    return U, x, swap_count

def back_substitution(U, c):
    nrows = len(U)
    ncols = len(U[0])
    pivot_cols = []

    cur_row = 0 
    for k in range(ncols):
        if cur_row >= nrows:
            break
       
        if abs(U[cur_row][k]) < epsilon:
           continue
       
        pivot_cols.append((cur_row, k))
        cur_row += 1

    print(pivot_cols)

    pivot_only_cols = [c for (r,c) in pivot_cols]
    free_vars = [col for col in range(ncols) if col not in pivot_only_cols]

    print(free_vars)
    sol = [None]*ncols

    if free_vars:
        # assign free vars
        for i, col in enumerate(free_vars):
            sol[col] = f"t{i+1}"

    # back-substitution bottom-up
    for row, col in reversed(pivot_cols):
        print(f"{row, col}")
        expr = f"{c[row]}"

        for j in range(ncols - 1, col, -1):
            print(f"j = {j}")
            if sol[j] is not None:
                if "t" not in str(sol[j]):
                    print(sol[j])
                    expr += f" - {U[row][j] * float(eval(sol[j]))}"
                else:    
                    expr += f" - ({U[row][j]})*({sol[j]})"

        if abs(U[row][col] - 1) > epsilon:
            expr = f"({expr}) / {U[row][col]}"
            if "t" not in expr:
                expr = str(float(eval(expr)))

        print(f"at pivot {row, col}, the exp is {expr}")
        sol[col] = expr

    return sol
