# Năm lỗi trong mã nguồn gốc — minh chứng và cách xử lý

Trang này dành cho người muốn tự kiểm chứng, không phải đọc rồi tin.

Mỗi lỗi có bốn phần: dòng code gốc gây ra lỗi, một script chạy được để
thấy lỗi xảy ra thật, cách nhóm xử lý, và ai xử lý.

Mã nguồn gốc nằm ở commit đầu tiên của repo, `b5e2762` — bản C++ của
giảng viên, giữ nguyên văn. Mọi số dòng `main.cpp` dưới đây đọc được ở đó.

```bash
git show b5e2762 --stat          # commit đầu tiên, chỉ có main.cpp
git show b5e2762:main.cpp        # xem nguyên văn bản gốc
```

Chạy cả năm script một lượt:

```bash
python docs/chung-minh-loi/loi1_sinh_khoi.py
python docs/chung-minh-loi/loi2_moc_tuong.py
python docs/chung-minh-loi/loi3_o_bi_det.py
python docs/chung-minh-loi/loi4_khong_bao_gio_thua.py
python docs/chung-minh-loi/loi5_khong_xoay_duoc.py
```

Bốn script đầu không cần thư viện gì ngoài Python. Script thứ năm gọi
thẳng `tetris.py` nên phải chạy từ thư mục gốc của dự án.

---

## Lỗi 1 — `rand()%7` chỉ sinh ra hai loại khối

**Trong bản gốc:** `main.cpp` dòng 130 và 145

```cpp
x = 5; y = 0; b = rand()%7;
```

Mảng `blocks` ở dòng 10 có 16 phần tử, xếp theo thứ tự trạng thái xoay chứ
không phải theo loại khối. Bảy phần tử đầu — tức là toàn bộ khoảng mà
`rand()%7` chạm tới — chỉ gồm khối I và khối O. Năm loại còn lại nằm ở chỉ
số 11 đến 15.

**Chứng minh:** `loi1_sinh_khoi.py` đọc thẳng `main.cpp`, tách mảng
`blocks`, in ra loại khối của từng chỉ số. Không có số liệu nào viết tay.

```
rand()%7 trả về số từ 0 đến 6, nên chỉ chạm tới 7 phần tử đầu.
  Loại khối xuất hiện được : I, O
  Loại khối không bao giờ ra: J, L, S, T, Z
```

**Cách xử lý:** `tetris.py` dòng 498–506 liệt kê đích danh trạng thái đầu
của cả bảy loại khối, rồi `random.choice` trên danh sách đó ở dòng 532.

```python
first_states = [0, 2, 3, 7, 9, 11, 15]
next_b = random.choice(first_states)
```

**Người xử lý:** Trương Đình Nguyên — PR #13.

---

## Lỗi 2 — `removeLine()` dựng tường rồi kẹt trong vòng lặp vô hạn

**Trong bản gốc:** `main.cpp` dòng 117–119

```cpp
for (int ii = i ; ii > 0 ; ii--)
    for (int jj = 0; jj < W; jj++)
        board[ii][jj] = board[ii-1][jj];
```

Vòng dồn hàng chạy tới `ii = 1`, nên nó chép hàng 0 xuống hàng 1. Hàng 0 là
hàng viền, toàn dấu `#`. Sau lần xoá hàng đầu tiên, hàng 1 thành một bức
tường đặc.

Hậu quả nặng hơn một bức tường. Hàng 1 giờ không còn ô trống nào, nên lần
xét tiếp theo thuật toán coi đó là một hàng đầy và xoá tiếp — xoá xong lại
chép hàng 0 xuống, hàng 1 lại thành tường. Vòng `for` ở dòng 113 không bao
giờ kết thúc.

**Chứng minh:** `loi2_moc_tuong.py` chép lại nguyên văn thuật toán sang
Python, chạy trên một bảng có sẵn một hàng đầy. Script đặt mức chặn 200
lượt, nếu không nó sẽ treo đúng như bản gốc treo.

