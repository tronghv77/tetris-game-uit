"""Lỗi 5: khối vừa sinh ra không xoay được, sáu trên bảy loại dính lỗi.

Khối sinh ra ở y = 0. Nhiều trạng thái xoay có ô nằm ngay hàng 0, mà hàng
0 là hàng viền. Phép thử can_move(0, 0) vì thế trả về False và nước xoay
bị huỷ.

Script dùng thẳng blocks và can_move của tetris.py, không chép lại, nên
kết quả in ra là hành vi thật của game chứ không phải mô phỏng.

Chạy:  python docs/chung-minh-loi/loi5_khong_xoay_duoc.py
"""

import os
import sys

if sys.platform == "win32":
    try:
        import ctypes
        ctypes.windll.kernel32.SetConsoleOutputCP(65001)
    except Exception:
        pass
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# Cho Python thấy tetris.py ở thư mục gốc của dự án
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import tetris  # noqa: E402

# Trạng thái đầu của 7 loại khối, lấy từ tetris.py dòng 498-506
TEN_KHOI = {0: "I", 2: "O", 3: "T", 7: "S", 9: "Z", 11: "J", 15: "L"}


def thu_xoay(trang_thai_dau, dung_wall_kick):
    """Đặt khối ở vị trí sinh ra rồi bấm xoay một lần.

    Trả về True nếu trạng thái khối thực sự đổi, tức là xoay có tác dụng.
    """
    tetris.init_board()
    tetris.b = trang_thai_dau
    tetris.x = 5
    tetris.y = 0

    truoc = tetris.b

    if dung_wall_kick:
        tetris.rotate_block()
    else:
        # Cách làm ban đầu của nhóm: đổi trạng thái rồi chỉ xét tại chỗ
        cu = tetris.b
        tetris.b = tetris.ROTATION_THU[tetris.b]
        if not tetris.can_move(0, 0):
            tetris.b = cu

    return tetris.b != truoc


def lay_bang_xoay():
    """Lấy lại bảng tra xoay từ chính rotate_block, không chép tay."""
    import inspect
    import re

    nguon = inspect.getsource(tetris.rotate_block)
    than = nguon[nguon.index("rotation = {"):nguon.index("old_b")]
    cap = re.findall(r"(\d+)\s*:\s*(\d+)", than)
    return {int(a): int(b) for a, b in cap}


def main():
    tetris.ROTATION_THU = lay_bang_xoay()

    print("Thử bấm phím xoay ngay lúc khối vừa sinh ra, tại x = 5, y = 0.")
    print()
    print("Khối   Không wall kick   Có wall kick")
    print("-" * 44)

    hong = 0
    for trang_thai, ten in TEN_KHOI.items():
        khong = thu_xoay(trang_thai, dung_wall_kick=False)
        co = thu_xoay(trang_thai, dung_wall_kick=True)
        if not khong:
            hong += 1
        print(f"{ten:<6} {'xoay được' if khong else 'KHÔNG xoay':<17} "
              f"{'xoay được' if co else 'KHÔNG xoay'}")

    print()
    print("KẾT QUẢ")
    print("-" * 44)
    print(f"Không có wall kick: {hong} trên {len(TEN_KHOI)} loại khối bấm xoay")
    print("không có tác dụng ở nhịp đầu tiên.")
    print()
    print("Vì sao: khối sinh ra ở y = 0. Trạng thái xoay mới có ô nằm ở hàng")
    print("i = 0 của lưới 4x4, tức là hàng 0 của bảng — hàng viền dấu thăng.")
    print("can_move(0, 0) thấy ô đó không trống nên trả về False.")
    print()
    print("NHÓM XỬ LÝ — tetris.py dòng 387-394")
    print("-" * 44)
    print("Xoay xong mà không lọt thì thử nhích khối một ô rồi xét lại:")
    print("    for dx, dy in ((0, 0), (-1, 0), (1, 0), (0, 1)):")
    print("        if can_move(dx, dy):")
    print("            x += dx; y += dy; return")
    print("    b = old_b")
    print()
    print("Bước (0, 1) nhích xuống một ô là bước gỡ được đúng lỗi này.")
    print("Thử hết bốn cách không lọt thì huỷ nước xoay, trả khối về cũ.")
    print()
    print("Cùng một cái bẫy đã làm hỏng is_game_over() lúc đầu, khi nhóm")
    print("viết can_move(0, 0) thay vì can_move(0, 1). Xem loi4.")


if __name__ == "__main__":
    main()
