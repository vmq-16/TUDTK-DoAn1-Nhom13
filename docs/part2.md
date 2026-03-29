# PHẦN 2: PHÂN RÀ MA TRẬN VÀ TRỰC QUAN HÓA VỚI MANIM

**Mục tiêu:** Cài đặt từ đầu một thuật toán phân rã ma trận, tính toán chéo hóa và dùng thư viện Manim để tạo video trực quan hóa toàn bộ quá trình.

## 1. QUY ĐỊNH CHUNG

* Tương tự Phần 1, tuyệt đối không dùng các hàm có sẵn như `scipy.linalg.qr`, `scipy.linalg.lu`... để phân rã. Chỉ dùng NumPy/SciPy để kiểm chứng.

## 2. CHI TIẾT YÊU CẦU CÁC FILE CODE THUẬT TOÁN

### 2.1. `decomposition.py` (Thuật toán phân rã)
* Cài đặt thuật toán phân rã nhóm đã chọn từ đầu.
* Tùy thuộc vào thuật toán chọn mà input/output sẽ khác nhau. Ví dụ nếu chọn SVD, hàm cần trả về 3 ma trận $U$, $\Sigma$, $V^{T}$.
* Cần viết kèm hàm đối chiếu sai số với kết quả của NumPy/SciPy (dùng `numpy.allclose` với `atol=1e-9` như Phần 1).

### 2.2. `diagonalization.py` (Chéo hóa ma trận)
* **Mục tiêu:** Phân tích ma trận thành dạng $A=P D P^{-1}$.
* Cài đặt thuật toán tìm các giá trị riêng $\lambda_{i}$ để tạo ma trận đường chéo $D$.
* Cài đặt thuật toán tìm các vector riêng độc lập tuyến tính để tạo ma trận $P$.

## 3. YÊU CẦU TRỰC QUAN HÓA MANIM (BẮT BUỘC)

Phần này dùng thư viện Manim Community v.20.1 để xuất video. Yêu cầu kỹ thuật:
* **File code:** `manim_scene.py`.
* **File video xuất ra:** `demo_video.mp4`, độ phân giải tối thiểu 720p (khuyến khích 1080p).
* **Thời lượng:** Từ 2 phút đến tối đa 30 phút.

### Kịch bản Video (tham khảo):
1. **Scene 1: Giới thiệu bài toán.**
   * Hiển thị ma trận $A$ cụ thể bằng số trên màn hình.
   * Nêu rõ bài toán phân rã nhóm chọn thực hiện.
2. **Scene 2: Trực quan hóa quá trình phân rã.**
   * *Nếu LU:* Minh họa từng bước khử Gauss, hình thành $L$ và $U$.
   * *Nếu QR:* Vẽ Gram-Schmidt trong không gian 2D/3D, biểu diễn vector trực giao hóa. 
   * *Nếu SVD:* Trực quan hóa phép biến đổi hình học rotate-scale-rotate (xoay - co giãn - xoay) trên hình tròn đơn vị. 
   * *Nếu Cholesky:* Hiển thị tính chất SPD của $A$, từng bước tính $L$.
3. **Scene 3: Chéo hóa.**
   * Hiển thị các giá trị riêng, vector riêng tìm được.
   * Minh họa phép phân tích $A=PDP^{-1}$.

## 4. LƯU Ý KHI CODE MANIM CHO NHÓM

* Thư viện Manim khá nặng và kén môi trường. Những bạn không phụ trách code Part 2 không cần thiết phải chạy thử file Manim để tránh lỗi máy.
* Render video nháp trong lúc test code: Sử dụng cờ `-ql` (Quality Low) để render nhanh ở độ phân giải thấp (VD: `manim -ql manim_scene.py MyScene`).
* Render video nộp bài (Final): Sử dụng cờ `-qh` (Quality High) để xuất video 1080p, hoặc custom cấu hình để đạt mức 720p theo barem (VD: `manim -qh manim_scene.py MyScene`).
* Không push các thư mục chứa video nháp (`media/`) lên GitHub. Chắc chắn rằng `.gitignore` đã chặn thư mục `media/`.

> **P/s: Tips gõ Tiếng Việt với LaTeX trong Manim:**
> Để các hàm `Tex`, `MathTex` không bị lỗi font khi gõ tiếng Việt, hãy dán đoạn cài đặt toàn cục này lên đầu file code (ngay dưới dòng `from manim import *`):
> ```python
> my_template = TexTemplate()
> my_template.add_to_preamble(r"\usepackage[utf8]{inputenc}")
> my_template.add_to_preamble(r"\usepackage[T5]{fontenc}")
> config.tex_template = my_template 
> ```