import numpy as np
import math

# Ngưỡng sai số toàn cục
epsilon = 1e-9

# Làm sạch sai số chấm động, hỗ trợ cả số thực và số phức.
def clean_value(x):
    # Nếu là số phức
    if isinstance(x, complex) or type(x).__name__ in ('complex128', 'complex64'):
        r = clean_value(x.real)
        i = clean_value(x.imag)
        if i == 0.0: return r
        return complex(r, i)
    
    # Nếu là số thực
    if abs(x) < epsilon: return 0.0

    rounded_x = round(float(x), 8)
    if abs(x - rounded_x) < epsilon: return rounded_x + 0.0

    return float(x) + 0.0

# ============================================================
# Các hàm bổ trợ
# ============================================================

# Hàm chuyển vị ma trận
def transpose(M):
    rows = len(M)
    cols = len(M[0])
    return [[M[i][j] for i in range(rows)] for j in range(cols)]

# Hàm nhân 2 ma trận
def matmul(A, B):
    rows_A, cols_A = len(A), len(A[0])
    rows_B, cols_B = len(B), len(B[0])
    if cols_A != rows_B:
        raise ValueError("Kích thước ma trận không hợp lệ để nhân.")
    
    C = [[0.0] * cols_B for _ in range(rows_A)]
    for i in range(rows_A):
        for j in range(cols_B):
            for k in range(cols_A):
                C[i][j] += A[i][k] * B[k][j]
    return C

# NTính c * vector với c là số thực
def scalar_multiply(c, vector):
    return [c * x for x in vector]

# ============================================================
# Thuật toán phân rã SVD
# ============================================================

# Phân tích giá trị suy biến A = U * S * V^T
# Chỉ dùng np.linalg.eig để tìm trị riêng
def svd_manual(A):
    m = len(A)
    n = len(A[0])
    
    # Bước 1: Tính ma trận A^T * A (Kích thước n x n)
    A_T = transpose(A)
    ATA = matmul(A_T, A)
    
    # Bước 2: Tính trị riêng bằng np.linalg.eig
    eigenvalues, V_np = np.linalg.eig(np.array(ATA, dtype=float))
    
    # Bước 3: Thu thập các cặp (trị riêng, vector riêng)
    pairs = []
    for i in range(n):
        # A^T A là ma trận đối xứng nên trị riêng chắc chắn là số thực
        val = clean_value(eigenvalues[i])
        if isinstance(val, complex): val = val.real 
        
        vec = [clean_value(V_np[j][i]) for j in range(n)]
        # Đảm bảo vector riêng là số thực
        vec = [v.real if isinstance(v, complex) else v for v in vec]
        pairs.append((val, vec))
        
    # Bước 4: Sắp xếp trị riêng giảm dần
    pairs.sort(key=lambda x: x[0], reverse=True)
    
    U_cols = []
    S_diag = []
    V_cols = []
    
    # Bước 5: Xây dựng U, S, V
    for val, vec in pairs:
        # Chỉ lấy các giá trị suy biến > 0 (khử nhiễu)
        if val > epsilon:
            sigma = math.sqrt(val)
            S_diag.append(sigma)
            V_cols.append(vec)
            
            # Tính vector u_i = (A * v_i) / sigma
            # Bản chất là nhân ma trận A (m x n) với vector cột v_i (n x 1)
            Av = matmul(A, [[x] for x in vec])
            u_i = [Av[k][0] / sigma for k in range(m)]
            U_cols.append(u_i)
            
    # Xây dựng các ma trận đầu ra

    # Hạng của ma trận
    r = len(S_diag) 

    # Xử lý trường hợp hạng = 0
    if r == 0:
        # Gán vector đơn vị đầu tiên cho U (chiều dài m) và V^T (chiều dài n)
        # S vẫn là ma trận 1x1 chứa số 0.0
        U_zero = [[1.0 if i == 0 else 0.0] for i in range(m)]
        S_zero = [[0.0]]
        VT_zero = [[1.0 if j == 0 else 0.0 for j in range(n)]]
        return U_zero, S_zero, VT_zero
    
    # Ma trận U (m x r)
    U = [[U_cols[j][i] for j in range(r)] for i in range(m)]
    
    # Ma trận S (r x r)
    S = [[S_diag[i] if i == j else 0.0 for j in range(r)] for i in range(r)]
    
    # Ma trận V^T (r x n)
    V_T = [[V_cols[i][j] for j in range(n)] for i in range(r)]
    
    # Làm sạch sai số lần cuối trước khi trả về
    U = [[clean_value(x) for x in row] for row in U]
    S = [[clean_value(x) for x in row] for row in S]
    V_T = [[clean_value(x) for x in row] for row in V_T]
    
    return U, S, V_T

# ============================================================
# Các hàm hiển thị và kiểm chứng
# ============================================================

# Định dạng số có 5 chữ số thập phân
def format_num(val):
    return f"{val:.5f}"

# In ma trận
def print_matrix(name, matrix):
    print(f"   + Ma trận {name}:")
    for row in matrix:
        print("     [" + ", ".join(format_num(val) for val in row) + "]")

