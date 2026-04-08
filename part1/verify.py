import numpy as np

# Sử dụng chung ngưỡng sai số do nhóm thống nhất
EPSILON = 1e-9

def verify_solution(A, x, b):
    """
    Kiểm chứng nghiệm của hệ phương trình Ax = b.
    Hỗ trợ kiểm tra cả nghiệm duy nhất, vô nghiệm và vô số nghiệm.
    """
    print("--- Kiểm chứng hàm gaussian_eliminate & back_substitution ---")
    try:
        A_np = np.array(A, dtype=float)
        b_np = np.array(b, dtype=float)
        
        # Trường hợp 1: Hệ vô nghiệm hoặc vô số nghiệm
        # (Giả định x được trả về là chuỗi công thức tổng quát, hoặc None)
        if isinstance(x, str) or x is None:
            rank_A = np.linalg.matrix_rank(A_np)
            # Thêm b thành một cột vào A để tạo ma trận tăng cường
            Ab_np = np.column_stack((A_np, b_np))
            rank_Ab = np.linalg.matrix_rank(Ab_np)
            
            if rank_A < rank_Ab:
                print("Chuẩn NumPy: Hệ VÔ NGHIỆM (Rank A < Rank Ab). Hãy đảm bảo code của bạn cũng báo vô nghiệm.")
            elif rank_A == rank_Ab and rank_A < A_np.shape[1]:
                print(f"Chuẩn NumPy: Hệ VÔ SỐ NGHIỆM (Rank A = {rank_A} < {A_np.shape[1]} biến).")
                print(f"Công thức nghiệm tổng quát bạn tính: {x}")
            return

        # Trường hợp 2: Hệ có nghiệm duy nhất
        x_np = np.array(x, dtype=float)
        
        # Kiểm tra 1: Ax có thực sự bằng b không? (Cách an toàn nhất)
        Ax = np.dot(A_np, x_np)
        is_Ax_b_correct = np.allclose(Ax, b_np, atol=EPSILON)
        
        # Kiểm tra 2: So sánh trực tiếp với hàm solve của numpy (chỉ dùng cho ma trận vuông, khả nghịch)
        is_x_correct_numpy = False
        if A_np.shape[0] == A_np.shape[1] and np.linalg.matrix_rank(A_np) == A_np.shape[1]:
            x_numpy = np.linalg.solve(A_np, b_np)
            is_x_correct_numpy = np.allclose(x_np, x_numpy, atol=EPSILON)
        
        if is_Ax_b_correct:
            print("PASSED: Ax = b (Sai số nằm trong ngưỡng cho phép).")
            if is_x_correct_numpy:
                print("PASSED: Vector nghiệm x khớp hoàn toàn với numpy.linalg.solve.")
        else:
            print("AILED: Phép nhân Ax không cho ra kết quả b.")
            print(f"   + Giá trị b gốc:       {b_np}")
            print(f"   + Giá trị Ax thực tế:  {Ax}")
            
    except Exception as e:
        print(f"Lỗi trong quá trình kiểm chứng: {e}")
    print()


def verify_determinant(A, my_det):
    """
    Hàm kiểm chứng định thức.
    """
    print("--- Kiểm chứng hàm determinant ---")
    A_np = np.array(A, dtype=float)
    np_det = np.linalg.det(A_np)
    
    if np.allclose(my_det, np_det, atol=EPSILON):
        print(f"PASSED: Định thức khớp chuẩn xác. Kết quả: {my_det}")
    else:
        print(f"FAILED: Định thức sai. Tính được: {my_det}, Chuẩn NumPy: {np_det}")
    print()


