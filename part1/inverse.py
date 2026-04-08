from gaussian import epsilon

def calculate_inverse(A):
    n = len(A)
    if n != len(A[0]):
        raise ValueError("Chỉ ma trận vuông mới có ma trận nghịch đảo.")

    # Tạo ma trận đơn vị I
    I = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    
    # Tạo ma trận ghép M = [A | I]
    M = [A[i] + I[i] for i in range(n)]
    
    # 1. Biến đổi về dạng tam giác trên (Khử Gauss)
    for i in range(n):
        # Tìm dòng có phần tử chốt lớn nhất
        pivot = i
        for k in range(i + 1, n):
            if abs(M[k][i]) > abs(M[pivot][i]):
                pivot = k
        
        # Kiểm tra tính khả nghịch: Nếu phần tử chốt xấp xỉ 0 thì det(A) = 0
        if abs(M[pivot][i]) < epsilon:
            print("Ma trận không khả nghịch (định thức bằng 0).")
            return None
        
        # Hoán vị dòng
        M[i], M[pivot] = M[pivot], M[i]
        
        # Chuẩn hóa dòng hiện tại (đưa phần tử chốt về 1)
        pivot_val = M[i][i]
        for j in range(i, 2 * n):
            M[i][j] /= pivot_val
            
        # Loại bỏ các phần tử dưới chốt
        for k in range(i + 1, n):
            factor = M[k][i]
            for j in range(i, 2 * n):
                M[k][j] -= factor * M[i][j]

    # 2. Biến đổi về dạng đơn vị (Khử ngược Jordan)
    for i in range(n - 1, -1, -1):
        for k in range(i - 1, -1, -1):
            factor = M[k][i]
            for j in range(i, 2 * n):
                M[k][j] -= factor * M[i][j]

    # 3. Tách lấy ma trận nghịch đảo A^-1 từ ma trận ghép
    inv_A = [row[n:] for row in M]
    
    # Làm tròn kết quả
    inv_A = [[round(val, 6) for val in row] for row in inv_A]
    
    return inv_A
