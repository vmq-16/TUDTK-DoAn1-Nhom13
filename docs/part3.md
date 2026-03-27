# PHẦN 3: GIẢI HỆ PHƯƠNG TRÌNH VÀ PHÂN TÍCH HIỆU NĂNG (ĐIỂM CỘNG)

**Mục tiêu:** Cài đặt phương pháp lặp để giải hệ $Ax=b$, sau đó thực nghiệm đo lường thời gian, sai số và phân tích tính ổn định số học so với các phương pháp trực tiếp ở Phần 1 và Phần 2.

## 1. QUY ĐỊNH CHUNG

* ✅ **Tái sử dụng code:** Gọi lại các hàm giải hệ phương trình bằng phép khử Gauss (từ `part1/`) và Phân rã ma trận (từ `part2/`) để làm đối tượng so sánh.
* ✅ **Phương pháp lặp:** Bắt buộc cài đặt ít nhất một phương pháp lặp, khuyến khích dùng **Gauss-Seidel**.
* ✅ **Thư viện:** Dùng `time` hoặc `timeit` để đo thời gian, dùng `matplotlib` để vẽ biểu đồ, dùng `numpy` để sinh ma trận ngẫu nhiên và tính chuẩn sai số.

## 2. CHI TIẾT YÊU CẦU CÁC FILE MÃ NGUỒN

Các file Python chứa logic thuật toán và hàm hỗ trợ được đặt trong `part3/`.

### 2.1. `solvers.py` (Phương pháp giải hệ lặp)
* **Hàm `gauss_seidel_solve(A, b, max_iter, tol)`:**
  * Cài đặt phương pháp lặp Gauss-Seidel dựa trên công thức lặp theo từng thành phần:
    $$x_{i}^{(k+1)}=\frac{1}{a_{ii}}(b_{i}-\sum_{j=1}^{i-1}a_{ij}x_{j}^{(k+1)}-\sum_{j=i+1}^{n}a_{ij}x_{j}^{(k)})$$
  * **Kiểm tra điều kiện hội tụ:** Ma trận $A$ phải là ma trận chéo trội chặt hàng ($|a_{ii}|>\sum_{j\ne i}|a_{ij}|$). Nếu không thỏa mãn, cần in ra cảnh báo trước khi lặp.
  * Dừng lặp khi đạt số lần tối đa `max_iter` hoặc khi độ lệch giữa hai nghiệm liên tiếp nhỏ hơn ngưỡng sai số `tol`.

### 2.2. `benchmark.py` (Công cụ sinh dữ liệu và đo lường)
* Cài đặt các hàm hỗ trợ sinh ma trận cho quá trình test:
  * Sinh ma trận ngẫu nhiên kích thước $n \times n$.
  * Sinh ma trận đối xứng xác định dương (SPD) ngẫu nhiên (dùng cho test well-conditioned).
  * Sinh **Ma trận Hilbert $H_n$** (dùng cho test ill-conditioned) với công thức $H_{i,j}=\frac{1}{i+j-1}$.

## 3. YÊU CẦU BÁO CÁO THỰC NGHIỆM (`analysis.ipynb`)

Đây là nơi nhóm sẽ chạy code, xuất biểu đồ và viết nhận xét phân tích. File Notebook cần chia làm 2 phần chính:

### 3.1. Phân tích Chi phí Tính toán (Hiệu năng)
* **Thực nghiệm:** Khởi tạo các ma trận ngẫu nhiên với kích thước $n\in\{50, 100, 200, 500, 1000\}$.
* **Đo lường:** Giải hệ $Ax=b$ bằng 3 phương pháp. Với mỗi kích thước $n$, chạy trung bình 5 lần và lấy thời gian thực thi trung bình.
* **Trực quan hóa:**
  * Vẽ đồ thị **log-log** trục tung là Thời gian (giây), trục hoành là Kích thước $n$.
  * Bắt buộc vẽ thêm đường thẳng lý thuyết đại diện cho độ phức tạp $O(n^3)$ để làm mốc so sánh.

### 3.2. Phân tích Ổn định Số học (Sai số)
* **Thực nghiệm:** Giải hệ $Ax=b$ trên hai loại ma trận: Ma trận ngẫu nhiên SPD (số điều kiện nhỏ) và Ma trận Hilbert (số điều kiện rất lớn).
* **Đo lường:** Tính sai số tương đối theo công thức: $\frac{||A\hat{x}-b||_{2}}{||b||_{2}}$ với $\hat{x}$ là nghiệm máy tính giải ra.
* **Nhận xét (Quan trọng để lấy điểm tối đa):**
  * So sánh sai số của các phương pháp trên ma trận Hilbert.
  * Trả lời câu hỏi: Phương pháp nào bị "vỡ trận" (sai số cực lớn) khi gặp ma trận có số điều kiện lớn? Tại sao?