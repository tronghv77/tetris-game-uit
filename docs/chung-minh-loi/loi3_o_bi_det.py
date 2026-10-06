"""Lỗi 3: bản gốc in mỗi ô bằng một ký tự nên bảng chơi bị kéo dẹt.

Ký tự trong cửa sổ dòng lệnh không vuông: với phông mặc định của Windows
Console, một ô ký tự rộng 8 điểm ảnh và cao 16 điểm ảnh, tức là cao gấp
đôi chiều rộng.

Script in cùng một bảng theo hai cách để nhìn thấy khác biệt.

Chạy:  python docs/chung-minh-loi/loi3_o_bi_det.py
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

# Phông mặc định của Windows Console
RONG_KY_TU = 8
CAO_KY_TU = 16


def bang_co_khoi():
    b = []
    for i in range(H):
        hang = []
        for j in range(W):
            if i == 0 or i == H - 1 or j == 0 or j == W - 1:
                hang.append("#")
            else:
                hang.append(" ")
        b.append(hang)

    # Một khối O 2x2 để thấy rõ hình vuông bị bóp thành hình gì
    for i, j in ((9, 7), (9, 8), (10, 7), (10, 8)):
        b[i][j] = "O"
    return b


def in_mot_ky_tu(board):
    """Đúng như draw() ở main.cpp dòng 105-110."""
    for hang in board:
        print("".join(hang))


def in_hai_ky_tu(board):
    """Cách nhóm sửa, tetris.py dòng 273-285."""
    for hang in board:
        ra = []
        for o in hang:
            if o == "#":
                ra.append("##")
            elif o == " ":
                ra.append("  ")
            else:
                ra.append("[]")
        print("".join(ra))


def main():
    board = bang_co_khoi()

    print("CÁCH CỦA BẢN GỐC — mỗi ô một ký tự (main.cpp dòng 109)")
    print()
    in_mot_ky_tu(board)

    rong = W * 1 * RONG_KY_TU
    cao = H * CAO_KY_TU
    print()
    print(f"Bảng {W} ô ngang x {H} ô dọc, in một ký tự mỗi ô:")
    print(f"  bề ngang {rong} điểm ảnh, bề cao {cao} điểm ảnh")
    print(f"  tỉ lệ ngang trên dọc = {rong / cao:.2f}")
    print("  Khối O đáng lẽ vuông thì hiện ra dẹt, cao gấp đôi bề ngang.")

    print()
    print("=" * 62)
    print()
    print("CÁCH NHÓM SỬA — mỗi ô hai ký tự (tetris.py dòng 276-281)")
    print()
    in_hai_ky_tu(board)

    rong2 = W * 2 * RONG_KY_TU
    print()
    print(f"Bảng {W} ô ngang x {H} ô dọc, in hai ký tự mỗi ô:")
    print(f"  bề ngang {rong2} điểm ảnh, bề cao {cao} điểm ảnh")
    print(f"  tỉ lệ ngang trên dọc = {rong2 / cao:.2f}")
    print("  Mỗi ô giờ vuông vức, khối O nhìn ra hình vuông.")
    print()
    print("Tỉ lệ đúng phải là {:.2f} vì bảng 15 ô ngang và 20 ô dọc.".format(W / H))
    print("Cách của bản gốc cho {:.2f}, cách sửa cho {:.2f}.".format(rong / cao, rong2 / cao))


if __name__ == "__main__":
    main()