def verify_inverse(A, my_inv):
    """
    Hàm kiểm chứng ma trận nghịch đảo.
    """
    print("--- Kiểm chứng hàm inverse ---")
    A_np = np.array(A, dtype=float)
    
    # Kiểm tra xem A có khả nghịch không
    if np.linalg.matrix_rank(A_np) < A_np.shape[0]:
        print("NumPy: Ma trận suy biến (không khả nghịch). Hãy đảm bảo code của bạn đã quăng lỗi đúng.")
        return

    my_inv_np = np.array(my_inv, dtype=float)
    np_inv = np.linalg.inv(A_np)
    
    # Kiểm tra my_inv có khớp với numpy không
    if np.allclose(my_inv_np, np_inv, atol=EPSILON):
        print("PASSED: Ma trận nghịch đảo khớp hoàn toàn với numpy.linalg.inv.")
        
        # Bonus: Kiểm tra thêm A * A^-1 == I
        I_check = np.dot(A_np, my_inv_np)
        I_true = np.eye(A_np.shape[0])
        if np.allclose(I_check, I_true, atol=EPSILON):
            print("PASSED: Tính chất A * A^-1 = Ma trận đơn vị (I) được đảm bảo.")
    else:
        print("FAILED: Ma trận nghịch đảo chưa chính xác.")
    print()

def verify_rank_and_basis(A, my_rank, my_col, my_row, my_null):
    """
    Hàm kiểm chứng cho module rank_basis.py.
    Sử dụng SymPy để lấy kết quả toán học chuẩn xác tuyệt đối và so sánh.
    """
    print("--- Kiểm chứng hàm rank_and_basis ---")
    try:
        # 1. Dùng SymPy để tìm kết quả chuẩn
        A_sym = sp.Matrix(A)
        rref_sym, pivot_cols_sym = A_sym.rref()
        
        expected_rank = len(pivot_cols_sym)
        
        # Chuyển đổi kết quả SymPy về NumPy array kiểu float
        expected_col = np.array([A[i] for i in range(len(A))])[:, list(pivot_cols_sym)].T.tolist() if expected_rank > 0 else []
        expected_row = np.array(rref_sym.tolist(), dtype=float)[:expected_rank].tolist()
        expected_null = np.array([vec.tolist() for vec in A_sym.nullspace()], dtype=float).squeeze(axis=2).tolist() if A_sym.nullspace() else []

        # 2. Bắt đầu so sánh
        is_all_passed = True
        
        # Kiểm tra Hạng
        if my_rank != expected_rank:
            print(f"FAILED: Sai hạng! Bạn tính: {my_rank}, Chuẩn SymPy: {expected_rank}")
            is_all_passed = False
            
        # Kiểm tra Không gian Cột
        if my_col or expected_col:
            if not np.allclose(my_col, expected_col, atol=EPSILON):
                print("FAILED: Sai cơ sở Không gian cột!")
                is_all_passed = False
                
        # Kiểm tra Không gian Dòng
        if my_row or expected_row:
            if not np.allclose(my_row, expected_row, atol=EPSILON):
                print("FAILED: Sai cơ sở Không gian dòng!")
                is_all_passed = False
                
        # Kiểm tra Không gian Nghiệm
        if my_null or expected_null:
            if not np.allclose(my_null, expected_null, atol=EPSILON):
                print("FAILED: Sai cơ sở Không gian nghiệm!")
                is_all_passed = False
                
        if is_all_passed:
            print(f"✅ PASSED: Rank = {my_rank}. Các không gian Cột, Dòng và Nghiệm đều khớp hoàn toàn với SymPy/NumPy!")
            
    except Exception as e:
        print(f"Lỗi trong quá trình kiểm chứng rank_and_basis: {e}")
    print()

# ==========================================
# CÁCH SỬ DỤNG TRONG part1_demo.ipynb
# ==========================================
if __name__ == "__main__":
    # Dữ liệu giả lập (Mock data) như thể lấy từ code của các bạn khác
    A_test = [[2, 1, -1], [-3, -1, 2], [-2, 1, 2]]
    b_test = [8, -11, -3]
    
    # Giả sử hàm gaussian_eliminate trả về x = [2.0, 3.0, -1.0]
    x_tinh_duoc = [2.0, 3.0, -1.0] 
    verify_solution(A_test, x_tinh_duoc, b_test)
    
    # Giả sử hàm determinant trả về -1.0
    det_tinh_duoc = -1.0
    verify_determinant(A_test, det_tinh_duoc)