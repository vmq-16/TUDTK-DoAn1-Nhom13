from gaussian import gaussian_elimination

def determinant(A):
    # Kiểm tra ma trận rỗng và ma trận vuông
    if not A or len(A) != len(A[0]):
        raise ValueError("Định thức chỉ xác định cho ma trận vuông.")

    # Sử dụng hàm khử Gauss để lấy ma trận tam giác trên U và số lần hoán vị dòng s
    # Truyền b=None để hàm trả về kết quả cho ma trận hệ số đơn thuần
    U, _, s = gaussian_elimination(A, b=None)
    
    n = len(U)
    det = 1.0
    
    # Tính tích các phần tử trên đường chéo chính của ma trận U
    for i in range(n):
        det *= U[i][i]
        
    # Nhân với (-1)^s (s là số lần hoán vị dòng)
    det *= ((-1) ** s)
    
    return round(det, 6)
