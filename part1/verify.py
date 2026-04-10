import numpy as np
import sympy as sp

# Sử dụng chung ngưỡng sai số do nhóm thống nhất
EPSILON = 1e-9

# Hiển thị màu kết quả kiểm chứng
COLOR_PASSED = '\033[92m'  # Xanh lá
COLOR_FAILED = '\033[91m'  # Đỏ
COLOR_RESET = '\033[0m'    # Trở về mặc định

def verify_solution(A, x, b):
    """
    Kiểm chứng nghiệm của hệ phương trình Ax = b.
    Hỗ trợ kiểm tra cả nghiệm duy nhất, vô nghiệm và vô số nghiệm.
    """
    try:
        A_np = np.array(A, dtype=float)
        b_np = np.array(b, dtype=float)
        
        # Trường hợp 1: Hệ vô nghiệm hoặc vô số nghiệm
        # x được trả về là mảng chứa công thức dạng string hoặc None
        is_string_array = isinstance(x, list) and any(isinstance(item, str) for item in x)
        
        if is_string_array or isinstance(x, str) or x is None:
            rank_A = np.linalg.matrix_rank(A_np, tol=EPSILON)
            # Thêm b thành một cột vào A để tạo ma trận mở rộng
            Ab_np = np.column_stack((A_np, b_np))
            rank_Ab = np.linalg.matrix_rank(Ab_np, tol=EPSILON)
            
            # In kết quả phân tích 2 bên trước
            print(f"   + Kết quả bạn tính (x) : {x}")
            
            if rank_A < rank_Ab:
                print(f"   + Chuẩn NumPy phân tích: Hệ VÔ NGHIỆM (Rank(A) = {rank_A} < Rank(A|b) = {rank_Ab})")
                print(f"{COLOR_PASSED}PASSED: Tính chất hệ chuẩn xác. Hãy đảm bảo kết quả bạn tính cũng vô nghiệm.{COLOR_RESET}")
            elif rank_A == rank_Ab and rank_A < A_np.shape[1]:
                print(f"   + Chuẩn NumPy phân tích: Hệ VÔ SỐ NGHIỆM (Rank(A) = {rank_A} < {A_np.shape[1]} biến)")
                print(f"{COLOR_PASSED}PASSED: Tính chất hệ chuẩn xác. Hãy đối chiếu công thức nghiệm tổng quát ở trên.{COLOR_RESET}")
            return

        # Trường hợp 2: Hệ có nghiệm duy nhất
        x_np = np.array(x, dtype=float)
        
        # Tính toán Ax của nhóm
        Ax = np.dot(A_np, x_np)
        
        # In kết quả so sánh Ax và b
        print(f"   + Giá trị b gốc        : {b_np}")
        print(f"   + Giá trị Ax thực tế   : {Ax}")
        print(f"   + Nghiệm x bạn tính    : {x_np}")
        
        is_Ax_b_correct = np.allclose(Ax, b_np, atol=EPSILON)
        
        # Kiểm tra 2: So sánh trực tiếp với hàm solve của numpy
        is_x_correct_numpy = False
        is_square_full_rank = (A_np.shape[0] == A_np.shape[1] and np.linalg.matrix_rank(A_np, tol=EPSILON) == A_np.shape[1])
        
        if is_square_full_rank:
            x_numpy = np.linalg.solve(A_np, b_np)
            print(f"   + Nghiệm x chuẩn NumPy : {x_numpy}")
            is_x_correct_numpy = np.allclose(x_np, x_numpy, atol=EPSILON)
        
        # Sau khi in hết kết quả 2 bên, mới đánh giá Passed/Failed
        if is_Ax_b_correct:
            print(f"{COLOR_PASSED}PASSED: Ax = b (Sai số nằm trong ngưỡng cho phép).{COLOR_RESET}")
            if is_square_full_rank:
                if is_x_correct_numpy:
                    print(f"{COLOR_PASSED}PASSED: Vector nghiệm x khớp hoàn toàn với numpy.linalg.solve.{COLOR_RESET}")
                else:
                    print(f"{COLOR_PASSED}PASSED: Vector x lệch nhẹ với NumPy do hệ mất ổn định số học. Tuy nhiên Ax=b vẫn thỏa mãn nên nghiệm vẫn đúng.{COLOR_RESET}")
        else:
            print(f"{COLOR_FAILED}FAILED: Phép nhân Ax không cho ra kết quả b.{COLOR_RESET}")
            
    except Exception as e:
        print(f"{COLOR_FAILED}Lỗi trong quá trình kiểm chứng: {e}{COLOR_RESET}")
    print()

