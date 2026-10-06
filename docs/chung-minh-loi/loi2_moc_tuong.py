"""Lỗi 2: removeLine() trong main.cpp biến hàng trên cùng thành tường,
và chính bức tường đó làm hàm kẹt trong vòng lặp vô hạn.

Script chép lại đúng thuật toán removeLine() của bản C++ (main.cpp dòng
111-125) sang Python, cho chạy trên một bảng dựng sẵn, rồi in bảng trước
và sau để thấy bức tường mọc ra.

Vòng lặp trong script có đặt mức chặn 200 lượt, nếu không script sẽ treo
đúng như bản gốc treo.

Chạy:  python docs/chung-minh-loi/loi2_moc_tuong.py
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
MUC_CHAN = 200


def bang_moi():
    """Bảng có viền, giống initBoard() của bản gốc."""
    b = []
    for i in range(H):
        hang = []
        for j in range(W):
            if i == 0 or i == H - 1 or j == 0 or j == W - 1:
                hang.append("#")
            else:
                hang.append(" ")
        b.append(hang)
    return b


def remove_line_ban_goc(board):
    """Dịch nguyên văn removeLine() ở main.cpp dòng 111-125.

        for (i = H-2 ; i > 0 ; i-- ){
            for (j = 0 ; j < W ; j++)
                if (board[i][j] == ' ') break;
            if (j == W){
                for (int ii = i ; ii > 0 ; ii--)
                    for (int jj = 0; jj < W; jj++)
                        board[ii][jj] = board[ii-1][jj];
                i++;
            }
        }

    Chỗ sai nằm ở `ii > 0`: vòng chạy tới ii = 1, tức là chép hàng 0 —
    hàng viền toàn dấu thăng — xuống hàng 1.

    Trả về số lượt đã chạy, và cờ cho biết có bị chặn hay không.
    """
    i = H - 2
    luot = 0
    while i > 0:
        luot += 1
        if luot > MUC_CHAN:
            return luot, True

        day = " " not in board[i]
        if day:
            ii = i
            while ii > 0:
                board[ii] = board[ii - 1][:]
                ii -= 1
            # i++ trong C++ rồi i-- của vòng for triệt tiêu nhau,
            # nên hàng vừa dồn xuống được xét lại
        else:
            i -= 1
    return luot, False


def in_bang(board, nhan):
    print(nhan)
    for i, hang in enumerate(board):
        print(f"  {i:>2} |" + "".join(hang) + "|")
    print()


def main():
    board = bang_moi()

    # Xếp đầy hàng 18 (hàng chơi được sát đáy)
    for j in range(1, W - 1):
        board[18][j] = "T"

    # Đặt vài ô rời ở hàng 17 để thấy nó bị dồn xuống
    board[17][3] = "S"
    board[17][4] = "S"

    in_bang(board, "TRƯỚC khi gọi removeLine() — hàng 18 đã đầy, cần xoá 1 hàng:")

    luot, bi_chan = remove_line_ban_goc(board)

    in_bang(board, f"SAU {luot} lượt chạy thuật toán của bản gốc:")

    tuong = [i for i in range(1, H - 1) if set(board[i]) == {"#"}]

    print("KẾT QUẢ")
    print("-" * 60)
    print("Hàng chơi được giờ toàn dấu thăng:", tuong if tuong else "không có")

    if tuong:
        print()
        print(f"Hàng {tuong[0]} vốn là hàng trống, nay thành một bức tường đặc.")
        print("Nguyên nhân: vòng dồn hàng chạy tới ii = 1 nên chép hàng 0 —")
        print("hàng viền — xuống hàng 1.")

    if bi_chan:
        print()
        print(f"Thuật toán chạy quá {MUC_CHAN} lượt mà không dừng, script phải tự chặn.")
        print()
        print("Vì sao không dừng: bức tường ở hàng 1 không còn ô trống nào,")
        print("nên lần xét sau thuật toán coi đó là một hàng đầy và xoá tiếp.")
        print("Xoá xong lại chép hàng 0 xuống, hàng 1 lại thành tường. Lặp mãi.")
        print()
        print("Nghĩa là bản C++ không chỉ mọc thêm tường — nó TREO ngay ở")
        print("lần xoá hàng đầu tiên. Trong game thật, màn hình nhấp nháy")
        print("liên tục vì mỗi lượt đều gọi draw() và _sleep(200).")

    print()
    print("NHÓM XỬ LÝ — tetris.py dòng 301-304")
    print("-" * 60)
    print("Vòng dồn hàng dừng ở hàng 2, không chạm hàng 1:")
    print("    for ii in range(i, 1, -1):")
    print("        board[ii] = board[ii - 1][:]")
    print("rồi dựng lại hàng 1 thành hàng trống có viền hai bên:")
    print('    board[1] = ["#"] + [" "] * (W - 2) + ["#"]')
    print()
    print("Hàng 1 luôn có ô trống nên không bao giờ bị coi là hàng đầy,")
    print("vòng lặp kết thúc bình thường.")


if __name__ == "__main__":
    main()
