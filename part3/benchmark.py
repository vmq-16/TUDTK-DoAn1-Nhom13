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
import json
import numpy as np

from solvers import get_all_solvers

# để có thể tái sử dụng kqua (giữ nguyên khi chạy lại)
np.random.seed(42)

# PHẦN 2: SINH DỮ LIỆU THỬ NGHIỆM

"""
Sinh dữ liệu để test.

-->Dùng 4 loại ma trận:

- random: trường hợp bình thường
- SPD: ma trận đối xứng xác định dương (dễ hội tụ)
- near-singular: gần suy biến (để test độ ổn định)

Vector b được tạo ngẫu nhiên cho đơn giản.
"""

def generate_random_matrix(n):
    # Bước 1: sinh ma trận n x n với giá trị ngẫu nhiên trong [-1, 1]
    # dùng uniform để phân bố đều
    A = np.random.uniform(-1, 1, (n, n))

    # Bước 2: chuyển về dạng list để tương thích với solver
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


def generate_near_singular_matrix(n):
    # Bước 1: tạo ma trận ngẫu nhiên
    A = np.random.rand(n, n)

    # Bước 2: làm cho 2 hàng gần phụ thuộc tuyến tính
    # → ma trận gần suy biến
    A[0] = A[1] * (1 - 1e-6)

    # Bước 3: chuyển về list
    return A.tolist()


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
    if norm_b < 1e-12:
        return float("inf")

    # Bước 5: trả về sai số tương đối
    return float(np.linalg.norm(residual) / norm_b)
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

        try:
            # đo thời gian bắt đầu
            start = time.perf_counter()

            # gọi solver
            result = solver_func(A, b)

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
    avg_time = sum(times) / len(times) if times else float("inf")
    avg_error = sum(errors) / len(errors) if errors else float("inf")

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
    sizes = [50, 100, 200, 500] # Tạm bỏ giá trị 1000 vì chạy lâu quá! #1000

    # Bước 2: định nghĩa các loại ma trận
    matrix_types = [
        ("random", generate_random_matrix),
        ("spd", generate_spd_matrix),
        ("hilbert", generate_hilbert_matrix),
        ("near_singular", generate_near_singular_matrix),
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
            print(f"\n[{case_id}/{total_cases}] n={n}, type={name}")

            # sinh dữ liệu
            A = generator(n)
            b = generate_rhs(n)

            # Bước 5: chạy từng solver
            for solver in solvers:

                # tránh SVD quá chậm với n lớn
                if solver.__name__ == "solve_svd" and n >= 1000:
                    print("  SVD skipped (n too large)")
                    continue

                res = benchmark_solver(solver, A, b)

                # thêm metadata
                res["n"] = n
                res["matrix_type"] = name

                results.append(res)

                method = res["method"]

                print(
                    f"  {method:15} | "
                    f"time = {res['avg_time']:.4f}s | "
                    f"error = {res['avg_error']:.2e}"
                )

    # Bước 6: trả kết quả
    return results

# PHẦN 6: LƯU KẾT QUẢ

def save_to_json(data, filename="benchmark_results.json"):

    # Bước 1: mở file
    with open(filename, "w") as f:

        # Bước 2: ghi dữ liệu JSON
        json.dump(data, f, indent=2)

    # Bước 3: thông báo
    print(f"\nĐã lưu vào {filename}")
    
def save_to_txt(data, filename="benchmark.txt"):

    # Bước 1: mở file
    with open(filename, "w") as f:

        # Bước 2: ghi từng dòng
        for item in data:
            f.write(
                f"n={item['n']}, type={item['matrix_type']}, "
                f"{item['method']} | "
                f"time={item['avg_time']:.4f}s | "
                f"error={item['avg_error']:.2e}\n"
            )

    # Bước 3: thông báo
    print(f"Đã lưu {filename}")

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
