# PHẦN 1: IMPORT

import numpy as np  # dùng cho tính toán ma trận (Gauss, SVD)


# PHẦN 2: CHECK DIAGONAL DOMINANCE

def check_strict_diagonal_dominance(matrix):
    nrows = len(matrix)  # số hàng của ma trận

    # duyệt từng hàng
    for row in range(nrows):
        diag = abs(matrix[row][row])  # phần tử trên đường chéo chính

        # tính tổng trị tuyệt đối các phần tử ngoài đường chéo
        off = sum(abs(matrix[row][col]) for col in range(nrows) if col != row)

        # nếu phần tử chéo <= tổng ngoài → không thỏa
        if diag <= off:
            return False

    # tất cả đều thỏa
    return True


# PHẦN 3: GAUSS-SEIDEL

def gauss_seidel(A, b, max_iter=1000, tol=1e-9):

    # kiểm tra điều kiện hội tụ
    if not check_strict_diagonal_dominance(A):
        return None, 0, False

    n = len(A)  # kích thước hệ

    # khởi tạo nghiệm ban đầu x = [0, 0, ..., 0]
    x = [0.0 for _ in range(n)]
    
    # lặp tối đa max_iter lần
    for iteration in range(max_iter):
        x_old = x.copy()  # lưu nghiệm cũ để tính sai số
        
        for i in range(n):

            # tính tổng từ j = 0 → i-1 (dùng giá trị mới x[j])
            sum1 = sum(A[i][j] * x[j] for j in range(i))

            # tính tổng từ j = i+1 → n-1 (dùng giá trị cũ x_old[j])
            sum2 = sum(A[i][j] * x_old[j] for j in range(i+1, n))

            # kiểm tra chia cho 0 (A[i][i] không được bằng 0)
            if abs(A[i][i]) < 1e-12:
                raise ValueError("Zero diagonal element")

            # công thức Gauss-Seidel:
            # x[i] = (b[i] - sum1 - sum2) / A[i][i]
            x[i] = (b[i] - sum1 - sum2) / A[i][i]
        
        # kiểm tra divergence (giá trị bị nổ)
        if any(abs(xi) > 1e50 for xi in x):
            raise ValueError("Divergence detected")

        # tính sai số ||x_new - x_old||
        error = sum((x[i] - x_old[i])**2 for i in range(n)) ** 0.5
        
        # nếu sai số nhỏ hơn ngưỡng → hội tụ
        if error < tol:
            return x, iteration + 1, True
    
    # nếu chạy hết vòng lặp mà chưa hội tụ
    return x, max_iter, False


# PHẦN 4: RESULT CLASS

class SolverResult:
    def __init__(self, method, x, iterations, converged, note=""):
        self.method = method      # tên phương pháp (Gauss, SVD,...)
        self.x = x                # nghiệm tìm được
        self.iterations = iterations  # số lần lặp (nếu có)
        self.converged = converged    # True/False hội tụ
        self.note = note          # ghi chú thêm


# PHẦN 5: LOẠI BỎ GAUSS

def solve_gauss(A, b):
    try:
        # chuyển sang numpy array để tính nhanh hơn
        A = np.array(A, dtype=float)
        b = np.array(b, dtype=float)

        n = len(A)

        # LOẠI BỎ FORWARD
        for i in range(n):

            # tìm dòng có phần tử lớn nhất ở cột i (pivot)
            max_row = np.argmax(abs(A[i:, i])) + i

            # đổi chỗ dòng i với dòng max_row
            A[[i, max_row]] = A[[max_row, i]]
            b[i], b[max_row] = b[max_row], b[i]

            # nếu pivot = 0 → ma trận suy biến
            if abs(A[i][i]) < 1e-12:
                raise ValueError("Singular matrix")

            # khử các phần tử phía dưới
            for j in range(i+1, n):
                factor = A[j][i] / A[i][i]  # hệ số khử

                A[j] -= factor * A[i]  # cập nhật hàng j
                b[j] -= factor * b[i]  # cập nhật vector b

        # THAY THẾ NGƯỢC
        x = np.zeros(n)

        for i in range(n-1, -1, -1):
            # tính x[i] từ dưới lên
            x[i] = (b[i] - np.dot(A[i][i+1:], x[i+1:])) / A[i][i]

        return SolverResult("Gauss", x.tolist(), 0, True)

    except Exception as e:
        return SolverResult("Gauss", None, 0, False, str(e))


# PHẦN 6: SVD SOLVER

def solve_svd(A, b):
    try:
        A = np.array(A, dtype=float)
        b = np.array(b, dtype=float)

        # phân tích A = U * S * V^T
        U, S, Vt = np.linalg.svd(A, full_matrices=False)

        # tạo ma trận nghịch đảo giả của S
        S_inv = np.diag([1/s if s > 1e-12 else 0 for s in S])

        # tính pseudo-inverse: A⁺ = V * S⁻¹ * U^T
        A_pinv = Vt.T @ S_inv @ U.T

        # nghiệm: x = A⁺ * b
        x = A_pinv @ b

        return SolverResult("SVD", x.tolist(), len(S), True)

    except Exception as e:
        return SolverResult("SVD", None, 0, False, str(e))


# PHẦN 7: WRAPPER GAUSS-SEIDEL

def solve_gauss_seidel(A, b):
    try:
        # gọi hàm Gauss-Seidel
        x, iterations, converged = gauss_seidel(A, b)

        # nếu không thỏa điều kiện ban đầu
        if x is None:
            return SolverResult(
                "Gauss-Seidel",
                None,
                0,
                False,
                "Not diagonally dominant"
            )

        # trả kết quả
        return SolverResult(
            "Gauss-Seidel",
            x,
            iterations,
            converged,
            "" if converged else "Did not fully converge"
        )

    except Exception as e:
        return SolverResult("Gauss-Seidel", None, 0, False, str(e))


# PHẦN 8: GET ALL SOLVERS
def get_all_solvers():
    # trả về danh sách solver để benchmark gọi
    return [
        solve_gauss,
        solve_svd,
        solve_gauss_seidel
    ]
