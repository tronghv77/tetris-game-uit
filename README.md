# 🧱 Tetris — Đồ án Kỹ năng nghề nghiệp, UIT

Đồ án môn Kỹ năng nghề nghiệp của nhóm 5 thành viên, Trường Đại học Công nghệ Thông tin — ĐHQG TP.HCM.

Dự án bắt đầu từ **mã nguồn C++ của giảng viên** (`main.cpp`), sau đó nhóm port sang Python và phát triển tiếp.

---

## 👥 Thành viên nhóm

| # | Họ và tên | MSSV | GitHub | Phần việc |
|---|-----------|------|--------|-----------|
| SV1 | Hồ Văn Trọng | 26730077 | [@tronghv77](https://github.com/tronghv77) | Nhóm trưởng — đưa code gốc lên Git, port sang Python, duyệt và gộp mã nguồn |
| SV2 | Vũ Anh Tuấn | 26730080 | [@26730080](https://github.com/26730080) | Viết hàm `remove_line()` — xoá hàng đã đầy |
| SV3 | Đặng Đức Tín | 26730073 | [@26730073](https://github.com/26730073) | Sửa giao diện: viền và block cho vuông vức, hiện đang bị dẹt |
| SV4 | Trương Đình Nguyên | 26730052 | [@nguyen26730052](https://github.com/nguyen26730052) | Nghiên cứu và viết phần xoay block |
| SV5 | Phan Nguyễn Minh Thảo | 26730063 | [@26730063](https://github.com/26730063) | Mỗi lần xoá hàng thì tốc độ rơi nhanh hơn; chủ biên báo cáo |

Chi tiết từng việc: [docs/PHAN-CONG.md](docs/PHAN-CONG.md)

---

## 📁 Mã nguồn

| File | Nội dung |
|------|----------|
| `main.cpp` | **Mã nguồn gốc của giảng viên**, giữ nguyên không sửa. Đây là điểm xuất phát của cả nhóm. |
| `tetris.py` | Bản port sang Python, dịch sát từng hàm từ `main.cpp`. Nhóm phát triển tiếp trên file này. |

Bản port cố ý giữ nguyên lối viết của bản C++: dùng biến toàn cục, vẽ bằng ký tự trong cửa sổ dòng lệnh, đọc phím bằng `msvcrt`. Giữ vậy để dễ đối chiếu hai bản, và để dành phần chuyển sang lập trình hướng đối tượng cho giai đoạn sau.

### Bảng đối chiếu tên hàm

| `main.cpp` | `tetris.py` |
|---|---|
| `canMove` | `can_move` |
| `block2Board` | `block_to_board` |
| `boardDelBlock` | `board_del_block` |
| `initBoard` | `init_board` |
| `draw` | `draw` |
| `removeLine` | `remove_line` |

---

## 🚀 Cách chạy

Yêu cầu: **Python 3.10 trở lên**, chạy trên **Windows** (dùng `msvcrt` để đọc phím, giống `conio.h` của bản C++).

```bash
git clone https://github.com/tronghv77/tetris-game-uit.git
cd tetris-game-uit
python tetris.py
```

Không cần cài thư viện ngoài.

### Điều khiển

| Phím | Tác dụng |
|------|----------|
| `a` | Sang trái |
| `d` | Sang phải |
| `w` | Xoay khối |
| `x` | Rơi nhanh một hàng |
| `q` | Thoát |

Bản gốc của giảng viên chưa có phím xoay. Phím `w` do nhóm bổ sung.

---

## 📋 Yêu cầu định lượng của môn học

| Chỉ tiêu | Ghi chú |
|---|---|
| 100% thành viên đóng góp mã nguồn trên Git | Mỗi người có phần việc riêng trong bảng trên |
| Trên 50 commit | Commit nhỏ và thường xuyên, mỗi lần một việc. **Đừng gom cả phần việc vào một commit** |
| Trên 3 conflict | Cả nhóm cùng sửa `tetris.py` nên conflict sẽ phát sinh tự nhiên. Cách xử lý ghi ở [docs/HUONG-DAN-GIT.md](docs/HUONG-DAN-GIT.md) |
| Trên 6 nhánh | Mỗi phần việc một nhánh riêng, không dùng lại nhánh cũ. **Không xoá nhánh sau khi merge** |

### Cách tự kiểm tra bốn chỉ tiêu

```bash
git log --oneline | wc -l                      # số commit
git branch -r | wc -l                          # số nhánh trên GitHub
git shortlog -sne --no-merges                  # ai đã đóng góp bao nhiêu commit
git log --grep=conflict --oneline               # các lần xử lý conflict
```

Chạy `git shortlog -sne --no-merges` để chắc chắn commit của mình được tính
đúng tên. Nếu tên hoặc email hiện ra không khớp tài khoản GitHub thì commit đó
không được ghi nhận cho ai, sửa bằng:

```bash
git config --global user.email "mssv@ms.uit.edu.vn"
```

---

## 🤝 Quy trình làm việc

1. Nhóm trưởng đưa mã nguồn gốc của giảng viên lên Git ✅
2. Nhóm trưởng port sang Python ✅
3. Mỗi thành viên nhận một phần việc, làm trên nhánh riêng
4. Xong thì tạo Pull Request, nhóm trưởng duyệt rồi merge

**Không ai push thẳng lên nhánh `main`.** Hướng dẫn Git cho người mới: [docs/HUONG-DAN-GIT.md](docs/HUONG-DAN-GIT.md)

---

## 🛠️ Công cụ nhóm sử dụng

| Công cụ | Dùng để |
|---------|---------|
| GitHub | Quản lý mã nguồn, giao việc qua Issues, duyệt code qua Pull Request |
| Slack | Kênh thảo luận chính của nhóm |
| Google Docs | Cùng viết báo cáo |

---

## 📄 Giấy phép

[MIT License](LICENSE) — áp dụng cho phần mã nguồn do nhóm viết. File `main.cpp` thuộc về giảng viên.