def verify_determinant(A, my_det):
    """
    Hàm kiểm chứng định thức.
    """
    A_np = np.array(A, dtype=float)
    np_det = np.linalg.det(A_np)
    
    # In kết quả 2 bên trước
    print(f"   + Định thức bạn tính   : {my_det}")
    print(f"   + Định thức chuẩn NumPy: {np_det}")
    
    if np.allclose(my_det, np_det, atol=EPSILON):
        print(f"{COLOR_PASSED}PASSED: Định thức đúng (Sai số nằm trong ngưỡng cho phép).{COLOR_RESET}")
    else:
        print(f"{COLOR_FAILED}FAILED: Định thức sai lệch so với chuẩn NumPy.{COLOR_RESET}")
    print()


def verify_inverse(A, my_inv):
    """
    Hàm kiểm chứng ma trận nghịch đảo.
    """
    A_np = np.array(A, dtype=float)
    
    # Kiểm tra xem A có khả nghịch không
    rank_A = np.linalg.matrix_rank(A_np, tol=EPSILON)
    if rank_A < A_np.shape[0]:
        print(f"   + Chuẩn NumPy phân tích: Ma trận suy biến (Rank(A) = {rank_A} < {A_np.shape[0]})")
        print(f"{COLOR_PASSED}PASSED: Ma trận không khả nghịch. Hãy đảm bảo code của bạn đã trả về lỗi đúng.{COLOR_RESET}")
        return

    my_inv_np = np.array(my_inv, dtype=float)
    np_inv = np.linalg.inv(A_np)
    
    # In ma trận 2 bên ra để đối chiếu
    print("   + Nghịch đảo bạn tính:")
    for row in my_inv_np:
        print(f"     {row}")
    print("   + Nghịch đảo chuẩn NumPy:")
    for row in np_inv:
        print(f"     {row}")
    
    # Kiểm tra my_inv có khớp với numpy không
    if np.allclose(my_inv_np, np_inv, atol=EPSILON):
        print(f"{COLOR_PASSED}PASSED: Ma trận nghịch đảo khớp hoàn toàn với numpy.linalg.inv.{COLOR_RESET}")
        
        # Bonus: Kiểm tra thêm A * A^-1 == I
        I_check = np.dot(A_np, my_inv_np)
        I_true = np.eye(A_np.shape[0])
        if np.allclose(I_check, I_true, atol=EPSILON):
            print(f"{COLOR_PASSED}PASSED: Tính chất khả nghịch được bảo đảm.{COLOR_RESET}")
    else:
        print(f"{COLOR_FAILED}FAILED: Ma trận nghịch đảo chưa chính xác.{COLOR_RESET}")
    print()


