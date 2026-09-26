# Phân công công việc

Phân công theo đúng gợi ý của giảng viên: SV1 đưa mã nguồn gốc lên Git, bốn thành
viên còn lại mỗi người làm một phần.

Cả nhóm cùng sửa file `tetris.py`, nên **conflict sẽ xảy ra** — đó là chuyện bình
thường và cũng nằm trong yêu cầu của môn học. Cách xử lý xem
[HUONG-DAN-GIT.md](HUONG-DAN-GIT.md).

---

## SV1 — Hồ Văn Trọng (26730077), nhóm trưởng

- [x] Đưa `main.cpp` của giảng viên lên Git, giữ nguyên không sửa
- [x] Port sang Python thành `tetris.py`, dịch sát từng hàm
- [x] Duyệt Pull Request của các bạn, hướng dẫn xử lý conflict
- [ ] Soạn hợp đồng nhóm và mục link công cụ trong báo cáo

---

## SV2 — Vũ Anh Tuấn (26730080)

**Việc:** viết hàm `remove_line()` trong `tetris.py`

Bản port hiện chưa có hàm này, nên hàng đầy vẫn nằm nguyên tại chỗ.

- [x] Viết `remove_line()`: tìm hàng đã đầy, xoá đi, đẩy các hàng phía trên rơi xuống
- [x] Gọi hàm đó trong `main()`, ngay sau `block_to_board()`

**Xong khi:** xếp đầy một hàng thì hàng đó biến mất và phần phía trên tụt xuống.

**Gợi ý:** hàm `removeLine()` trong `main.cpp` đã làm đúng việc này, đọc để hiểu
ý tưởng rồi viết lại bằng Python. Chú ý viền trái phải là dấu `#`, nên khi kiểm
tra hàng đầy phải xét đúng vùng bên trong.

---

## SV3 — Đặng Đức Tín (26730073)

**Việc:** sửa giao diện cho viền và block vuông vức

Ký tự trong cửa sổ dòng lệnh cao hơn là rộng, nên bảng chơi hiện bị dẹt thành
hình chữ nhật thay vì vuông.

- [x] Sửa hàm `draw()` để mỗi ô chiếm hai ký tự bề ngang
- [x] Chọn ký tự vẽ viền và vẽ block cho dễ nhìn

**Xong khi:** nhìn vào bảng chơi thấy các ô vuông vức, không bị kéo dẹt.

---

## SV4 — Trương Đình Nguyên (26730052)

**Việc:** nghiên cứu và viết phần xoay block

Bản của giảng viên chưa có xoay, hiện chỉ có các phím `a`, `d`, `x`, `q`.

- [x] Thêm một phím xoay
- [x] Viết phần xoay: đổi `b` sang trạng thái xoay tương ứng
- [x] Kiểm tra `can_move()` trước khi nhận nước xoay, tránh khối xoay xuyên tường

**Xong khi:** bấm phím xoay thì khối xoay đúng, sát tường không bị lỗi.

**Lưu ý:** mảng `blocks` có sẵn 16 khối nhưng `random.randint(0, 6)` chỉ lấy khối
0 đến 6, tức là chỉ ra khối I và O. Các khối T, S, Z, J, L nằm ở vị trí 11 đến 15
chưa bao giờ xuất hiện — đây là chỗ cần bàn với cả nhóm khi làm phần xoay.

---

## SV5 — Phan Nguyễn Minh Thảo (26730063)

**Việc 1:** mỗi lần xoá được hàng thì tốc độ rơi nhanh hơn

- [ ] Thay thời gian chờ cố định 0.5 giây ở cuối `main()` bằng một biến tốc độ
- [ ] Mỗi lần `remove_line()` xoá được hàng thì giảm thời gian chờ
- [ ] Đặt một mức chờ tối thiểu để game không nhanh tới mức không chơi nổi

**Xong khi:** xoá càng nhiều hàng thì khối rơi càng nhanh, nhưng vẫn chơi được.

**Lưu ý:** phần này phụ thuộc vào `remove_line()` của Tuấn. Chờ Tuấn merge xong
rồi bắt đầu, hoặc trao đổi trước để thống nhất hàm trả về số hàng đã xoá.

**Việc 2:** chủ biên phần giới thiệu và hướng dẫn chơi Tetris trong báo cáo, làm
trên Google Docs của nhóm.

---

## Lỗi tìm được trong mã nguồn gốc của giảng viên

Ba lỗi nhóm phát hiện khi đọc và port `main.cpp`. Nên đưa vào báo cáo.

1. **`rand()%7` chỉ sinh ra hai loại khối.** Bảy phần tử đầu của mảng `blocks`
   chỉ gồm khối I và O, nên T, S, Z, J, L ở vị trí 11–15 không bao giờ xuất
   hiện. Nguyên xử lý bằng danh sách `first_states`.
2. **`removeLine()` biến hàng trên cùng thành tường.** Vòng lặp chép hàng viền
   `#` ở trên xuống hàng 1, nên mỗi lần xoá hàng lại mọc thêm một bức tường.
   Tuấn xử lý bằng cách dừng ở hàng 2 rồi đặt lại hàng 1 thành hàng trống.
3. **Ô hiển thị bị kéo dẹt.** Ký tự trong cửa sổ dòng lệnh cao hơn là rộng nên
   bảng chơi thành hình chữ nhật. Tín xử lý bằng cách in mỗi ô thành hai ký tự.

---

## Yêu cầu định lượng cần theo dõi

| Chỉ tiêu | Cách đạt |
|---|---|
| 100% thành viên đóng góp mã nguồn | Mỗi người đã có một phần việc code riêng |
| Trên 50 commit | Commit nhỏ, mỗi lần một việc. Đừng dồn cả phần việc vào một commit |
| Trên 3 conflict | Cả nhóm cùng sửa `tetris.py` nên sẽ có. Gặp conflict thì tự xử lý và báo trong Slack |
| Trên 6 nhánh | Mỗi phần việc một nhánh riêng, sửa tiếp thì mở nhánh mới |
