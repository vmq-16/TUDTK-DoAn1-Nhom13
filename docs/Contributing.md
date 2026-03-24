# HƯỚNG DẪN LÀM VIỆC NHÓM - ĐỒ ÁN 1 TOÁN ỨNG DỤNG (NHÓM 13)

> Tài liệu này mô tả chi tiết từ A-Z cách thiết lập môi trường Python, cấu trúc thư mục và quy trình sử dụng Git để toàn bộ Nhóm 13 làm việc đồng bộ, tránh xung đột code (conflict) và lỗi môi trường.

---

## 📋 MỤC LỤC

1. [Yêu cầu hệ thống](#1-yêu-cầu-hệ-thống)
2. [Thiết lập ban đầu (Làm 1 lần)](#2-thiết-lập-ban-đầu)
3. [Cấu trúc thư mục & Quy tắc file](#3-cấu-trúc-thư-mục--quy-tắc-file)
4. [Git Workflow hàng ngày (Quan trọng)](#4-git-workflow-hàng-ngày)
5. [Xử lý khi có lỗi (Troubleshooting)](#5-xử-lý-khi-có-lỗi-troubleshooting)
6. [Chuẩn mực Commit Message](#6-chuẩn-mực-commit-message)
7. [Quy tắc Sinh Tồn](#7-quy-tắc-sinh-tồn)

---

## 1. YÊU CẦU HỆ THỐNG

Tất cả thành viên cần cài đặt đủ 3 công cụ sau trước khi clone code về máy:

| Phần mềm | Ghi chú quan trọng |
|----------|---------|
| **1. Git** | Tải từ [git-scm.com](https://git-scm.com/downloads). Cứ Next liên tục để cài đặt. Cài xong sẽ có công cụ **Git Bash**. |
| **2. Python 3.x** | Tải từ [python.org](https://www.python.org/downloads/). ⚠️ **BẮT BUỘC TICK VÀO Ô `Add python.exe to PATH`** ở màn hình cài đặt đầu tiên. |
| **3. VS Code** | Trình soạn thảo chính. Vào mục Extensions (Ctrl+Shift+X) cài thêm 2 tiện ích: **Python** và **Jupyter** (của Microsoft). |

---

## 2. THIẾT LẬP BAN ĐẦU

> Chỉ làm **một lần duy nhất** khi mới tải project về máy.

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
> Thư viện `manim` cần bộ giải mã video của Windows. **Chỉ những ai code Phần 2** mới cần mở `Windows PowerShell` lên và chạy lệnh: `winget install Gyan.FFmpeg`, sau đó khởi động lại môi trường lập trình. Người làm phần khác không cần cài.

---

## 3. CẤU TRÚC THƯ MỤC & QUY TẮC FILE

> ⚠️ **Quan trọng:** Phải đặt file đúng thư mục để khi chạy đường dẫn không bị lỗi trên máy người khác.

```text
TUDTK-DoAn1-Nhom13/
├── part1/                     ← Code thuật toán (gaussian.py, determinant.py...)
├── part2/                     ← Code hiệu ứng Manim xuất video
├── part3/                     ← File Jupyter Notebook (.ipynb) đo hiệu năng
├── report/                    ← Báo cáo LaTeX (.tex) và file PDF
├── venv/                      ← Thư viện cục bộ (Git tự động bỏ qua, không đẩy lên)
├── .gitignore                 ← File cấu hình ẩn rác (KHÔNG ĐƯỢC XÓA)
└── requirements.txt           ← Danh sách thư viện Python
```

---

## 4. GIT WORKFLOW HÀNG NGÀY

> ⚠️ Nhánh `main` đã được khóa bảo vệ. **Tuyệt đối không code trực tiếp trên `main`.** Mọi người tuân thủ 5 bước sau mỗi ngày.

### Bước 1 — Lấy code mới nhất về trước khi làm việc
```bash
git checkout main
git pull origin main
```

### Bước 2 — Tạo branch mới để code
```bash
# Ví dụ: Nhận phần code Khử Gauss
git checkout -b part1-khu-gauss
```
**Quy tắc đặt tên nhánh:** `tênphần-chứcnăng` (Ví dụ: `part2-ma-tran`, `report-chuong1`).

### Bước 3 — Code và Chạy thử
Mở VS Code lên code. 
> 🛑 **LUÔN LUÔN** gõ lệnh kích hoạt `source venv/Scripts/activate` trước khi chạy thử bất kỳ file Python nào.

### Bước 4 — Commit và Push lên GitHub
```bash
git add .
git commit -m "Hoàn thành thuật toán tìm ma trận nghịch đảo"
git push -u origin part1-khu-gauss
```

### Bước 5 — Tạo Pull Request (PR) để gộp bài
1. Vào trang GitHub của repo.
2. Bấm nút xanh **Compare & pull request**.
3. Bấm **Create pull request**.
4. Báo cho Leader vào kiểm tra. Leader sẽ review code và bấm **Merge** để gộp vào `main`.

---

## 5. XỬ LÝ KHI CÓ LỖI (TROUBLESHOOTING)

### Lỗi 1: `ModuleNotFoundError: No module named 'numpy'`
* **Nguyên nhân:** Quên kích hoạt hộp đồ nghề.
* **Cách sửa:** Gõ `source venv/Scripts/activate` vào terminal rồi chạy lại file code.

### Lỗi 2: Không thể push vì báo `Updates were rejected`
* **Nguyên nhân:** Có người vừa gộp code mới vào nhánh trên mạng, máy bạn đang bị cũ hơn.
* **Cách sửa:** Kéo code mới về trước khi push.
```bash
git pull origin ten-nhanh-cua-ban
# Nếu có xung đột (conflict), sửa file đỏ -> add -> commit
git push
```

### Lỗi 3: Lỡ cài thêm thư viện mới, làm sao báo cho nhóm?
Nếu phần code của bạn bắt buộc phải dùng thư viện mới (ví dụ: `pip install pandas`), bạn **phải cập nhật hóa đơn**:
```bash
pip freeze > requirements.txt
```
Sau đó commit tệp `requirements.txt` này đẩy lên để anh em khác biết đường tải thêm.

---

## 6. CHUẨN MỰC COMMIT MESSAGE

Commit rõ ràng giúp Leader dễ duyệt bài và dễ tìm lại code cũ khi bug xảy ra.

✅ **Tốt (Khuyên dùng):**
```text
Add: Thuật toán tìm hạng của ma trận (rank_basis.py)
Fix: Lỗi chia cho 0 trong hàm khử Gauss
Update: Tối ưu hóa vòng lặp phần vẽ đồ thị Part 3
Docs: Thêm hướng dẫn setup Manim vào README
```

❌ **Không tốt:**
```text
Xong part 1
Fix bug
Update code mới
Sửa lại xíu
```

---

## 7. QUY TẮC SINH TỒN 🚨

### ❌ KHÔNG BAO GIỜ:
- Code trực tiếp trên nhánh `main`.
- Xóa các tệp cấu hình hệ thống như `.gitignore`.
- Đẩy (push) thư mục `venv/`, thư mục chứa video nháp `media/` hoặc các file rác `.pyc` lên mạng.
- Pull code khi file của bạn đang gõ dở dang chưa được commit hay cất đi (stash).

### ✅ LUÔN LUÔN:
- Bật `(venv)` mỗi khi mở VS Code.
- Tạo một nhánh (branch) mới cho từng task vụ nhỏ.
- Test kỹ thuật toán trên máy cá nhân trước khi tạo Pull Request.

---
Chuc cac ban lam viec hieu qua! 💪