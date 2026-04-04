# PHẦN 1: PHÉP KHỬ GAUSS VÀ ỨNG DỤNG

**Yêu cầu: Thuật toán phải tổng quát hóa cho ma trận kích thước $m\times n$ và xử lý trọn vẹn các trường hợp suy biến.**

## 1. QUY ĐỊNH CHUNG VỀ CÀI ĐẶT

- ❌ **THƯ VIỆN:** Không được sử dụng trực tiếp các hàm có sẵn như `numpy.linalg.solve`, `numpy.linalg.inv`, `scipy.linalg.qr`, `scipy.linalg.lu`, `sympy.linsolve`, hay các phương thức như `echelon_form`, `rref` cho phần cài đặt thuật toán.
- ✅ **KIỂM CHỨNG:** Các thư viện NumPy, SciPy, SymPy chỉ được phép dùng để kiểm chứng kết quả.

## 2. SƠ ĐỒ MODULE VÀ DEPENDENCY

```
                 +---> determinant.py ---+
                 |                       |
gaussian.py -----+---> inverse.py -------+---> part1_demo.ipynb
                 |                       |            ^
                 +---> rank_basis.py ----+            |
                                                      |
verify.py --------------------------------------------+

```

## 3. CHI TIẾT YÊU CẦU CÁC HÀM

Mã nguồn phải bao gồm đúng 6 hàm theo yêu cầu bắt buộc của đồ án.

### 3.1. `gaussian_eliminate(A, b)` và `back_substitution(U, c)` (gaussian.py)

- **Hàm `gaussian_eliminate(A, b)`:** Trả về ma trận sau khi khử, nghiệm $x$, số lần hoán đổi.
- **Hàm `back_substitution(U, c)`:** Dùng để thế ngược, giải hệ tam giác trên $Ux=c$ từ dưới lên. Trả về ma trận kết quả.
- **Xử lý Pivot:**
  - Tại bước khử $k$, tìm $p$ sao cho phần tử chốt lớn nhất.
  - Nếu phần tử chốt $|M_{pk}|=0$: Bắt buộc báo lỗi `"không tồn tại pivot tại cột k (hệ không có nghiệm duy nhất)"`.
  - Nếu phần tử chốt $|M_{pk}|<\epsilon$: Bắt buộc in ra cảnh báo `"pivot gần bằng 0, hệ có thể không ổn định số học"`.
- **Nghiệm tổng quát:** Đối với trường hợp vô số nghiệm, bắt buộc phải đưa ra công thức nghiệm tổng quát. _(Ví dụ: x1 = 2 - 3t1, x2 = t1)_.

### 3.2. `determinant(A)` (Tính định thức, determinant.py)

- Trả về giá trị định thức qua phép khử Gauss.
- Công thức tính cần lưu ý: $det(A)=(-1)^{s}\cdot\prod_{i=1}^{n}u_{ii}$ với $s$ là số lần hoán đổi dòng.

### 3.3. `inverse(A)` (Tìm ma trận nghịch đảo, inverse.py)

- Trả về ma trận nghịch đảo bằng phương pháp Gauss-Jordan.
- Điều kiện: Chỉ áp dụng khi $det(A)\ne0$.
- Thực hiện biến đổi dòng đồng thời trên ma trận ghép $[A|I_{n}]$ cho đến khi đạt dạng $[I_{n}|A^{-1}]$.

### 3.4. `rank_and_basis(A)` (Tìm Hạng và Cơ sở, rank_basis.py)

**Trả về:**

- **Hạng:** số dòng khác 0 trong bậc thang rút gọn.
- **Không gian cột $\mathcal{C}(A)$:** Sinh bởi các cột pivot của ma trận $A$ gốc.
- **Không gian dòng $\mathcal{R}(A)$:** Sinh bởi các dòng khác 0 trong bậc thang dòng rút gọn.
- **Không gian nghiệm $\mathcal{N}(A)$:** Tập nghiệm của hệ $Ax=0$.

### 3.5. `verify_solution(A, x, b)` (Kiểm chứng kết quả, verify.py)

- Cài đặt hàm này để tự động so sánh kết quả tự code với hàm chuẩn của NumPy/SciPy.

## 4. YÊU CẦU KIỂM THỬ (`part1_demo.ipynb`)

Mỗi hàm cần có ít nhất 5 test cases bao gồm các trường hợp đặc biệt (edge cases). Tham khảo các test cases sau:

1. **Ma trận vuông cơ bản:** Nghiệm duy nhất.
2. **Ma trận chữ nhật:** Kích thước $m\ne n$.
3. **Ma trận suy biến:** Vô số nghiệm (có đưa ra công thức tổng quát), vô nghiệm
4. **Cảnh báo Pivot:** Đưa vào ma trận có phần tử trên đường chéo chính rất nhỏ để kích hoạt cảnh báo _ill-conditioned_.
5. **Nghiệm tầm thường:** Hệ phương trình thuần nhất ($b=0$).

## 5. LƯU Ý XỬ LÝ SAI SỐ CHẤM ĐỘNG

Do máy tính lưu trữ số thực luôn tiềm ẩn sai số (ví dụ $0.1+0.2=0.30000000000000004$), nhóm thống nhất sử dụng biến epsilon $\epsilon=1e-9$ làm ngưỡng sai số tuyệt đối.

- Khi so sánh một số thực $x$ với $0$, kiểm tra điều kiện $|x|<\epsilon$ thay vì $x==0$.
- Khi giá trị cực nhỏ (nhỏ hơn $\epsilon$), chủ động gán thẳng giá trị đó về $0.0$ để làm sạch ma trận, tránh rác dữ liệu ở các bước tính toán tiếp theo.
- Để kiểm tra $x==0$, có thề xài `math.isclose(x, 0, abs_tol=1e-9)`.

P/s: có thể dùng `numpy.allclose` với `atol=1e-9` để so sánh 2 số/mảng/ma trận/mảng n chiều.
