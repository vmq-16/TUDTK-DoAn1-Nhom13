# PHẦN 1: PHÉP KHỬ GAUSS VÀ ỨNG DỤNG

**Yêu cầu: Thuật toán phải tổng quát hóa cho ma trận kích thước $m\times n$ và xử lý trọn vẹn các trường hợp suy biến.**

## 1. QUY ĐỊNH CHUNG VỀ CÀI ĐẶT

* ❌ **THƯ VIỆN:** Không được sử dụng trực tiếp các hàm có sẵn như `numpy.linalg.solve`, `numpy.linalg.inv`, `scipy.linalg.qr`, `scipy.linalg.lu`, `sympy.linsolve`, hay các phương thức như `echelon_form`, `rref` cho phần cài đặt thuật toán. 
* ✅ **KIỂM CHỨNG:** Các thư viện NumPy, SciPy, SymPy chỉ được phép dùng để kiểm chứng kết quả.
* ⚠️ **CÀI ĐẶT TỪ ĐẦU:** Sinh viên phải cài đặt từ đầu (không dùng NumPy/SciPy/SymPy) các hàm thuật toán. Nên sử dụng kiểu dữ liệu mảng cơ bản của Python (List of Lists) cho logic cốt lõi.
* ⚠️ **TRỤ XOAY BÁN PHẦN (PARTIAL PIVOTING):** Bắt buộc áp dụng để đảm bảo tính ổn định số học.

## 2. CHI TIẾT YÊU CẦU CÁC HÀM

Mã nguồn phải bao gồm đúng 6 hàm theo yêu cầu bắt buộc của đồ án.

### 2.1. `gaussian_eliminate(A, b)` và `back_substitution(U, c)`
* **Hàm `gaussian_eliminate(A, b)`:** Trả về ma trận sau khi khử, nghiệm $x$, số lần hoán đổi dòng.
* **Hàm `back_substitution(U, c)`:** Dùng để thế ngược, giải hệ tam giác trên $Ux=c$ từ dưới lên.
* **Xử lý Pivot:**
  * Tại bước khử $k$, tìm $p$ sao cho phần tử chốt lớn nhất.
  * Nếu phần tử chốt $|M_{pk}|=0$: Bắt buộc báo lỗi `"không tồn tại pivot tại cột k (hệ không có nghiệm duy nhất)"`.
  * Nếu phần tử chốt $|M_{pk}|<\epsilon$: Bắt buộc in ra cảnh báo `"pivot gần bằng 0, hệ có thể không ổn định số học"`. 
* **Nghiệm tổng quát:** Đối với trường hợp vô số nghiệm, sinh viên bắt buộc phải đưa ra công thức nghiệm tổng quát. *(Ví dụ: x1 = 2 - 3t1, x2 = t1)*.

### 2.2. `determinant(A)` (Tính định thức)
* Tính định thức qua phép khử Gauss.
* Công thức tính cần lưu ý: $det(A)=(-1)^{s}\cdot\prod_{i=1}^{n}u_{ii}$ với $s$ là số lần hoán đổi dòng. 
* Trả về đúng dấu và giá trị định thức.

### 2.3. `inverse(A)` (Tìm ma trận nghịch đảo)
* Tính ma trận nghịch đảo bằng phương pháp Gauss-Jordan.
* Điều kiện: Chỉ áp dụng khi $det(A)\ne0$.
* Thực hiện biến đổi dòng đồng thời trên ma trận ghép $[A|I_{n}]$ cho đến khi đạt dạng $[I_{n}|A^{-1}]$.
* Cần có bước kiểm thử $AA^{-1}=I$.

### 2.4. `rank_and_basis(A)` (Tìm Hạng và Cơ sở)
* Tính hạng của ma trận và tìm cơ sở của các không gian.
* **Không gian cột $\mathcal{C}(A)$:** Sinh bởi các cột pivot của ma trận $A$ gốc.
* **Không gian dòng $\mathcal{R}(A)$:** Sinh bởi các dòng khác 0 trong dạng bậc thang dòng rút gọn (RREF).
* **Không gian nghiệm $\mathcal{N}(A)$:** Tập nghiệm của hệ $Ax=0$.

### 2.5. `verify_solution(A, x, b)` (Kiểm chứng kết quả)
* Cài đặt hàm này để tự động so sánh kết quả tự code với hàm chuẩn của NumPy/SciPy.

## 3. LƯU Ý XỬ LÝ SAI SỐ CHẤM ĐỘNG

Do máy tính lưu trữ số thực luôn tiềm ẩn sai số (ví dụ $0.1+0.2=0.30000000000000004$), nhóm thống nhất sử dụng biến epsilon $\epsilon=1e-9$ làm ngưỡng sai số tuyệt đối.

* Khi so sánh một số thực $x$ với $0$, kiểm tra điều kiện $|x|<\epsilon$ thay vì $x==0$.
* Khi giá trị cực nhỏ (nhỏ hơn $\epsilon$), chủ động gán thẳng giá trị đó về $0.0$ để làm sạch ma trận, tránh rác dữ liệu ở các bước tính toán tiếp theo.
* Để kiểm tra $x==0$, có thề xài `abs(x) < 1e-9` hoặc `math.isclose(x, 0)`.

## 4. YÊU CẦU KIỂM THỬ (`part1_demo.ipynb`)

Mỗi hàm cần có ít nhất 5 test cases bao gồm các trường hợp đặc biệt (edge cases). Thiết kế các kịch bản sau:

1. **Hệ nghiệm duy nhất:** Ma trận vuông cơ bản.
2. **Ma trận chữ nhật:** Kích thước $m\ne n$.
3. **Cảnh báo Pivot:** Đưa vào ma trận có phần tử trên đường chéo chính rất nhỏ để kích hoạt cảnh báo *ill-conditioned*.
4. **Hệ không nghiệm duy nhất:** Ma trận không tồn tại pivot tại một cột, code phải in ra được công thức nghiệm tổng quát.
5. **Nghiệm tầm thường:** Hệ phương trình thuần nhất ($b=0$).

P/s: Trong kiểm thử, có thể dùng `numpy.allclose` với `atol=1e-9` để so sánh 2 số/mảng/ma trận/mảng n chiều.