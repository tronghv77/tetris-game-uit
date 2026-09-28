"""Tetris — bản port sang Python từ main.cpp của giảng viên.

Người phụ trách bản port: Hồ Văn Trọng (26730077)

Bản này dịch sát từng hàm trong `main.cpp`: vẫn dùng biến toàn cục, vẫn vẽ
bằng ký tự trong cửa sổ dòng lệnh, vẫn đọc phím bằng thư viện chuẩn của
Windows. Giữ nguyên như vậy để dễ đối chiếu với bản C++, và để dành phần
chuyển sang lập trình hướng đối tượng cho giai đoạn sau.

Bảng đối chiếu tên hàm:

    C++             Python
    canMove         can_move
    block2Board     block_to_board
    boardDelBlock   board_del_block
    initBoard       init_board
    draw            draw
    removeLine      remove_line

Cách chơi:  a sang trái, d sang phải, w xoay khối, x rơi nhanh, q thoát.
Chạy:       python tetris.py
"""

import msvcrt
import os
import random
import time

H = 20
W = 15

# Bảng chơi
board = [[" "] * W for _ in range(H)]

# Vị trí khối
x = 0
y = 0
b = 0

# Tốc độ rơi mặc định (giây)
fall_speed = 0.5

# ============================================================
# CÁC KHỐI VÀ TRẠNG THÁI XOAY
# ============================================================
blocks = [
    # 0 - 1: I
    [
        " I  ",
        " I  ",
        " I  ",
        " I  "
    ],
    [
        "    ",
        "IIII",
        "    ",
        "    "
    ],

    # 2: O
    [
        "    ",
        " OO ",
        " OO ",
        "    "
    ],

    # 3 - 6: T
    [
        " T  ",
        "TTT ",
        "    ",
        "    "
    ],
    [
        " T  ",
        " TT ",
        " T  ",
        "    "
    ],
    [
        "    ",
        "TTT ",
        " T  ",
        "    "
    ],
    [
        " T  ",
        "TT  ",
        " T  ",
        "    "
    ],

    # 7 - 8: S
    [
        "    ",
        " SS ",
        "SS  ",
        "    "
    ],
    [
        " S  ",
        " SS ",
        "  S ",
        "    "
    ],

    # 9 - 10: Z
    [
        "    ",
        "ZZ  ",
        " ZZ ",
        "    "
    ],
    [
        " Z  ",
        "ZZ  ",
        "Z   ",
        "    "
    ],

    # 11 - 14: J
    [
        "J   ",
        "JJJ ",
        "    ",
        "    "
    ],
    [
        "JJ  ",
        "J   ",
        "J   ",
        "    "
    ],
    [
        "JJJ ",
        "  J ",
        "    ",
        "    "
    ],
    [
        " J  ",
        " J  ",
        "JJ  ",
        "    "
    ],

    # 15 - 18: L
    [
        "  L ",
        "LLL ",
        "    ",
        "    "
    ],
    [
        "L   ",
        "L   ",
        "LL  ",
        "    "
    ],
    [
        "LLL ",
        "L   ",
        "    ",
        "    "
    ],
    [
        "LL  ",
        " L  ",
        " L  ",
        "    "
    ],
]


# ============================================================
# KIỂM TRA KHỐI CÓ THỂ DI CHUYỂN KHÔNG
# ============================================================
def can_move(dx, dy):
    for i in range(4):
        for j in range(4):
            if blocks[b][i][j] != " ":
                xt = x + j + dx
                yt = y + i + dy

                # Đụng tường
                if xt < 1 or xt >= W - 1:
                    return False

                # Đụng đáy
                if yt >= H - 1:
                    return False

                # Đụng khối khác
                if board[yt][xt] != " ":
                    return False

    return True


# ============================================================
# ĐƯA KHỐI VÀO BẢNG
# ============================================================
def block_to_board():
    for i in range(4):
        for j in range(4):
            if blocks[b][i][j] != " ":
                board[y + i][x + j] = blocks[b][i][j]


