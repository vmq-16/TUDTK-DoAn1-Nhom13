import math
import copy

# Khai báo hằng số epsilon theo thống nhất của nhóm
EPSILON = 1e-9

def clean_value(x):
    """
    Làm sạch sai số chấm động.
    Nếu giá trị cực nhỏ (nhỏ hơn EPSILON), gán thẳng về 0.0.
    """
    if math.isclose(x, 0, abs_tol=EPSILON):
        return 0.0
    return x

def to_rref(A):
    """
    Đưa ma trận A về Dạng bậc thang dòng rút gọn (RREF).
    Được nâng cấp để xử lý triệt để sai số chấm động.
    """
    # Khởi tạo bản sao và làm sạch dữ liệu đầu vào
    mat = [[clean_value(val) for val in row] for row in A]
    m = len(mat)
    n = len(mat[0]) if m > 0 else 0
    
    pivot_cols = []
    r = 0
    
    for c in range(n):
        if r >= m:
            break
            
        # 1. Partial Pivoting
        pivot_row = r
        max_val = abs(mat[r][c])
        for i in range(r + 1, m):
            if abs(mat[i][c]) > max_val:
                max_val = abs(mat[i][c])
                pivot_row = i
                
        # Kiểm tra Pivot == 0 bằng cấu trúc thống nhất của nhóm
        if math.isclose(max_val, 0, abs_tol=EPSILON):
            for i in range(r, m):
                mat[i][c] = 0.0 # Ép về 0.0 để tránh rác dữ liệu
            continue
            
        # 2. Hoán đổi dòng
        mat[r], mat[pivot_row] = mat[pivot_row], mat[r]
        pivot_cols.append(c)
        
        # 3. Chuẩn hóa dòng pivot (pivot = 1)
        pivot_val = mat[r][c]
        for j in range(c, n):
            mat[r][j] = clean_value(mat[r][j] / pivot_val)
            
        # 4. Khử các phần tử khác trong cột c
        for i in range(m):
            if i != r:
                factor = mat[i][c]
                for j in range(c, n):
                    mat[i][j] -= factor * mat[r][j]
                    mat[i][j] = clean_value(mat[i][j]) # Dọn dẹp rác lập tức
                    
        r += 1
        
    return mat, pivot_cols

def rank_and_basis(A):
    """
    Tính Hạng và cơ sở của các không gian.
    Trả về: rank, col_space, row_space, null_space
    """
    m = len(A)
    n = len(A[0]) if m > 0 else 0
    
    rref_mat, pivot_cols = to_rref(A)
    
    # 1. Hạng (Rank): Số dòng khác 0 trong bậc thang rút gọn
    rank = len(pivot_cols)
    
    # 2. Không gian cột C(A): Sinh bởi các cột pivot của ma trận A gốc
    col_space = []
    for c in pivot_cols:
        col_vec = [clean_value(A[i][c]) for i in range(m)]
        col_space.append(col_vec)
        
    # 3. Không gian dòng R(A): Sinh bởi các dòng khác 0 trong bậc thang dòng rút gọn
    row_space = []
    for i in range(rank):
        row_space.append(rref_mat[i])
        
    # 4. Không gian nghiệm N(A): Tập nghiệm của hệ Ax = 0
    null_space = []
    free_cols = [c for c in range(n) if c not in pivot_cols]
    
    for free_col in free_cols:
        null_vec = [0.0] * n
        null_vec[free_col] = 1.0
        
        for i, pivot_col in enumerate(pivot_cols):
            # Tính và làm sạch giá trị vector nghiệm
            val = -rref_mat[i][free_col]
            null_vec[pivot_col] = clean_value(val)
            
        null_space.append(null_vec)
        
    return rank, col_space, row_space, null_space