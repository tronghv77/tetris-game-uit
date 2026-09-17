"""Tetris — bản port sang Python từ main.cpp của giảng viên.

Người phụ trách bản port: Hồ Văn Trọng (26730077)

Bản này dịch sát từng hàm trong `main.cpp`: vẫn dùng biến toàn cục, vẫn vẽ
bằng ký tự trong cửa sổ dòng lệnh, vẫn đọc phím bằng thư viện chuẩn của
Windows. Giữ nguyên như vậy để dễ đối chiếu với bản C++, và để dành phần
chuyển sang lập trình hướng đối tượng cho giai đoạn sau.

Bảng đối chiếu tên hàm:

    C++              Python
    canMove          can_move
    block2Board      block_to_board
    boardDelBlock    board_del_block
    initBoard        init_board
    draw             draw
    removeLine       (chưa có — phần việc của SV2)

Cách chơi:  a sang trái, d sang phải, x rơi nhanh, q thoát.
Chạy:       python tetris.py
"""

import msvcrt
import os
import random
import time

H = 20
W = 15

# Bảng chơi. board[hàng][cột], viền là dấu '#', ô trống là dấu cách.
board = [[" "] * W for _ in range(H)]

# Vị trí khối đang rơi và chỉ số loại khối, giống x, y, b trong bản C++.
x = 0
y = 0
b = 0

# Bảng các khối, chép đúng từ mảng blocks[][4][4] trong main.cpp.
# Mỗi khối là 4 dòng, mỗi dòng 4 ký tự.
blocks = [
    [" I  ", " I  ", " I  ", " I  "],
    [" I  ", " I  ", " I  ", " I  "],
    ["    ", " OO ", " OO ", "    "],
    ["    ", " OO ", " OO ", "    "],
    ["    ", " OO ", " OO ", "    "],
    ["    ", " OO ", " OO ", "    "],
    ["    ", " OO ", " OO ", "    "],
    ["    ", " OO ", " OO ", "    "],
    ["    ", " OO ", " OO ", "    "],
    ["    ", "IIII", "    ", "    "],
    ["    ", " OO ", " OO ", "    "],
    ["    ", " T  ", "TTT ", "    "],
    ["    ", " SS ", "SS  ", "    "],
    ["    ", "ZZ  ", " ZZ ", "    "],
    ["    ", "J   ", "JJJ ", "    "],
    ["    ", "  L ", "LLL ", "    "],
]


def can_move(dx, dy):
    """Khối có dịch được sang (dx, dy) không. Dịch từ canMove trong C++."""
    for i in range(4):
        for j in range(4):
            if blocks[b][i][j] != " ":
                xt = x + j + dx
                yt = y + i + dy
                if xt < 1 or xt >= W - 1 or yt >= H - 1:
                    return False
                if board[yt][xt] != " ":
                    return False
    return True


def block_to_board():
    """Ghi khối đang rơi vào bảng. Dịch từ block2Board."""
    for i in range(4):
        for j in range(4):
            if blocks[b][i][j] != " ":
                board[y + i][x + j] = blocks[b][i][j]


def board_del_block():
    """Xoá khối đang rơi khỏi bảng. Dịch từ boardDelBlock."""
    for i in range(4):
        for j in range(4):
            if blocks[b][i][j] != " ":
                board[y + i][x + j] = " "


def init_board():
    """Dựng bảng rỗng có viền bao quanh. Dịch từ initBoard."""
    for i in range(H):
        for j in range(W):
            if i == 0 or i == H - 1 or j == 0 or j == W - 1:
                board[i][j] = "#"
            else:
                board[i][j] = " "


def draw():
    """Xoá màn hình rồi in lại toàn bộ bảng. Dịch từ draw."""
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

# TODO(SV4): viết phần xoay khối. Bản C++ chưa có, các phím hiện chỉ có
# a, d, x, q. Gợi ý: thêm một phím xoay, đổi giá trị b sang trạng thái xoay
# tương ứng, và nhớ kiểm tra can_move trước khi nhận nước xoay.

# TODO(SV5): mỗi lần xoá được hàng thì cho khối rơi nhanh hơn. Hiện tốc độ
# đang cố định 0.5 giây một hàng ở cuối hàm main().


def main():
    """Vòng lặp game. Dịch từ hàm main trong C++."""
    global x, y, b

    random.seed()
    x = 5
    y = 0
    b = random.randint(0, 6)
    init_board()

    while True:
        board_del_block()

        if msvcrt.kbhit():
            c = msvcrt.getch().decode("utf-8", errors="ignore")
            if c == "a" and can_move(-1, 0):
                x -= 1
            if c == "d" and can_move(1, 0):
                x += 1
            if c == "x" and can_move(0, 1):
                y += 1
            if c == "q":
                break

        if can_move(0, 1):
            y += 1
        else:
            block_to_board()
            remove_line()
            x = 5
            y = 0
            b = random.randint(0, 6)

        block_to_board()
        draw()
        time.sleep(0.5)


if __name__ == "__main__":
    main()
