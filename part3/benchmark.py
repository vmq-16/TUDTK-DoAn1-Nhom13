# PHẦN 1: IMPORT THƯ VIỆN

"""
File này dùng để test hiệu năng của các phương pháp giải hệ Ax = b.

Ở đây sẽ:
- đo thời gian chạy của từng phương pháp
- kiểm tra độ chính xác của nghiệm
- so sánh giữa các cách giải

Lưu ý:
    File này không cài đặt thuật toán,
    chỉ gọi lại các hàm đã viết ở solvers.py.
"""

import time
import os
import json
import numpy as np
import copy

from solvers import get_all_solvers

# để có thể tái sử dụng kqua (giữ nguyên khi chạy lại)
np.random.seed(42)

# PHẦN 2: SINH DỮ LIỆU THỬ NGHIỆM

"""
Sinh dữ liệu để kiểm thử và đánh giá hiệu năng của các thuật toán.

--> Sử dụng 3 loại ma trận với các đặc tính khác nhau:

1. diagonally_dominant (Ma trận chéo trội):
   - Khái niệm: Ma trận có trị tuyệt đối của phần tử trên đường chéo chính luôn lớn hơn tổng trị tuyệt đối của các phần tử còn lại trong cùng một hàng.
   - Tác dụng: Dạng ma trận lý tưởng cho các phương pháp lặp. Dùng để chứng minh tốc độ hội tụ tức thời và hiệu năng tính toán vượt trội của thuật toán Gauss-Seidel so với các phương pháp giải trực tiếp.

2. spd (Ma trận đối xứng xác định dương):
   - Khái niệm: Ma trận có tính đối xứng và mọi giá trị riêng đều dương, có cấu trúc rất tốt nhưng không bắt buộc phải thỏa mãn điều kiện chéo trội chặt.
   - Tác dụng: Dùng để kiểm thử tính ổn định và độ chính xác của phương pháp Khử Gauss cùng Phân rã SVD. Đồng thời, nó giúp minh họa giới hạn của Gauss-Seidel (có thể không hội tụ) khi dữ liệu đầu vào thiếu đi tính chéo trội.

3. hilbert (Ma trận Hilbert):
   - Khái niệm: Ma trận gây mất ổn định số học, có số điều kiện tăng theo hàm mũ, khiến hệ phương trình rơi vào trạng thái gần suy biến.
   - Tác dụng: Dùng để ép các thuật toán đến giới hạn, qua đó quan sát và đánh giá mức độ nhạy cảm về sai số của chúng.

* Ghi chú: Vector b được khởi tạo ngẫu nhiên để phục vụ việc giải hệ Ax = b.
"""

# Tạo ma trận chéo trội
def generate_diagonally_dominant_matrix(n):
    # Sinh ma trận n x n với giá trị ngẫu nhiên
    A = np.random.uniform(-1, 1, (n, n))

    # Ép phần tử trên đường chéo chính phải lớn hơn tổng các phần tử khác
    for i in range(n):
        row_sum = sum(abs(A[i][j]) for j in range(n) if j != i)
        A[i][i] = row_sum + np.random.uniform(1, 5) # Đảm bảo chéo trội chặt
        
    return A.tolist()


def generate_spd_matrix(n):
    # Bước 1: tạo ma trận ngẫu nhiên B
    B = np.random.rand(n, n)

    # Bước 2: nhân B^T * B để tạo ma trận đối xứng
    # đảm bảo luôn >= 0
    A = B.T @ B

    # Bước 3: cộng thêm I để đảm bảo xác định dương (tránh singular)
    A = A + np.eye(n)

    # Bước 4: chuyển về list
    return A.tolist()


def generate_hilbert_matrix(n):
    # Bước 1: tạo ma trận Hilbert theo công thức H[i][j] = 1/(i+j+1)
    H = [[1.0 / (i + j + 1) for j in range(n)] for i in range(n)]

    # Bước 2: trả về trực tiếp (đã là list)
    return H

def generate_rhs(n):
    # Bước 1: sinh vector b ngẫu nhiên trong khoảng [-10, 10]
    b = np.random.uniform(-10, 10, n)

    # Bước 2: chuyển về list
    return b.tolist()

# PHẦN 3: HÀM TÍNH SAI SỐ

"""
Hàm tính sai số tương đối của nghiệm.

Ý tưởng:
    Nếu x là nghiệm tìm được thì kiểm tra Ax có gần b không.

Sai số càng nhỏ -> nghiệm càng chính xác.
"""

def compute_relative_error(A, x, b):
    # Bước 1: chuyển về numpy để dễ tính toán
    A = np.array(A, dtype=float)
    x = np.array(x, dtype=float)
    b = np.array(b, dtype=float)

    # Bước 2: tính vector dư r = Ax - b
    residual = A @ x - b

    # Bước 3: tính chuẩn của b
    norm_b = np.linalg.norm(b)

    # Bước 4: tránh chia cho 0
    if norm_b < 1e-9:
        return None

    # Bước 5: trả về sai số tương đối
    err = float(np.linalg.norm(residual) / norm_b)
    
    # Nếu numpy tính ra kết quả là inf hoặc NaN do tràn số, cũng ép về None
    if np.isinf(err) or np.isnan(err):
        return None
        
    return err

# PHẦN 4: BENCHMARK MỘT SOLVER

"""
Hàm này chạy một solver nhiều lần.

Lý do:
    thời gian chạy có thể dao động,
    nên cần lấy trung bình cho ổn định.

Ngoài ra:
    chỉ tính sai số nếu solver hội tụ.
"""