# Kiểm chứng thuật toán phân ra SVD
def verify_svd(A, U, S, V_T):
    if U is None or S is None or V_T is None:
        print("   -> LỖI: Không thể phân tích SVD.")
        return
    
    # Kiểm tra khôi phục ma trận: A = U * S * V^T
    US = matmul(U, S)
    A_reconstructed = matmul(US, V_T)
    print_matrix("A tái tạo (U * S * V^T)", A_reconstructed)
    
    # Kiểm tra tính trực giao của U: U^T * U = I
    U_T = transpose(U)
    UT_U = matmul(U_T, U)
    
    # Kiểm tra tính trực giao của V: V * V^T = I
    # Vì ta đang có V_T, nên V_T * (V_T)^T = V_T * V = I
    V = transpose(V_T)
    VT_V = matmul(V_T, V)
    
    A_np = np.array(A, dtype=float)
    A_rec_np = np.array(A_reconstructed, dtype=float)
    I_r = np.eye(len(S))
    
    verify_epsilon = 1e-5 
    
    is_reconstruct_ok = np.allclose(A_np, A_rec_np, atol=verify_epsilon)
    is_U_ortho = np.allclose(np.array(UT_U), I_r, atol=verify_epsilon)
    is_V_ortho = np.allclose(np.array(VT_V), I_r, atol=verify_epsilon)
    
    print(f"   + Kiểm tra trực giao U (U^T * U = I): {'Thành công' if is_U_ortho else 'Thất bại'}")
    print(f"   + Kiểm tra trực giao V (V^T * V = I): {'Thành công' if is_V_ortho else 'Thất bại'}")
    
    if is_reconstruct_ok and is_U_ortho and is_V_ortho:
        print("   -> Kết luận: Thành công. Thuật toán SVD hoạt động hoàn hảo!")
    else:
        print("   -> Kết luận: Thất bại. Có lỗi trong quá trình phân tích.")

if __name__ == "__main__":
    # 1. Ma trận vuông 3x3
    A1 = [[ 1.0,  2.0,  3.0], 
          [ 4.0,  5.0,  6.0], 
          [ 7.0,  8.0,  9.0]]
          
    # 2. Ma trận chữ nhật 4x2 (Nhiều dòng hơn cột)
    A2 = [[ 2.0,  4.0], 
          [ 1.0,  3.0], 
          [ 0.0,  0.0], 
          [ 0.0,  0.0]]
          
    # 3. Ma trận chữ nhật 2x4 (Nhiều cột hơn dòng)
    A3 = [[ 3.0,  2.0,  2.0,  0.0], 
          [ 2.0,  3.0, -2.0,  0.0]]
    
    # 4. Ma trận suy biến (Rank = 2 < 3) - Dòng 3 = Dòng 1 + Dòng 2
    A4 = [[ 1.0,  2.0,  3.0], 
          [ 4.0,  5.0,  6.0], 
          [ 5.0,  7.0,  9.0]]
          
    # 5. Ma trận kích thước lớn 5x5 (Kiểm tra giới hạn bậc phương trình)
    A5 = [[ 2.0,  0.0,  0.0,  0.0,  1.0], 
          [ 0.0,  3.0,  0.0,  0.0,  0.0], 
          [ 0.0,  0.0,  4.0,  0.0,  0.0], 
          [ 0.0,  0.0,  0.0,  5.0,  0.0], 
          [ 1.0,  0.0,  0.0,  0.0,  6.0]]
    
    # 6. Ma trận toàn số 0
    A6 = [[ 0.0,  0.0,  0.0], 
          [ 0.0,  0.0,  0.0]]
          
    # 7. Ma trận 1D (vector dòng 1x4)
    A7 = [[ 1.0, -2.0,  3.0, -4.0]]
    
    # 8. Ma trận đơn vị 3x3 (Trị riêng lặp)
    A8 = [[ 1.0,  0.0,  0.0], 
          [ 0.0,  1.0,  0.0], 
          [ 0.0,  0.0,  1.0]]

    test_cases = [
        ("TESTCASE 1: MA TRẬN VUÔNG 3x3", A1),
        ("TESTCASE 2: MA TRẬN CHỮ NHẬT 4x2", A2),
        ("TESTCASE 3: MA TRẬN CHỮ NHẬT 2x4", A3),
        ("TESTCASE 4: MA TRẬN SUY BIẾN", A4),
        ("TESTCASE 5: MA TRẬN KÍCH THƯỚC LỚN (5x5)", A5),
        ("TESTCASE 6: MA TRẬN KHÔNG", A6),
        ("TESTCASE 7: MA TRẬN 1 CHIỀU (VECTOR DÒNG 1x4)", A7),
        ("TESTCASE 8: MA TRẬN ĐƠN VỊ 3x3", A8)
    ]

    for title, matrix in test_cases:
        print("\n" + "="*70)
        print(f"  {title}")
        print("="*70)

        print("[0] DỮ LIỆU ĐẦU VÀO:")
        print_matrix("A", matrix)
        print("-" * 30)
        
        print("[1] KẾT QUẢ PHÂN TÍCH SVD:")
        U, S, V_T = svd_manual(matrix)
        print_matrix("U", U)
        print_matrix("S", S)
        print_matrix("V^T", V_T)
        print("-" * 30)
        
        print("[2] KIỂM CHỨNG TOÁN HỌC:")
        verify_svd(matrix, U, S, V_T)