# ============================================================
# XOÁ KHỐI KHỎI BẢNG
# ============================================================
def board_del_block():
    for i in range(4):
        for j in range(4):
            if blocks[b][i][j] != " ":
                board[y + i][x + j] = " "


# ============================================================
# KHỞI TẠO BẢNG
# ============================================================
def init_board():
    for i in range(H):
        for j in range(W):
            if i == 0 or i == H - 1 or j == 0 or j == W - 1:
                board[i][j] = "#"
            else:
                board[i][j] = " "


# ============================================================
# VẼ BẢNG
# ============================================================
def draw():
    os.system("cls")

    for i in range(H):
        row = []
        for cell in board[i]:
            if cell == "#":
                row.append("##")
            elif cell == " ":
                row.append("  ")
            else:
                row.append("[]")
        print("".join(row))


# ============================================================
# XOÁ HÀNG ĐẦY
# ============================================================
def remove_line():
    """Xóa các hàng đầy và trả về số hàng đã xóa."""
    lines_cleared = 0
    i = H - 2

    while i > 0:
        if " " not in board[i]:
            lines_cleared += 1
            for ii in range(i, 1, -1):
                board[ii] = board[ii - 1][:]

            board[1] = ["#"] + [" "] * (W - 2) + ["#"]

            draw()
            time.sleep(0.2)
        else:
            i -= 1

    return lines_cleared


# ============================================================
# XOAY KHỐI
# ============================================================
def rotate_block():
    global b

    # Trạng thái xoay của từng loại khối
    rotation = {
        # I
        0: 1,
        1: 0,
        # O
        2: 2,
        # T
        3: 4,
        4: 5,
        5: 6,
        6: 3,
        # S
        7: 8,
        8: 7,
        # Z
        9: 10,
        10: 9,
        # J
        11: 12,
        12: 13,
        13: 14,
        14: 11,
        # L
        15: 16,
        16: 17,
        17: 18,
        18: 15,
    }

    old_b = b

    # Chuyển sang trạng thái xoay
    b = rotation[b]

    # Kiểm tra vị trí mới
    if not can_move(0, 0):
        # Nếu xoay bị đụng tường / khối khác thì quay lại trạng thái cũ
        b = old_b


# ============================================================
# MÀN HÌNH BẮT ĐẦU
# ============================================================

def wait_any_key():
    """Chờ người chơi bấm một phím, trả về phím đó.

    Bỏ hết phím còn sót trong bộ đệm trước đã, không thì mấy phím bấm
    lúc đang chơi sẽ làm màn hình trôi qua ngay lập tức.
    """
    while msvcrt.kbhit():
        msvcrt.getch()

    return msvcrt.getch().decode("utf-8", errors="ignore")


def draw_start_screen():
    """Màn hình chào, hiện bảng phím trước khi vào ván đầu tiên."""
    os.system("cls")
    print()
    print("    ==================================")
    print("              T E T R I S             ")
    print("    ==================================")
    print()
    print("      Do an Ky nang nghe nghiep - UIT")
    print("      Nhom 07")
    print()
    print("    ----------------------------------")
    print("      a / d    sang trai / sang phai")
    print("      w        xoay khoi")
    print("      x        roi nhanh mot hang")
    print("      p        tam dung / choi tiep")
    print("      q        thoat")
    print("    ----------------------------------")
    print()
    print("      Nhan phim bat ky de bat dau...")


# ============================================================
# MÀN HÌNH TẠM DỪNG
# ============================================================

def draw_pause_screen():
    """Vẽ bảng chơi kèm khung báo đang tạm dừng."""
    draw()
    print()
    print("  ===============================")
    print("            TAM DUNG             ")
    print("  ===============================")
    print()
    print("     Nhan p de choi tiep")
    print("     Nhan q de thoat")


# ============================================================
# MÀN HÌNH KẾT THÚC
# ============================================================

