import sys
import os
import numpy as np

# Tái sử dụng các hàm của file part1/gaussian.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from part1.gaussian import gaussian_elimination, clean_value

# Ngưỡng sai số toàn cục
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

# Hàm hỗ trợ format chuỗi số thực/phức khi in
def format_complex(val):
    if isinstance(val, complex) or type(val).__name__ in ('complex128', 'complex64'):
        return f"{val.real:.4f}{val.imag:+.4f}j" if val.imag != 0 else f"{val.real:.4f}"
    return f"{val:.4f}"

# Hỗ trợ in ma trận
def print_matrix(name, matrix):
    print(f"   + Ma trận {name}:")
    for row in matrix:
        formatted_row = [format_complex(val) for val in row]
        print("     [" + ", ".join(formatted_row) + "]")

# Kiểm chứng kết quả chéo hóa với NumPy
def verify_diagonalization(A_origin, P, D):
    A_np = np.array(A_origin, dtype=float)
    print_matrix("A gốc", A_origin)
    
    if P is None or D is None:
        # Nhờ NumPy xác nhận lại xem có đúng là suy biến không
        _, P_np_raw = np.linalg.eig(A_np)
        rank_np = np.linalg.matrix_rank(P_np_raw, tol=epsilon)
        
        print(f"   + Số vector riêng (NumPy tìm được) : {rank_np}/{len(A_origin)}")
        if rank_np < len(A_origin):
            print("   -> Kết luận: Thành công. NumPy cũng xác nhận ma trận không thể chéo hóa.")
        else:
            print("   -> Kết luận: Thất bại. NumPy chéo hóa được còn thuật toán cài đặt thì không.")
        return

    P_np = np.array(P, dtype=complex) 
    D_np = np.array(D, dtype=complex)
    
    try:
        P_inv = np.linalg.inv(P_np)
        A_reconstructed = P_np @ D_np @ P_inv
        
        # In ma trận tái tạo
        print_matrix("A tái tạo (P * D * P^-1)", A_reconstructed.tolist())
        
        if np.allclose(A_np, A_reconstructed.real, atol=epsilon):
            print("   -> Kết luận: Thành công. A = P * D * P^-1 (Sai số nằm trong ngưỡng cho phép).")
        else:
            print("   -> Kết luận: Thất bại. P * D * P^-1 không khớp với A.")
    except np.linalg.LinAlgError:
        print("   -> Kết luận: Thất bại. Ma trận P không khả nghịch.")

if __name__ == "__main__":
    
    # Ma trận 2x2 chéo hóa được
    A1 = [[4.0, 1.0], 
          [2.0, 3.0]]
    
    # Ma trận 3x3 không chéo hóa được
    A2 = [[1.0, 1.0, 0.0], 
          [0.0, 1.0, 1.0], 
          [0.0, 0.0, 1.0]]
    
    # Ma trận 3x3 đối xứng
    A3 = [[ 2.0, -1.0,  0.0], 
          [-1.0,  2.0, -1.0], 
          [ 0.0, -1.0,  2.0]]
    
    # Ma trận 5x5 chéo hóa được
    A4 = [[1, 2, 3, 4, 5], 
          [0, 2, 3, 4, 5], 
          [0, 0, 3, 4, 5], 
          [0, 0, 0, 4, 5], 
          [0, 0, 0, 0, 5]]
    
    # Ma trận 5x5 không chéo hóa được
    A5 = [[1, 1, 0, 0, 0], 
          [0, 1, 0, 0, 0], 
          [0, 0, 2, 0, 0], 
          [0, 0, 0, 3, 0], 
          [0, 0, 0, 0, 4]]
    
    # Ma trận phép quay (sinh ra số phức)
    A6 = [[ 0.0, -1.0], 
          [ 1.0,  0.0]]

    test_cases = [
        ("TESTCASE 1: MA TRẬN 2x2 CHÉO HÓA ĐƯỢC", A1),
        ("TESTCASE 2: MA TRẬN 3x3 KHÔNG CHÉO HÓA ĐƯỢC", A2),
        ("TESTCASE 3: MA TRẬN 3x3 ĐỐI XỨNG", A3),
        ("TESTCASE 4: MA TRẬN 5x5 CHÉO HÓA ĐƯỢC", A4),
        ("TESTCASE 5: MA TRẬN 5x5 KHÔNG CHÉO HÓA ĐƯỢC", A5),
        ("TESTCASE 6: MA TRẬN PHÉP QUAY (SINH RA SỐ PHỨC)", A6)
    ]

    for title, matrix in test_cases:
        print("\n" + "="*75)
        print(f"  {title}")
        print("="*75)
        
        print("[0] DỮ LIỆU ĐẦU VÀO:")
        print_matrix("A", matrix)
        print("-" * 30)
        
        print("[1] KẾT QUẢ CHÉO HÓA:")
        P, D = diagonalize(matrix)
        
        if P is None or D is None:
            print("   -> P và D = None (Số vector riêng ít hơn bậc của trị riêng).")
        else:
            print_matrix("P (Các vector riêng)", P)
            print_matrix("D (Các tri riêng)", D)
            
        print("-" * 30)
        
        print("[2] KIỂM CHỨNG:")
        verify_diagonalization(matrix, P, D)