def benchmark_solver(solver_func, A, b, repeat=None):

    # Bước 1: chọn số lần chạy
    if repeat is None:
        repeat = 3 if len(A) > 200 else 5

    times = []
    errors = []
    converged_list = []

    method_name = None
    iterations = None
    note = ""

    # Bước 2: chạy nhiều lần
    for _ in range(repeat):

        # Copy độc lập để giải để tránh bị mất dữ liệu
        A_test = copy.deepcopy(A)
        b_test = copy.deepcopy(b)

        try:
            # đo thời gian bắt đầu
            start = time.perf_counter()

            # gọi solver
            result = solver_func(A_test, b_test)

            # đo thời gian kết thúc
            end = time.perf_counter()

            # lưu thời gian
            times.append(end - start)

            # lưu thông tin
            method_name = result.method
            iterations = result.iterations
            note = result.note

            # lưu trạng thái hội tụ
            converged_list.append(result.converged)

            # chỉ tính error nếu hội tụ
            if result.x and result.converged:
                err = compute_relative_error(A, result.x, b)
                errors.append(err)

        except Exception as e:
            print(f"Lỗi solver: {e}")

    # Bước 3: tính trung bình
    avg_time = sum(times) / len(times) if times else None
    avg_error = sum(errors) / len(errors) if errors else None

    # Bước 4: quyết định hội tụ theo majority
    converged = sum(converged_list) > len(converged_list) / 2

    # Bước 5: trả kết quả
    return {
        "method": method_name or "Unknown",
        "avg_time": avg_time,
        "avg_error": avg_error,
        "iterations": iterations,
        "converged": converged,
        "note": note
    }

# PHẦN 5: BENCHMARK TOÀN DIỆN

"""
Chạy toàn bộ benchmark.

Với mỗi kích thước ma trận và mỗi loại dữ liệu,
sẽ chạy tất cả các solver để so sánh.
"""

def run_benchmark():

    # Bước 1: định nghĩa các kích thước
    sizes = [50, 100, 200, 500, 1000]

    # Bước 2: định nghĩa các loại ma trận
    matrix_types = [
        ("diagonally_dominant", generate_diagonally_dominant_matrix),
        ("spd", generate_spd_matrix),
        ("hilbert", generate_hilbert_matrix),
    ]

    # Bước 3: lấy danh sách solver
    solvers = get_all_solvers()

    results = []

    total_cases = len(sizes) * len(matrix_types)
    case_id = 0

    # Bước 4: duyệt từng trường hợp
    for n in sizes:
        for name, generator in matrix_types:

            case_id += 1
            print(f"\n[{case_id}/{total_cases}] n = {n}, type = {name}")

            # sinh dữ liệu
            A = generator(n)
            b = generate_rhs(n)

            # Bước 5: chạy từng solver
            for solver in solvers:

                res = benchmark_solver(solver, A, b)

                # thêm metadata
                res["n"] = n
                res["matrix_type"] = name

                results.append(res)

                # Xử lý an toàn cho việc in ra màn hình terminal
                err_val = res['avg_error']
                err_str = f"{err_val:.2e}" if err_val is not None else "inf"
                
                time_val = res['avg_time']
                time_str = f"{time_val:.4f}s" if time_val is not None else "inf"

                print(f"  {res['method']:<15} | time = {time_str} | error = {err_str}")

    # Bước 6: trả kết quả
    return results

# PHẦN 6: LƯU KẾT QUẢ 
def save_to_json(data, filename="benchmark_results.json"):
    # Tạo đường dẫn part3/benchmark_results.json
    folder = "part3"
    os.makedirs(folder, exist_ok=True) # Tạo thư mục nếu chưa tồn tại
    filepath = os.path.join(folder, filename)

    # Mở file
    with open(filepath, "w", encoding="utf-8") as f:
        # Ghi dữ liệu JSON
        json.dump(results, f, indent=4, ensure_ascii=False)
    # Thông báo
    print(f"\nĐã lưu vào {filepath}")
    
def save_to_txt(data, filename="benchmark.txt"):
    # Tạo đường dẫn part3/benchmark.txt
    folder = "part3"
    os.makedirs(folder, exist_ok=True) # Tạo thư mục nếu chưa tồn tại
    filepath = os.path.join(folder, filename)

    # Mở file
    with open(filepath, "w", encoding="utf-8") as f:

        # Ghi từng dòng
        for item in data:
            # Xử lý an toàn cho Error
            err_val = item['avg_error']
            err_str = f"{err_val:.2e}" if err_val is not None else "inf"

            # Xử lý an toàn cho Time
            time_val = item['avg_time']
            time_str = f"{time_val:.4f}s" if time_val is not None else "inf"
            
            f.write(
                f"n={item['n']}, loại={item['matrix_type']}, "
                f"thuật toán={item['method']}, thời gian={time_str}, "
                f"sai số={err_str}\n"
            )

    # Thông báo
    print(f"Đã lưu vào {filepath}")

# PHẦN 7: MAIN
if __name__ == "__main__":

    # Bước 1: in tiêu đề
    print("=" * 60)
    print("BENCHMARK GIẢI HỆ PHƯƠNG TRÌNH TUYẾN TÍNH")
    print("=" * 60)

    # Bước 2: chạy benchmark
    results = run_benchmark()

    # Bước 3: lưu kết quả
    save_to_json(results)
    save_to_txt(results)  