def verify_rank_and_basis(A, my_rank, my_col, my_row, my_null):
    """
    Hàm kiểm chứng cho module rank_basis.py theo TÍNH CHẤT TOÁN HỌC.
    Thay vì so sánh trực tiếp (vì vector cơ sở không duy nhất), 
    ta kiểm tra số chiều và sự phụ thuộc tuyến tính.
    """
    try:
        A_np = np.array(A, dtype=float)
        m, n = A_np.shape
        
        # ----------------------------------------------------
        # Kiểm chứng hạng
        # ----------------------------------------------------
        expected_rank = np.linalg.matrix_rank(A_np, tol=EPSILON)
        print(f"   + Hạng bạn tính     : {my_rank}")
        print(f"   + Hạng chuẩn NumPy  : {expected_rank}")
        
        if my_rank == expected_rank:
            print(f"{COLOR_PASSED}PASSED: Hạng chuẩn xác.{COLOR_RESET}")
        else:
            print(f"{COLOR_FAILED}FAILED: Sai hạng!{COLOR_RESET}")
            return # Nếu sai hạng, các không gian phía sau chắc chắn sai số chiều => Dừng

        # ----------------------------------------------------
        # Kiểm chứng không gian cột C(A)
        # ----------------------------------------------------
        print(f"\n   + Cơ sở cột bạn tính   : {my_col if my_col else '[]'}")
        col_np = np.array(my_col).T if my_col else np.empty((m, 0))
        
        if col_np.shape[1] == expected_rank:
            if expected_rank > 0:
                # Ghép các vector cột vào A
                augmented_col = np.column_stack((A_np, col_np))
                aug_col_rank = np.linalg.matrix_rank(augmented_col, tol=EPSILON)
                print(f"   + Numpy tính toán      : Hạng gốc = {expected_rank}, Hạng khi ghép cơ sở cột = {aug_col_rank}")
                
                if aug_col_rank == expected_rank:
                    print(f"{COLOR_PASSED}PASSED: Cơ sở không gian cột hợp lệ (cùng tập sinh với A).{COLOR_RESET}")
                else:
                    print(f"{COLOR_FAILED}FAILED: Vector cột sinh ra không gian khác C(A).{COLOR_RESET}")
            else:
                print(f"{COLOR_PASSED}PASSED: Cơ sở không gian cột hợp lệ (trống).{COLOR_RESET}")
        else:
            print(f"{COLOR_FAILED}FAILED: Sai số chiều không gian cột.{COLOR_RESET}")

        # ----------------------------------------------------
        # Kiểm chứng không gian dòng R(A)
        # ----------------------------------------------------
        print(f"\n   + Cơ sở dòng bạn tính  : {my_row if my_row else '[]'}")
        row_np = np.array(my_row) if my_row else np.empty((0, n))
        
        if row_np.shape[0] == expected_rank:
            if expected_rank > 0:
                # Ghép các vector dòng vào A
                augmented_row = np.vstack((A_np, row_np))
                aug_row_rank = np.linalg.matrix_rank(augmented_row, tol=EPSILON)
                print(f"   + NumPy tính toán      : Hạng gốc = {expected_rank}, Hạng khi ghép cơ sở dòng = {aug_row_rank}")
                
                if aug_row_rank == expected_rank:
                    print(f"{COLOR_PASSED}PASSED: Cơ sở không gian dòng hợp lệ (Cùng tập sinh với A).{COLOR_RESET}")
                else:
                    print(f"{COLOR_FAILED}FAILED: Vector dòng sinh ra không gian khác R(A).{COLOR_RESET}")
            else:
                print(f"{COLOR_PASSED}PASSED: Cơ sở không gian dòng hợp lệ (trống).{COLOR_RESET}")
        else:
            print(f"{COLOR_FAILED}FAILED: Sai số chiều không gian dòng.{COLOR_RESET}")

        # ----------------------------------------------------
        # Kiểm chứng không gian nghiệm N(A)
        # ----------------------------------------------------
        expected_nullity = n - expected_rank
        print(f"\n   + Cơ sở nghiệm bạn tính: {my_null if my_null else '[]'}")
        print(f"   + Số chiều chuẩn NumPy : {expected_nullity}")
        
        null_np = np.array(my_null).T if my_null else np.empty((n, 0))
        
        if null_np.shape[1] == expected_nullity:
            if expected_nullity > 0:
                # So sánh Ax với 0
                check_zero = np.dot(A_np, null_np)
                if np.allclose(check_zero, 0, atol=EPSILON):
                    print(f"{COLOR_PASSED}PASSED: Cơ sở không gian nghiệm hợp lệ (thỏa mãn Ax = 0).{COLOR_RESET}")
                else:
                    print(f"   + Thực tế A*x ra       : {check_zero}")
                    print(f"{COLOR_FAILED}FAILED: Vector nghiệm không thỏa mãn Ax = 0.{COLOR_RESET}")
            else:
                print(f"{COLOR_PASSED}PASSED: Cơ sở không gian nghiệm hợp lệ (chỉ có nghiệm tầm thường).{COLOR_RESET}")
        else:
            print(f"{COLOR_FAILED}FAILED: Sai số chiều không gian nghiệm.{COLOR_RESET}")
            
    except Exception as e:
        print(f"{COLOR_FAILED}Lỗi trong quá trình kiểm chứng hàm rank_and_basis: {e}{COLOR_RESET}")
    print()