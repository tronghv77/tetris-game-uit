"""Lỗi 4: bản gốc không có điều kiện thua, vòng while(1) chạy mãi.

Script dựng một bảng đã đầy tới đỉnh rồi chạy đúng phần thân vòng lặp
của main() trong main.cpp (dòng 132-150), bỏ phần đọc bàn phím. Mỗi lượt
đều cho cùng một kết quả: khối mới không rơi được, bản gốc cố định nó rồi
sinh khối mới, không có chỗ nào thoát ra.

Chạy:  python docs/chung-minh-loi/loi4_khong_bao_gio_thua.py
"""

import sys

if sys.platform == "win32":
    try:
        import ctypes
        ctypes.windll.kernel32.SetConsoleOutputCP(65001)
    except Exception:
        pass
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

H = 20
W = 15
SO_LUOT_THU = 50

# Khối I dựng đứng, lấy từ main.cpp dòng 11-14.
# Chọn khối này vì nó có ô ngay ở hàng đầu của lưới 4x4, nhờ vậy thấy được
# luôn chuyện khối sinh ra ở y = 0 thì ghi đè lên hàng viền trên cùng.
KHOI = [
    " I  ",
    " I  ",
    " I  ",
    " I  ",
]


def bang_day_toi_dinh():
    """Bảng có viền, vùng chơi xếp kín từ hàng 1 tới hàng 18."""
    b = []
    for i in range(H):
        hang = []
        for j in range(W):
            if i == 0 or i == H - 1 or j == 0 or j == W - 1:
                hang.append("#")
            else:
                hang.append("T")
        b.append(hang)
    return b


def can_move(board, x, y, dx, dy):
    """Đúng canMove() ở main.cpp dòng 76-86."""
    for i in range(4):
        for j in range(4):
            if KHOI[i][j] != " ":
                xt = x + j + dx
                yt = y + i + dy
                if xt < 1 or xt >= W - 1 or yt >= H - 1:
                    return False
                if board[yt][xt] != " ":
                    return False
    return True


def block_to_board(board, x, y):
    """Đúng block2Board() ở main.cpp dòng 87-92."""
    for i in range(4):
        for j in range(4):
            if KHOI[i][j] != " ":
                board[y + i][x + j] = KHOI[i][j]


def main():
    board = bang_day_toi_dinh()
    vien_tren_ban_dau = "".join(board[0])

    print("Bảng đã xếp kín từ hàng 1 tới hàng 18, không còn chỗ trống.")
    print("Khối mới sinh ra ở x = 5, y = 0 đúng như main.cpp dòng 145.")
    print()
    print("Lượt   canMove(0,1)   Bản gốc làm gì")
    print("-" * 56)

    x, y = 5, 0
    so_lan_sinh_khoi = 0

    for luot in range(1, SO_LUOT_THU + 1):
        roi_duoc = can_move(board, x, y, 0, 1)

        if roi_duoc:
            y += 1
            viec = "khối rơi xuống một ô"
        else:
            block_to_board(board, x, y)
            x, y = 5, 0
            so_lan_sinh_khoi += 1
            viec = "cố định khối rồi sinh khối mới ở y = 0"

        if luot <= 5 or luot == SO_LUOT_THU:
            print(f"{luot:>4}   {str(roi_duoc):<13}  {viec}")
        elif luot == 6:
            print("  ..   ...            (giống hệt các lượt trên)")

    print()
    print("KẾT QUẢ")
    print("-" * 56)
    print(f"Chạy {SO_LUOT_THU} lượt, sinh khối mới {so_lan_sinh_khoi} lần,")
    print("không lượt nào thoát khỏi vòng lặp.")
    print()
    print("Trong main.cpp, vòng while(1) ở dòng 132 chỉ có một lối ra duy")
    print("nhất là dòng 139:  if (c == 'q') break;")
    print("Không có chỗ nào kiểm tra bảng đã đầy. Game không bao giờ báo thua.")
    print()

    vien_tren_bay_gio = "".join(board[0])
    print("Thêm một hệ quả: khối sinh ra ở y = 0 nên block2Board ghi đè")
    print("lên cả hàng viền trên cùng.")
    print(f"  Hàng 0 lúc đầu    : {vien_tren_ban_dau}")
    print(f"  Hàng 0 sau khi chạy: {vien_tren_bay_gio}")
    if vien_tren_ban_dau != vien_tren_bay_gio:
        print("  Viền trên đã bị khối ghi đè. Đây là gốc của lỗi 4 và lỗi 5.")
    print()
    print("NHÓM XỬ LÝ — tetris.py dòng 474-484 và 613-629")
    print("-" * 56)
    print("Thêm hàm is_game_over() trả về  not can_move(0, 1)")
    print("Khối vừa sinh ra mà không rơi xuống được nghĩa là bảng đã đầy.")
    print("Vòng lặp chính gọi hàm này sau mỗi lần sinh khối, thua thì hiện")
    print("màn hình báo thua và cho chọn chơi lại hay thoát.")
    print()
    print("Lưu ý quan trọng: phải là can_move(0, 1) chứ không phải")
    print("can_move(0, 0). Xem script loi5_khong_xoay_duoc.py để biết vì sao.")


if __name__ == "__main__":
    main()
