# Đồ Án 1: Toán Ứng Dụng - Nhóm 13

Repository này chứa mã nguồn và tài liệu cho Đồ án 1 môn Toán ứng dụng, bao gồm các thuật toán đại số tuyến tính cơ bản, phân rã ma trận và minh họa trực quan.

## 1. Cấu trúc nội dung
Dự án được chia thành 3 phần chính:
* **`part1`**: Khử Gauss, tính định thức, tìm ma trận nghịch đảo, tính hạng (rank) và tìm cơ sở (basis).
* **`part2`**: Chéo hóa ma trận, phân rã giá trị đơn lẻ (SVD) và mô phỏng hình học bằng thư viện Manim.
* **`part3`**: Phân tích và so sánh các phương pháp lặp (Jacobi, Gauss-Seidel...).

## 2. Yêu cầu hệ thống
* **Python**: `>= 3.10` (Khuyến khích sử dụng bản 3.12+).
* **Quản lý thư viện**: `pip` (đi kèm với Python).
* **Công cụ hỗ trợ**: Jupyter Notebook hoặc VS Code (cài thêm Python/Jupyter extensions).
* **Yêu cầu riêng cho Manim (`part2`)**:
    * `FFmpeg` (Xử lý video).
    * `MiKTeX` (Nếu cần render công thức bằng LaTeX).
    * `Ghostscript`.

## 3. Cài đặt môi trường
Mở terminal và thực hiện các lệnh sau để tải mã nguồn và thiết lập môi trường ảo:

```bash
git clone https://github.com/vmq-16/TUDTK-DoAn1-Nhom13.git
cd TUDTK-DoAn1-Nhom13
```

### Windows (PowerShell)
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Windows (Git Bash)
```bash
python -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt
```

### macOS / Linux
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## 4. Hướng dẫn sử dụng

### Phần 1: Giải hệ phương trình, Định thức, Nghịch đảo, Hạng & Cơ sở
**Cách 1: Chạy file Demo (Khuyên dùng)**
```bash
jupyter notebook part1/part1_demo.ipynb
```

**Cách 2: Gọi trực tiếp hàm trong Python Shell**
Vì các file trong `part1` được viết dưới dạng module, bạn có thể kiểm tra nhanh như sau:
```python
from part1.determinant import determinant
from part1.inverse import inverse
from part1.rank_basis import rank_and_basis

A = [[2, 1], [1, 3]]
print(f"Định thức: {determinant(A)}")
print(f"Nghịch đảo: {inverse(A)}")
print(f"Hạng và cơ sở: {rank_and_basis(A)}")
```

### Phần 2: Chéo hóa, SVD và Manim
* **Chạy script chéo hóa:** `python part2/diagonalization.py`
* **Chạy script phân rã SVD:** `python part2/decomposition.py`
* **Render video mô phỏng (Manim):**
    ```bash
    manim -pqh part2/manim_scene.py SVDScene
    ```
    *Ghi chú:* `-pqh` dùng để render chất lượng cao và tự động mở video sau khi xong. Cần đảm bảo thư mục `assets/` có đầy đủ các file ảnh (như `Kazuha.jpg`) để phần nén ảnh hoạt động đúng.

### Phần 3: Các phương pháp lặp
Hiện tại phần này tập trung vào việc phân tích hiệu năng và độ hội tụ:
```bash
jupyter notebook part3/analysis.ipynb
```

---

## 5. Cấu trúc thư mục chi tiết
```text
TUDTK-DoAn1-Nhom13/
├── README.md
├── requirements.txt
├── docs/
│   └── Contributing.md        # Quy tắc đóng góp và làm việc nhóm
├── part1/                     # Các thuật toán cơ bản
│   ├── gaussian.py
│   ├── determinant.py
│   ├── inverse.py
│   ├── rank_basis.py
│   ├── verify.py              # File kiểm chứng kết quả
│   └── part1_demo.ipynb
├── part2/                     # Phân rã ma trận & Manim
│   ├── decomposition.py
│   ├── diagonalization.py
│   └── manim_scene.py
└── part3/                     # Phương pháp lặp
    ├── analysis.ipynb
    ├── benchmark.py
    └── solvers.py
```

## 6. Các lỗi thường gặp
1.  **ModuleNotFoundError**: Quên chưa kích hoạt môi trường ảo (`venv`) hoặc chưa chạy `pip install`.
2.  **Manim Error**: Thiếu `ffmpeg` trong biến môi trường (Environment Variables) hoặc thiếu file ảnh trong thư mục `assets/`.
3.  **LaTeX Error**: Nếu không cài `MiKTeX`, hãy cấu hình Manim để sử dụng text thông thường thay vì LaTeX.
