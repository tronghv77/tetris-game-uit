# Tổng kết đồ án

Trang này gom lại toàn bộ minh chứng của nhóm vào một chỗ, để người đọc không
phải lục từng Pull Request.

Mọi con số dưới đây đều kiểm chứng được bằng lệnh Git, có ghi sẵn ở cuối trang.

---

## Đồ án bắt đầu từ đâu

Commit đầu tiên của repo là `b5e2762` — **mã nguồn C++ của giảng viên, giữ
nguyên văn, không sửa một dòng nào**.

```bash
git log --oneline --reverse | head -1
git show b5e2762 --stat
```

Bản port sang Python nằm ở commit sau đó, trong file `tetris.py`. Bản port cố ý
**bỏ trống** hàm `remove_line()` để SV2 tự viết. Lý do của lựa chọn này ghi
trong [README](../README.md).

---

## Năm chỉ tiêu của môn học

| Chỉ tiêu | Yêu cầu | Đạt được |
|---|---|---|
| Thành viên đóng góp mã nguồn | 100% | 5/5 |
| Số commit | > 50 | xem lệnh kiểm tra bên dưới |
| Số conflict đã xử lý | > 3 | 6 |
| Số nhánh | > 6 | 11 |
| Chữ ký hợp đồng nhóm | 5/5 | 5/5, ký ngày 26/09/2026 |

---

## Ai làm gì

| Thành viên | Phần việc | Pull Request |
|---|---|---|
| Hồ Văn Trọng | Đưa mã nguồn gốc lên Git, port sang Python, kết thúc game, màn hình bắt đầu, tạm dừng, file kiểm tra tự động | #11, #15, #16, #19, #23, #24, #25 |
| Vũ Anh Tuấn | Xoá hàng đã đầy, hiển thị điểm và số hàng | #10, #18 |
| Đặng Đức Tín | Viền và khối vuông vức, hiện khối kế tiếp | #12, và commit `b722450` |
| Trương Đình Nguyên | Xoay khối, sửa lỗi `rand()%7` chỉ sinh ra hai loại khối | #13 |
| Phan Nguyễn Minh Thảo | Tăng tốc độ rơi sau mỗi lần xoá hàng, chủ biên Phần 3 báo cáo | #14 |

---

## Sáu lần gặp và xử lý conflict

Cả nhóm cùng sửa một file `tetris.py`, nên conflict phát sinh tự nhiên chứ
không phải dựng lên cho đủ chỉ tiêu.

| # | Commit | Người gỡ | Đụng giữa |
|---|---|---|---|
| 1 | `b7ae74e` | Phan Nguyễn Minh Thảo | Tăng tốc độ rơi × xoay khối |
| 2 | `9d0cc32` | Hồ Văn Trọng | Kết thúc game × tăng tốc độ rơi |
| 3 | `0a1711c` | Vũ Anh Tuấn | Điểm số × tăng tốc × kết thúc game |
| 4 | `be484e9` | Hồ Văn Trọng | Điểm số × khối kế tiếp |
| 5 | `f6f263a` | Hồ Văn Trọng | Bảng phím trong README, hai nhánh cùng thêm một dòng |
| 6 | `023ca79` | Hồ Văn Trọng | Mẫu Pull Request |

Cách xử lý từng lần ghi trong mô tả của Pull Request tương ứng.

---

## Năm lỗi tìm được trong mã nguồn gốc

Đây là phần nhóm thấy đáng nói nhất. Bốn trong năm lỗi chỉ lộ ra khi ngồi chơi
thật, chứ không phải khi đọc code.

**1. `rand()%7` chỉ sinh ra khối I và O.** Bảy phần tử đầu của mảng `blocks`
chỉ gồm hai loại đó, còn T, S, Z, J, L nằm ở vị trí 11 đến 15 nên không bao giờ
xuất hiện. Chơi bản gốc sẽ thấy chỉ rơi hai loại khối.
*Nguyên xử lý bằng danh sách `first_states`.*

**2. `removeLine()` biến hàng trên cùng thành tường.** Vòng lặp chép hàng viền
`#` ở trên xuống hàng 1, nên mỗi lần xoá hàng lại mọc thêm một bức tường.
*Tuấn xử lý bằng cách dừng ở hàng 2 rồi đặt lại hàng 1 thành hàng trống.*

**3. Ô hiển thị bị kéo dẹt.** Ký tự trong cửa sổ dòng lệnh cao hơn là rộng, nên
bảng chơi thành hình chữ nhật thay vì vuông.
*Tín xử lý bằng cách in mỗi ô thành hai ký tự.*

**4. Game không bao giờ kết thúc.** Bảng đầy tới đỉnh thì khối mới bị khoá ngay
tại chỗ rồi lại sinh khối mới, vòng `while (1)` chạy mãi, chỉ thoát được bằng
phím `q`.
*Trọng xử lý bằng `is_game_over()` và màn hình báo thua.*

**5. Khối vừa sinh ra không xoay được.** Khối sinh ra ở `y = 0` nên nhiều trạng
thái xoay có ô nằm ngay hàng 0, là hàng viền `#`. Phép thử `canMove(0, 0)` trả
về sai và nước xoay bị huỷ. Sáu trên bảy loại khối dính lỗi này.
*Xử lý bằng wall kick: xoay không lọt thì thử nhích khối một ô rồi xét lại.*

Lỗi 4 và lỗi 5 cùng một nguyên nhân gốc: bản C++ vẽ khối đè lên hàng viền trên
cùng, nên mọi phép thử `canMove(0, 0)` tại `y = 0` đều sai. Nhóm dính bẫy này
hai lần trước khi hiểu ra.

---

## Cách người đọc tự kiểm chứng

```bash
git clone https://github.com/tronghv77/tetris-game-uit.git
cd tetris-game-uit

git log --oneline | wc -l              # số commit
git branch -r | grep -v HEAD | wc -l   # số nhánh
git log --no-merges --format='%an' | sort | uniq -c | sort -rn   # ai bao nhiêu commit
git log --oneline -i --grep=conflict   # các lần gỡ conflict
git log --oneline --reverse | head -1  # commit đầu tiên là mã nguồn của thầy

python tetris.py      # chơi thử
python kiem_tra.py    # chạy 54 phép kiểm tra tự động
```

---

## Những thứ nhóm chưa làm

Ghi lại cho đầy đủ, không giấu:

- Ô giữ khối, xem trước nhiều hơn một khối, thả khối thẳng xuống đáy bằng một phím
- Nhân điểm theo cấp độ, và lên cấp sau mỗi 10 hàng
- Chuyển sang lập trình hướng đối tượng. Bản hiện tại vẫn giữ lối viết dùng
  biến toàn cục của bản C++, cố ý giữ vậy để dễ đối chiếu hai bản
