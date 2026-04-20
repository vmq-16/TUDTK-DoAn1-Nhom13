import numpy as np
import sys
import os
import copy

epsilon = 1e-9

# Tái sử dụng các hàm từ part 1 và 2
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from part1.gaussian import gaussian_elimination
from part2.decomposition import svd_manual


# PHẦN 1: KIỂM TRA ĐIỀU KIỆN CHÉO TRỘI NGHIÊM NGẶT
def check_strict_diagonal_dominance(matrix):
    nrows = len(matrix)
    for row in range(nrows):
        diag = abs(matrix[row][row])
        off = sum(abs(matrix[row][col]) for col in range(nrows) if col != row)
        if diag <= off:
            return False
    return True


# PHẦN 2: GAUSS-SEIDEL
def gauss_seidel(A, b, max_iter = 1000, tol = epsilon):
    # kiểm tra điều kiện hội tụ
    if not check_strict_diagonal_dominance(A):
        return None, 0, False

    # khởi tạo nghiệm ban đầu x = [0, 0, ..., 0]
    n = len(A)
    x = [0.0 for _ in range(n)]
    
    for iteration in range(max_iter):
        # lưu nghiệm cũ để tính sai số
        x_old = x.copy()
        
        for i in range(n):
            # tính tổng từ j = 0 → i-1 (dùng giá trị mới x[j])
            sum1 = sum(A[i][j] * x[j] for j in range(i))
            # tính tổng từ j = i+1 → n-1 (dùng giá trị cũ x_old[j])
            sum2 = sum(A[i][j] * x_old[j] for j in range(i+1, n))
            
            # kiểm tra chia cho 0 (A[i][i] không được bằng 0)
            if abs(A[i][i]) < epsilon:
                raise ValueError("Phần tử trên đường chéo chính bằng 0")
                
            # công thức Gauss-Seidel:
            x[i] = (b[i] - sum1 - sum2) / A[i][i]
        
         # kiểm tra divergence (giá trị bị nổ)
        if any(abs(xi) > 1e50 for xi in x):
            raise ValueError("Phát hiện phân kỳ")

        # tính sai số ||x_new - x_old||
        error = sum((x[i] - x_old[i])**2 for i in range(n)) ** 0.5
        
        # nếu sai số nhỏ hơn ngưỡng → hội tụ
        if error < tol:
            return x, iteration + 1, True
            
    return x, max_iter, False


# PHẦN 3: CLASS LƯU KẾT QUẢ TRẢ VỀ
class SolverResult:
    def __init__(self, method, x, iterations, converged, note=""):
        self.method = method            # Tên phương pháp (Gauss, SVD...)
        self.x = x                      # Vector nghiệm
        self.iterations = iterations    # Số vòng lặp (nếu có)
        self.converged = converged      # Trạng thái hội tụ (True/False)
        self.note = note                # Ghi chú chi tiết


# PHẦN 4: HÀM GIẢI BẰNG KHỬ GAUSS
def solve_gauss(A, b):
    try:
        # Tạo bản sao độc lập để không làm hỏng ma trận gốc
        A_copy = copy.deepcopy(A)
        b_copy = copy.deepcopy(b)

        # Tái sử dụng hàm khử Gauss từ part 1
        U, b_new, _ = gaussian_elimination(A_copy, b=b_copy, to_rref=True, silent=True)
        
        if U is None or b_new is None:
             raise ValueError("Ma trận suy biến hoặc mất ổn định số học")
             
        return SolverResult("Khử Gauss", b_new, 0, True, "Giải chính xác")

    except Exception as e:
        return SolverResult("Khử Gauss", None, 0, False, f"Lỗi: {str(e)}")

# PHẦN 5: HÀM GIẢI BẰNG SVD
def solve_svd(A, b):
    try:
        # Tái sử dụng hàm phân rã SVD từ part 2
        U, S, Vt = svd_manual(A)
        
        if U is None or S is None or Vt is None:
             raise ValueError("Phân rã SVD thất bại")
             
        # Đưa về định dạng NumPy để nhân ma trận nhanh trong lúc benchmark
        U_np = np.array(U, dtype=float)
        S_np = np.array(S, dtype=float)
        Vt_np = np.array(Vt, dtype=float)
        b_np = np.array(b, dtype=float)

        # Tính ma trận nghịch đảo của S
        r = len(S_np)
        S_inv = np.zeros((r, r))
        for i in range(r):
            if S_np[i][i] > epsilon:
                S_inv[i][i] = 1.0 / S_np[i][i]

        # Tính giả nghịch đảo: A⁺ = V * S⁻¹ * U^T
        A_pinv = Vt_np.T @ S_inv @ U_np.T
        # Nghiệm: x = A⁺ * b
        x = A_pinv @ b_np

        return SolverResult("Phân rã SVD", x.tolist(), r, True, "Dùng giả nghịch đảo SVD")

    except Exception as e:
        return SolverResult("Phân rã SVD", None, 0, False, f"Lỗi: {str(e)}")

# PHẦN 6: HÀM GIẢI BẰNG GAUSS-SEIDEL
def solve_gauss_seidel(A, b):
    try:
        # Gọi hàm Gauss-Seidel
        x, iterations, converged = gauss_seidel(A, b)

        # Nếu không thỏa điều kiện ban đầu
        if x is None:
            return SolverResult(
                "Gauss-Seidel", 
                None, 
                0, 
                False, 
                "Ma trận không chéo trội chặt (Không đảm bảo hội tụ)"
            )

        # Trả kết quả
        return SolverResult(
            "Gauss-Seidel", 
            x, 
            iterations, 
            converged, 
            "Hội tụ thành công" if converged else "Chưa hội tụ hoàn toàn (Đạt max iter)"
        )

    except Exception as e:
        return SolverResult("Gauss-Seidel", None, 0, False, f"Lỗi: {str(e)}")


# PHẦN 7: TỔNG HỢP CÁC PHƯƠNG PHÁP GIẢI
def get_all_solvers():
    # trả về danh sách solver để benchmark gọi
    return [
        solve_gauss,
        solve_svd,
        solve_gauss_seidel
    ]