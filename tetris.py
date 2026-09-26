"""Tetris - SV4: Xoay khối."""

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

    i = H - 2

    while i > 0:

        if " " not in board[i]:

            for ii in range(i, 1, -1):
                board[ii] = board[ii - 1][:]

            board[1] = ["#"] + [" "] * (W - 2) + ["#"]

            draw()
            time.sleep(0.2)

        else:
            i -= 1


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

        # Nếu xoay bị đụng tường / khối khác
        # thì quay lại trạng thái cũ
        b = old_b


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
    """Khối vừa sinh ra đã không còn chỗ đứng nghĩa là bảng đầy tới đỉnh.

    Bản C++ của thầy không có phần này: khi bảng đầy, khối mới cứ bị khoá
    ngay tại đỉnh rồi lại sinh khối mới, vòng lặp chạy mãi không dừng.
    """
    return not can_move(0, 0)


# ============================================================
# MAIN
# ============================================================

def main():

    global x, y, b

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

    # Vòng ngoài: mỗi lượt là một ván chơi
    while True:

        init_board()

        # Số khối đã xếp được trong ván này
        pieces = 0

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

                # Thoát hẳn, không chơi lại
                if c == "q":
                    return

            # Khối tự động rơi
            if can_move(0, 1):

                y += 1

            else:

                # Không rơi được nữa -> cố định khối
                block_to_board()

                # Xoá hàng
                remove_line()

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
            time.sleep(0.5)


if __name__ == "__main__":
    main()
