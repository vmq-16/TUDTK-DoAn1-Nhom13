from gaussian import gaussian_elimination, epsilon, clean_value

# Tìm hạng và cơ sở
def rank_and_basis(A):
    m = len(A)
    n = len(A[0]) if m > 0 else 0
    
    # Lấy ma trận RREF
    rref_mat, _, _ = gaussian_elimination(A, b = None, to_rref=True, silent = True)
    
    # Tìm các cột pivot để trả về hạng
    pivot_cols = []
    curr_row = 0
    for col in range(n):
        if curr_row < m and abs(rref_mat[curr_row][col]) >= epsilon:
            pivot_cols.append(col)
            curr_row += 1
            
    rank = len(pivot_cols)
    
    # Trích xuất C(A) và R(A)
    col_space = [[clean_value(A[i][c]) for i in range(m)] for c in pivot_cols]
    row_space = [[clean_value(val) for val in rref_mat[i]] for i in range(rank)]
    
    # Trích xuất N(A)
    null_space = []
    free_vars = [col for col in range(n) if col not in pivot_cols]
    
    for f_col in free_vars:
        null_vec = [0.0] * n
        null_vec[f_col] = 1.0
        for i, p_col in enumerate(pivot_cols):
            null_vec[p_col] = clean_value(-rref_mat[i][f_col])
        null_space.append([clean_value(v) for v in null_vec])
        
    return rank, col_space, row_space, null_space