import sys
import os
import numpy as np

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from part1.gaussian import gaussian_elimination, clean_value

epsilon = 1e-9

# Chéo hóa ma trận
def diagonalize(A):
    n = len(A)
    eigenvalues, P_np = np.linalg.eig(A)
    
    P = [[clean_value(P_np[i][j]) for j in range(n)] for i in range(n)]
        
    # Gọi Khử Gauss chạy ngầm (silent=True) để lấy ma trận bậc thang U
    U, _, _ = gaussian_elimination(P, b=None, silent=True)
    
    # Tính hạng
    rank = 0
    for row in U:
        if any(abs(val) > epsilon for val in row):
            rank += 1
            
    if rank < n:
        return None, None
        
    D = [[clean_value(eigenvalues[i]) if i == j else 0.0 for j in range(n)] for i in range(n)]
    return P, D

def format_complex(val):
    """Hàm hỗ trợ format chuỗi số thực/phức khi in"""
    if isinstance(val, complex) or type(val).__name__ in ('complex128', 'complex64'):
        return f"{val.real:.4f}{val.imag:+.4f}j" if val.imag != 0 else f"{val.real:.4f}"
    return f"{val:.4f}"

# Hỗ trợ in ma trận
def print_matrix(name, matrix):
    print(f"   + Ma tran {name}:")
    for row in matrix:
        formatted_row = [format_complex(val) for val in row]
        print("     [" + ", ".join(formatted_row) + "]")

# Kiểm chứng kết quả chéo hóa với NumPy
def verify_diagonalization(A_origin, P, D):
    A_np = np.array(A_origin, dtype=float)
    print_matrix("A goc", A_origin)
    
    if P is None or D is None:
        # Nhờ NumPy xác nhận lại xem có đúng là suy biến không
        _, P_np_raw = np.linalg.eig(A_np)
        rank_np = np.linalg.matrix_rank(P_np_raw, tol=epsilon)
        
        print(f"   + So vector rieng (NumPy tim duoc) : {rank_np}/{len(A_origin)}")
        if rank_np < len(A_origin):
            print("   -> Ket luan: PASSED. NumPy cung xac nhan MA TRAN KHONG THE CHEO HOA.")
        else:
            print("   -> Ket luan: FAILED. NumPy cheo hoa duoc nhung thuat toan cai dat thi khong.")
        return

    P_np = np.array(P, dtype=complex) 
    D_np = np.array(D, dtype=complex)
    
    try:
        P_inv = np.linalg.inv(P_np)
        A_reconstructed = P_np @ D_np @ P_inv
        
        # In ma trận tái tạo
        print_matrix("A tai tao (P * D * P^-1)", A_reconstructed.tolist())
        
        if np.allclose(A_np, A_reconstructed.real, atol=epsilon):
            print("   -> Ket luan: PASSED. A = P * D * P^-1 (Sai so nam trong nguong cho phep).")
        else:
            print("   -> Ket luan: FAILED. P * D * P^-1 khong khop voi A.")
    except np.linalg.LinAlgError:
        print("   -> Ket luan: FAILED. Ma tran P khong kha nghich.")

if __name__ == "__main__":
    
    A1 = [[4.0, 1.0], 
          [2.0, 3.0]]
    
    A2 = [[1.0, 1.0, 0.0], 
          [0.0, 1.0, 1.0], 
          [0.0, 0.0, 1.0]]
    
    A3 = [[ 2.0, -1.0,  0.0], 
          [-1.0,  2.0, -1.0], 
          [ 0.0, -1.0,  2.0]]
    
    A4 = [[1, 2, 3, 4, 5], 
          [0, 2, 3, 4, 5], 
          [0, 0, 3, 4, 5], 
          [0, 0, 0, 4, 5], 
          [0, 0, 0, 0, 5]]
    
    A5 = [[1, 1, 0, 0, 0], 
          [0, 1, 0, 0, 0], 
          [0, 0, 2, 0, 0], 
          [0, 0, 0, 3, 0], 
          [0, 0, 0, 0, 4]]
    
    A6 = [[ 0.0, -1.0], 
          [ 1.0,  0.0]]

    test_cases = [
        ("TESTCASE 1: MA TRAN 2x2 CHEO HOA DUOC", A1),
        ("TESTCASE 2: MA TRAN 3x3 KHONG CHEO HOA DUOC", A2),
        ("TESTCASE 3: MA TRAN 3x3 DOI XUNG", A3),
        ("TESTCASE 4: MA TRAN 5x5 CHEO HOA DUOC", A4),
        ("TESTCASE 5: MA TRAN 5x5 KHONG CHEO HOA DUOC", A5),
        ("TESTCASE 6: MA TRAN PHEP QUAY (SINH RA SO PHUC)", A6)
    ]

    for title, matrix in test_cases:
        print("\n" + "="*75)
        print(f"  {title}")
        print("="*75)
        
        print("[0] DU LIEU DAU VAO:")
        print_matrix("A", matrix)
        print("-" * 30)
        
        print("[1] KET QUA CHEO HOA:")
        P, D = diagonalize(matrix)
        
        if P is None or D is None:
            print("   -> P va D = None (So vector rieng it hon bac cua tri rieng).")
        else:
            print_matrix("P (Cac vector rieng)", P)
            print_matrix("D (Cac tri rieng)", D)
            
        print("-" * 30)
        
        print("[2] KIEM CHUNG:")
        verify_diagonalization(matrix, P, D)