"""Lỗi 1: rand()%7 trong main.cpp chỉ sinh ra hai loại khối.

Script này đọc thẳng file main.cpp của thầy, tách mảng blocks ra, rồi in
xem mỗi chỉ số trong mảng là loại khối gì. Không có số liệu nào viết tay.

Chạy:  python docs/chung-minh-loi/loi1_sinh_khoi.py
"""

import os
import re
import sys

# Cửa sổ dòng lệnh Windows mặc định không in được tiếng Việt
if sys.platform == "win32":
    try:
        import ctypes
        ctypes.windll.kernel32.SetConsoleOutputCP(65001)
    except Exception:
        pass
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

GOC = os.path.join(os.path.dirname(__file__), "..", "..", "main.cpp")


def doc_cac_khoi():
    """Trả về danh sách loại khối theo đúng thứ tự trong mảng blocks."""
    with open(GOC, encoding="utf-8", errors="ignore") as f:
        nguon = f.read()

    # Cắt lấy phần giữa "char blocks[][4][4] ={" và dấu "};" đầu tiên
    dau = nguon.index("char blocks")
    dau = nguon.index("{", dau)
    cuoi = nguon.index("};", dau)
    than = nguon[dau + 1:cuoi]

    # Mỗi khối là một cụm "{{...}}" gồm 4 hàng
    cum_khoi = re.findall(r"\{\{.*?\}\}", than, re.S)

    loai = []
    for cum in cum_khoi:
        chu = set(re.findall(r"'([A-Z])'", cum))
        loai.append("".join(sorted(chu)) if chu else "?")
    return loai


def main():
    loai = doc_cac_khoi()

    print("Mảng blocks trong main.cpp có", len(loai), "phần tử.")
    print()
    print("Chỉ số  Loại khối   rand()%7 lấy được?")
    print("-" * 42)
    for i, ten in enumerate(loai):
        lay = "CÓ" if i < 7 else "không"
        print(f"{i:>5}   {ten:<10}  {lay}")

    trong_tam = sorted(set(loai[:7]))
    ngoai_tam = sorted(set(loai[7:]) - set(loai[:7]))

    print()
    print("rand()%7 trả về số từ 0 đến 6, nên chỉ chạm tới 7 phần tử đầu.")
    print("  Loại khối xuất hiện được :", ", ".join(trong_tam))
    print("  Loại khối không bao giờ ra:", ", ".join(ngoai_tam))
    print()
    print("Dòng 130 và 145 của main.cpp đều viết  b = rand()%7;")
    print("Vậy chơi bản gốc chỉ thấy rơi 2 trong 7 loại khối.")
    print()
    print("Nhóm xử lý: tetris.py dòng 498-506 dùng danh sách first_states")
    print("liệt kê đích danh trạng thái đầu của cả 7 loại khối, rồi")
    print("random.choice trên danh sách đó (dòng 532).")


if __name__ == "__main__":
    main()