```
Hàng chơi được giờ toàn dấu thăng: [1]
Thuật toán chạy quá 200 lượt mà không dừng, script phải tự chặn.
```

Trong game thật, mỗi lượt đều gọi `draw()` và `_sleep(200)` ở dòng 121–122,
nên màn hình nhấp nháy liên tục thay vì đứng im — dễ tưởng là máy chậm chứ
không phải treo.

**Cách xử lý:** `tetris.py` dòng 301–304. Vòng dồn hàng dừng ở hàng 2,
không chạm hàng 1, rồi dựng lại hàng 1 thành hàng trống có viền hai bên.

```python
for ii in range(i, 1, -1):
    board[ii] = board[ii - 1][:]

board[1] = ["#"] + [" "] * (W - 2) + ["#"]
```

Hàng 1 luôn có ô trống nên không bao giờ bị coi là hàng đầy.

**Người xử lý:** Vũ Anh Tuấn — PR #10.

---

## Lỗi 3 — ô hiển thị bị kéo dẹt

**Trong bản gốc:** `main.cpp` dòng 109

```cpp
for (int j = 0 ; j < W ; j++) cout<<board[i][j];
```

Mỗi ô in bằng một ký tự. Ký tự trong cửa sổ dòng lệnh không vuông: phông
mặc định của Windows Console rộng 8 điểm ảnh, cao 16 điểm ảnh.

Bảng 15 ô ngang và 20 ô dọc đáng lẽ có tỉ lệ 0,75. In một ký tự mỗi ô cho
ra 120 × 320 điểm ảnh, tỉ lệ 0,38 — hẹp bằng một nửa. Khối O vuông vức
hiện ra thành hình chữ nhật đứng.

**Chứng minh:** `loi3_o_bi_det.py` in cùng một bảng theo hai cách, kèm một
khối O để nhìn thấy khác biệt, và tính tỉ lệ cho cả hai.

```
Tỉ lệ đúng phải là 0.75 vì bảng 15 ô ngang và 20 ô dọc.
Cách của bản gốc cho 0.38, cách sửa cho 0.75.
```

**Cách xử lý:** `tetris.py` dòng 276–281, mỗi ô in thành hai ký tự.

```python
if cell == "#":
    row.append("##")
elif cell == " ":
    row.append("  ")
else:
    row.append("[]")
```

**Người xử lý:** Đặng Đức Tín — PR #12.

---

## Lỗi 4 — game không bao giờ kết thúc

**Trong bản gốc:** `main.cpp` dòng 132 và 139

```cpp
while (1){
    ...
    if (c == 'q') break;
```

Vòng lặp chính chỉ có một lối ra: bấm phím `q`. Không có chỗ nào kiểm tra
bảng đã đầy. Khi bảng xếp kín tới đỉnh, khối mới bị khoá ngay tại chỗ, bản
gốc cố định nó rồi sinh khối mới, lặp lại mãi.

**Chứng minh:** `loi4_khong_bao_gio_thua.py` dựng một bảng đã đầy rồi chạy
đúng phần thân vòng lặp của `main()`, bỏ phần đọc bàn phím.

```
Chạy 50 lượt, sinh khối mới 50 lần, không lượt nào thoát khỏi vòng lặp.
```

Script in thêm một thứ đáng chú ý: khối sinh ra ở `y = 0` nên `block2Board`
ghi đè lên cả hàng viền trên cùng.

```
  Hàng 0 lúc đầu    : ###############
  Hàng 0 sau khi chạy: ######I########
```

Đây là nguyên nhân gốc chung của lỗi 4 và lỗi 5.

**Cách xử lý:** `tetris.py` dòng 474–484 thêm hàm `is_game_over()`, dòng
613–629 gọi hàm này sau mỗi lần sinh khối.

```python
def is_game_over():
    return not can_move(0, 1)
```

Phải là `can_move(0, 1)` chứ không phải `can_move(0, 0)`. Khối I, T, J, L
sinh ra có ô nằm ngay hàng 0 — hàng viền — nên xét tại chỗ thì ván nào cũng
báo thua ngay từ khối đầu tiên. Nhóm đã viết sai đúng kiểu đó rồi mới sửa.