def draw_game_over(pieces):
    """Vẽ màn hình báo thua kèm số khối đã xếp được."""
    draw()
    print()
    print("  ===============================")
    print("            GAME OVER            ")
    print("  ===============================")
    print(f"     So khoi da xep duoc: {pieces}")
    print()
    print("     Nhan r de choi lai")
    print("     Nhan q de thoat")


# ============================================================
# KIỂM TRA THUA
# ============================================================

def is_game_over():
    """Khối vừa sinh ra mà không rơi xuống được nữa nghĩa là bảng đầy tới đỉnh.

    Bản C++ của thầy không có phần này: khi bảng đầy, khối mới cứ bị khoá
    ngay tại đỉnh rồi lại sinh khối mới, vòng lặp chạy mãi không dừng.

    Phải xét `can_move(0, 1)` chứ không phải `can_move(0, 0)`. Khối I, T, J, L
    sinh ra có ô nằm ngay hàng 0, mà hàng 0 là viền `#`, nên xét tại chỗ thì
    ván nào cũng báo thua ngay từ khối đầu tiên.
    """
    return not can_move(0, 1)


# ============================================================
# MAIN
# ============================================================
def main():
    """Vòng lặp game. Dịch từ hàm main trong C++."""
    global x, y, b, fall_speed

    random.seed()

    # Chỉ chọn trạng thái ban đầu của từng loại khối
    # I, O, T, S, Z, J, L
    first_states = [
        0,      # I
        2,      # O
        3,      # T
        7,      # S
        9,      # Z
        11,     # J
        15      # L
    ]

    # Màn hình chào, bấm q ở đây là thoát luôn
    draw_start_screen()

    if wait_any_key() == "q":
        return

    # Vòng ngoài: mỗi lượt là một ván chơi
    while True:

        init_board()

        # Số khối đã xếp được trong ván này
        pieces = 0

        # Tốc độ rơi, đặt lại mỗi ván
        fall_speed = 0.5

        x = 5
        y = 0
        b = random.choice(first_states)

        # Vòng trong: một ván chơi
        while True:

            # Xoá khối hiện tại khỏi bảng
            board_del_block()

            # Kiểm tra phím
            if msvcrt.kbhit():

                c = msvcrt.getch().decode(
                    "utf-8",
                    errors="ignore"
                )

                # Sang trái
                if c == "a" and can_move(-1, 0):
                    x -= 1
                # Sang phải
                if c == "d" and can_move(1, 0):
                    x += 1

                # Rơi nhanh
                if c == "x" and can_move(0, 1):
                    y += 1

                # Xoay
                if c == "w":
                    rotate_block()

                # Tạm dừng
                if c == "p":

                    draw_pause_screen()

                    while True:
                        phim = wait_any_key()
                        if phim == "p":
                            break
                        if phim == "q":
                            return

                # Thoát hẳn, không chơi lại
                if c == "q":
                    return

            # Khối tự động rơi
            if can_move(0, 1):

                y += 1

            else:

                # Không rơi được nữa -> cố định khối
                block_to_board()

                # Xoá hàng và tăng tốc độ rơi
                lines = remove_line()

                if lines > 0:
                    fall_speed = max(
                        0.1,
                        fall_speed - 0.05 * lines
                    )

                pieces += 1

                # Tạo khối mới
                x = 5
                y = 0
                b = random.choice(first_states)

                # Khối mới không có chỗ đứng nghĩa là thua
                if is_game_over():

                    draw_game_over(pieces)

                    # Chờ người chơi chọn chơi lại hay thoát
                    while True:
                        phim = msvcrt.getch().decode(
                            "utf-8",
                            errors="ignore"
                        )
                        if phim == "r":
                            break
                        if phim == "q":
                            return

                    # Thoát vòng trong để bắt đầu ván mới
                    break

            # Đưa khối hiện tại vào bảng
            block_to_board()

            # Vẽ
            draw()

            # Tốc độ rơi
            time.sleep(fall_speed)


if __name__ == "__main__":
    main()
