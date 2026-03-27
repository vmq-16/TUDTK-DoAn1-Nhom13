# HƯỚNG DẪN LÀM VIỆC NHÓM - ĐỒ ÁN 1 TOÁN ỨNG DỤNG (NHÓM 13)

## 📋 MỤC LỤC

1. [Yêu cầu hệ thống](#1-yêu-cầu-hệ-thống)
2. [Thiết lập ban đầu](#2-thiết-lập-ban-đầu)
3. [Cấu trúc thư mục & Quy tắc file](#3-cấu-trúc-thư-mục--quy-tắc-file)
4. [Git Workflow hàng ngày](#4-git-workflow-hàng-ngày)
5. [Quy tắc Cốt lõi](#5-quy-tắc-cốt-lõi)

## 1. YÊU CẦU HỆ THỐNG

Tất cả thành viên cần cài đặt đủ 3 công cụ sau trước khi clone code về máy:

| Phần mềm | Ghi chú quan trọng |
|----------|---------|
| **1. Git** | Tải từ [git-scm.com](https://git-scm.com/downloads). Cài đặt xong thì đăng nhập Github. |
| **2. Python 3.10 trở lên** | Tải từ [python.org](https://www.python.org/downloads/). ⚠️ **BẮT BUỘC TICK VÀO Ô `Add python.exe to PATH`** ở màn hình cài đặt đầu tiên.
| **3. VS Code** | Trình soạn thảo chính. Vào mục Extensions (Ctrl+Shift+X) cài thêm 2 tiện ích: **Python** và **Jupyter** (của Microsoft). |

## 2. THIẾT LẬP BAN ĐẦU

### Bước 2.1: Clone repo về máy
Mở thư mục bạn muốn chứa đồ án, click chuột phải chọn **Open Git Bash here** (hoặc mở Terminal trong VS Code) và chạy lệnh:
```bash
git clone https://github.com/vmq-16/TUDTK-DoAn1-Nhom13.git
cd TUDTK-DoAn1-Nhom13
```

### Bước 2.2: Tạo môi trường ảo (Virtual Environment)
Để các thư viện của đồ án không làm rác máy tính cá nhân, chúng ta dùng `venv`:
```bash
# 1. Tạo môi trường ảo (Lưu ý: Nếu lỗi, hãy thử dùng lệnh `py -m venv venv`)
python -m venv venv

# 2. Kích hoạt môi trường (Dành cho Git Bash trên Windows)
source venv/Scripts/activate
```
> 💡 **Thành công:** Khi bạn thấy chữ `(venv)` xuất hiện ở đầu dòng lệnh Terminal.

### Bước 2.3: Tải thư viện tự động
Đảm bảo đã có chữ `(venv)`, gõ lệnh sau để `pip` tự cài các thư viện trong `requirements.txt`:
```bash
pip install -r requirements.txt
```

> ⚠️ **ĐẶC BIỆT LƯU Ý CHO PHẦN 2 (MANIM):**
> Thư viện `manim` cần bộ giải mã video của Windows. Khuyến khích sử dụng Manim Community phiên bản stable v.20.1. **Chỉ những ai code Phần 2** mới cần mở `Windows PowerShell` lên và chạy lệnh: `winget install Gyan.FFmpeg`, sau đó khởi động lại môi trường lập trình để tiếp tục làm.

## 3. CẤU TRÚC THƯ MỤC & QUY TẮC FILE

> ⚠️ **Quan trọng:** Phải đặt file đúng thư mục để khi chạy đường dẫn không bị lỗi trên máy người khác. Sơ đồ dưới đây bám sát đúng yêu cầu cấu trúc nộp bài của đồ án:

```text
TUDTK-DoAn1-Nhom13/
|-- README.md                  ← Thông tin chung của project
|-- requirements.txt           ← Danh sách thư viện Python
|-- report/                    
|   |-- report.pdf             ← Báo cáo PDF cuối cùng
|   `-- report.tex/md          ← Source code LaTeX hoặc Markdown của báo cáo
|-- part1/                     
|   |-- gaussian.py            ← Code thuật toán khử Gauss
|   |-- determinant.py         ← Code tính định thức
|   |-- inverse.py             ← Code tìm ma trận nghịch đảo
|   |-- rank_basis.py          ← Code tìm hạng và cơ sở
|   `-- part1_demo.ipynb       ← File Jupyter Notebook chạy thử Phần 1
|-- part2/                     
|   |-- decomposition.py       ← Code thuật toán phân rã ma trận
|   |-- diagonalization.py     ← Code chéo hóa ma trận
|   |-- manim_scene.py         ← Code hiệu ứng Manim
|   `-- demo_video.mp4         ← Video xuất ra từ Manim
|-- part3/                     
|   |-- solvers.py             ← Code các phương pháp lặp giải hệ phương trình
|   |-- benchmark.py           ← Code đo lường thời gian và sai số
|   `-- analysis.ipynb         ← File Jupyter Notebook báo cáo Phần 3
|
|-- venv/                      ← Thư viện cục bộ (Git tự động bỏ qua, KHÔNG nộp)
`-- .gitignore                 ← File cấu hình ẩn rác (KHÔNG ĐƯỢC XÓA, KHÔNG nộp)
```

## 4. GIT WORKFLOW HÀNG NGÀY
> ⚠️ Nhánh `main` đã được khóa bảo vệ. **Tuyệt đối không code trực tiếp trên `main`.** Cần theo 5 bước sau mỗi ngày.

### Bước 1 - Lấy code mới nhất về trước khi làm việc
```bash
git checkout main
git pull origin main
```

### Bước 2 - Tạo branch mới để code
```bash
# Ví dụ: Nhận phần code Khử Gauss
git checkout -b part1-khu-gauss
```

### Bước 3 - Code và Chạy thử
Mở VS Code lên code. 
> 🛑 **LUÔN LUÔN** gõ lệnh kích hoạt `source venv/Scripts/activate` trước khi chạy thử bất kỳ file Python nào.

### Bước 4 - Commit và Push lên GitHub
```bash
git add .
git commit -m "Hoàn thành thuật toán tìm ma trận nghịch đảo"
git push -u origin part1-khu-gauss
```

### Bước 5 - Tạo Pull Request (PR) để gộp bài
1. Vào trang GitHub của repo.
2. Bấm nút xanh **Compare & pull request**.
3. Bấm **Create pull request**.
4. Leader sẽ review code và bấm **Merge** để gộp vào `main`.

## 5. QUY TẮC CỐT LÕI

### 🛑 Sử dụng thư viện:
* **KHÔNG ĐƯỢC DÙNG** các hàm có sẵn như `numpy.linalg.solve`, `numpy.linalg.inv`, `scipy.linalg.qr`, `scipy.linalg.lu`, `sympy.linsolve`, hay các phương thức như `echelon_form`, `rref`... để cài đặt thuật toán. 
* Các thư viện NumPy, SciPy, SymPy **CHỈ ĐƯỢC DÙNG ĐỂ KIỂM CHỨNG** kết quả code của bạn có đúng không.

### ❌ Không bao giờ:
- Code trực tiếp trên nhánh `main`.
- Xóa các tệp cấu hình hệ thống như `.gitignore`.
- Đẩy (push) thư mục `venv/`, thư mục chứa video nháp `media/`, `__pycache__/`, `.ipynb_checkpoints/` hoặc các file rác `.pyc` lên mạng (hãy chắc chắn chúng đã nằm trong `.gitignore`).
- Pull code khi file của bạn đang gõ dở dang chưa được commit hay cất đi.

### ✅ Luôn luôn:
- Bật `(venv)` mỗi khi mở VS Code.
- Tạo một branch mới cho từng task vụ nhỏ.
- Test kỹ thuật toán trên máy cá nhân trước khi tạo Pull Request.

---
:v