**Người xử lý:** Hồ Văn Trọng — PR #16, commit `3119190`.

---

## Lỗi 5 — khối vừa sinh ra không xoay được

Bản C++ không có chức năng xoay. Lỗi này lộ ra khi nhóm thêm `rotate_block()`,
nhưng nguyên nhân thì nằm sẵn trong thiết kế của bản gốc: khối sinh ra ở
`y = 0`, chồng lên hàng viền trên cùng.

**Hiện tượng:** nhiều trạng thái xoay có ô nằm ở hàng đầu của lưới 4×4,
tức là hàng 0 của bảng. Phép thử `can_move(0, 0)` thấy ô viền `#` ở đó nên
trả về `False`, nước xoay bị huỷ. Bấm `w` ngay lúc khối vừa xuất hiện
không có tác dụng.

**Chứng minh:** `loi5_khong_xoay_duoc.py` gọi thẳng `blocks` và `can_move`
của `tetris.py`, không chép lại, nên kết quả là hành vi thật của game.

```
Khối   Không wall kick   Có wall kick
--------------------------------------------
I      xoay được         xoay được
O      KHÔNG xoay        KHÔNG xoay
T      KHÔNG xoay        xoay được
S      KHÔNG xoay        xoay được
Z      KHÔNG xoay        xoay được
J      KHÔNG xoay        xoay được
L      KHÔNG xoay        xoay được
```

Sáu trên bảy loại khối dính lỗi. Khối O nằm ngoài vì nó xoay vẫn là chính
nó, trạng thái không đổi nên không tính.

**Cách xử lý:** `tetris.py` dòng 387–394, wall kick. Xoay xong mà không lọt
thì thử nhích khối một ô rồi xét lại.

```python
for dx, dy in ((0, 0), (-1, 0), (1, 0), (0, 1)):
    if can_move(dx, dy):
        x += dx
        y += dy
        return

b = old_b
```

Bước `(0, 1)` nhích xuống một ô là bước gỡ được đúng lỗi này. Thử hết bốn
cách không lọt thì huỷ nước xoay.

**Người xử lý:** Hồ Văn Trọng — PR #25, commit `def6ea8`, trên nền hàm
`rotate_block()` của Trương Đình Nguyên ở PR #13.

---

## Hai lỗi cuối cùng một nguyên nhân gốc

Bản C++ cho khối sinh ra ở `y = 0`, chồng lên hàng viền trên cùng. Vì vậy
mọi phép thử `can_move(0, 0)` tại `y = 0` đều trả về `False`, dù khối hoàn
toàn hợp lệ.

Nhóm dính đúng cái bẫy này hai lần ở hai chỗ khác nhau — một lần trong
`is_game_over()`, một lần trong `rotate_block()` — rồi mới nhận ra đó là
cùng một chuyện.

| | Viết sai | Sửa thành |
|---|---|---|
| `is_game_over()` | `can_move(0, 0)` | `can_move(0, 1)` |
| `rotate_block()` | chỉ xét `can_move(0, 0)` | thử thêm `(-1,0)`, `(1,0)`, `(0,1)` |

---

## Bảng tổng hợp

| # | Lỗi | Dòng trong `main.cpp` | Sửa ở `tetris.py` | Người xử lý |
|---|---|---|---|---|
| 1 | Chỉ ra hai loại khối | 130, 145 | 498–506, 532 | Trương Đình Nguyên (#13) |
| 2 | Mọc tường, kẹt vòng lặp | 117–119 | 301–304 | Vũ Anh Tuấn (#10) |
| 3 | Ô bị kéo dẹt | 109 | 276–281 | Đặng Đức Tín (#12) |
| 4 | Không bao giờ thua | 132, 139 | 474–484, 613–629 | Hồ Văn Trọng (#16) |
| 5 | Khối mới không xoay được | thiết kế `y = 0` | 387–394 | Hồ Văn Trọng (#25) |
