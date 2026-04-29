# Đồ Án 1: Ma Trận và Cơ Sở của Tính Toán Khoa Học - Nhóm 13

Repository này chứa mã nguồn và tài liệu cho Đồ án 1 môn Toán ứng dụng thống kê, tập trung vào việc triển khai các thuật toán đại số tuyến tính, phân rã ma trận và đánh giá hiệu năng thực tế.

## 1. Cấu trúc nội dung
Đồ án được chia thành 3 phần trọng tâm:
* **`part1`**: Triển khai các thuật toán nền tảng: Khử Gauss, tính định thức, tìm ma trận nghịch đảo, xác định hạng (rank) và tìm cơ sở (basis).
* **`part2`**: Chéo hóa ma trận, phân rã giá trị đơn lẻ (SVD) và trực quan hóa hình học thông qua thư viện Manim.
* **`part3`**: Phân tích thực nghiệm, so sánh hiệu năng và độ ổn định số học giữa các phương pháp trực tiếp (Khử Gauss, SVD) và phương pháp lặp (Gauss-Seidel) trên các hệ phương trình đặc thù.

## 2. Yêu cầu hệ thống
* **Python**: `>= 3.10` (Khuyến khích sử dụng bản 3.12+).
* **Quản lý thư viện**: `pip`.
* **Công cụ hỗ trợ**: Jupyter Notebook hoặc VS Code (cài đặt Python/Jupyter extensions).
* **Yêu cầu riêng cho Manim (`part2`)**: Cần cài đặt `FFmpeg`, `MiKTeX` (cho LaTeX) và `Ghostscript`.

## 3. Cài đặt môi trường
Thực hiện các lệnh sau để thiết lập môi trường làm việc:

```bash
git clone https://github.com/vmq-16/TUDTK-DoAn1-Nhom13.git
cd TUDTK-DoAn1-Nhom13
python -m venv venv
```

**Kích hoạt môi trường và cài đặt thư viện:**
* Windows (Git Bash): `source venv/Scripts/activate`
* macOS / Linux: `source venv/bin/activate`
* Cài đặt: `pip install -r requirements.txt`

---

## 4. Hướng dẫn sử dụng

### Phần 1: Giải thuật Đại số Tuyến tính cơ bản
**Cách 1: Chạy file Demo (Khuyên dùng)**
```bash
jupyter notebook part1/part1_demo.ipynb
```

**Cách 2: Sử dụng như mã nguồn thư viện**
Vì các file trong `part1` được viết dưới dạng module, bạn có thể kiểm tra nhanh như sau:
```python
from part1.gaussian import gaussian_elimination
from part1.determinant import determinant
from part1.inverse import inverse
from part1.rank_basis import rank_and_basis

A = [[2, 1, -1],
     [-3, -1, 2],
     [-2, 1, 2]]
b = [8, -11, -3]


print(f"Nghiệm của hệ (Khử Gauss): {gaussian_elimination(A, b)}")

print(f"Định thức: {determinant(A)}")
print(f"Ma trận nghịch đảo:\n{inverse(A)}")
print(f"Hạng và cơ sở: {rank_and_basis(A)}")
```

### Phần 2: Phân rã Ma trận & Minh họa Hình học
* **Phân rã SVD & Chéo hóa:** Chạy các script `decomposition.py` hoặc `diagonalization.py`.
* **Render mô phỏng Manim:**
    ```bash
    manim -pqh part2/manim_scene.py SVDScene
    ```

### Phần 3: Phân tích Hiệu năng & Sai số
Đây là phần đánh giá chuyên sâu về tốc độ xử lý và độ ổn định trên 3 loại ma trận: **Chéo trội, SPD, và Hilbert**. Toàn bộ kết quả thống kê và biểu đồ phân tích được trình bày tại:
```bash
jupyter notebook part3/analysis.ipynb
```

---

## 5. Cấu trúc thư mục chi tiết
```text
TUDTK-DoAn1-Nhom13/
├── README.md
├── requirements.txt
├── part1/                     # Các thuật toán cơ bản
│   ├── gaussian.py
│   ├── determinant.py
│   ├── inverse.py
│   ├── rank_basis.py
|   ├── verify.py
│   └── part1_demo.ipynb       # Kiểm chứng kết quả
├── part2/                     # Phân rã, chéo hóa ma trận và manim
│   ├── decomposition.py
│   ├── diagonalization.py
│   └── manim_scene.py
└── part3/                     # Đánh giá thực nghiệm
    ├── analysis.ipynb         # Báo cáo thực nghiệm
    ├── solvers.py
    ├── benchmark.py
    ├── benchmark.txt
    └── benchmark_results.json           # Dữ liệu thống kê cấu trúc
```

## 6. Các lỗi thường gặp
1.  **ModuleNotFoundError**: Quên chưa kích hoạt môi trường ảo (`venv`) hoặc chưa chạy `pip install`.
2.  **Manim Error**: Thiếu `ffmpeg` trong biến môi trường (Environment Variables) hoặc thiếu file ảnh trong thư mục `assets/`.
3.  **LaTeX Error**: Nếu không cài `MiKTeX`, hãy cấu hình Manim để sử dụng text thông thường thay vì LaTeX.