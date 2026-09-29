"""Kiểm tra tự động cho tetris.py.

Chạy trước khi tạo Pull Request, để biết phần mình vừa sửa có làm hỏng
phần của người khác không:

    python kiem_tra.py

Không cần cài thư viện gì thêm. File này không sửa `tetris.py`, chỉ nạp
vào rồi gọi từng hàm và so kết quả với điều mình mong đợi.

Vì sao cần: cả nhóm cùng sửa một file, mà mỗi người chỉ chơi thử phần
của mình. Phần xoay khối của Nguyên từng làm lộ ra một lỗi trong phần
kết thúc game của Trọng, mà tới lúc merge mới biết.
"""

import io
import sys
import types


# ============================================================
# BÀN PHÍM GIẢ LẬP
# ============================================================

# `tetris.py` đọc phím bằng msvcrt, nghĩa là phải có người ngồi bấm.
# Ở đây thay msvcrt bằng một bản giả, nạp sẵn danh sách phím, để máy
# tự "bấm" giúp.

_hang_doi = []      # các phím còn chờ được bấm
_o_dem = []         # phím đang nằm trong bộ đệm bàn phím
_nghi = [False]     # khoảng nghỉ giữa hai lần bấm


def nap_phim(danh_sach):
    """Nạp sẵn các phím sẽ được bấm, ví dụ: nap_phim([b"a", b"w", b"q"])."""
    _hang_doi[:] = list(danh_sach)
    _o_dem.clear()
    _nghi[0] = False


def _kbhit():
    if _nghi[0]:
        _nghi[0] = False
        return False
    if not _o_dem and _hang_doi:
        _o_dem.append(_hang_doi.pop(0))
    return bool(_o_dem)


def _getch():
    if not _o_dem:
        if _hang_doi:
            _o_dem.append(_hang_doi.pop(0))
        else:
            return b"q"     # hết phím thì coi như người chơi bấm thoát
    _nghi[0] = True
    return _o_dem.pop(0)


def nap_game():
    """Nạp tetris.py thành một module riêng, tắt màn hình và độ trễ."""
    gia = types.ModuleType("msvcrt")
    gia.kbhit = _kbhit
    gia.getch = _getch
    sys.modules["msvcrt"] = gia

    ma_nguon = io.open("tetris.py", encoding="utf-8").read()
    game = types.ModuleType("tetris")
    game.__dict__["__name__"] = "tetris"
    exec(compile(ma_nguon, "tetris.py", "exec"), game.__dict__)

    game.time.sleep = lambda *a: None       # khỏi phải chờ thật
    game.os.system = lambda *a: None        # khỏi xoá màn hình
    return game


# Bảy trạng thái khối lúc mới sinh ra, chép từ `first_states` trong main().
KHOI_BAN_DAU = [0, 2, 3, 7, 9, 11, 15]
TEN_KHOI = ["I", "O", "T", "S", "Z", "J", "L"]


# ============================================================
# GHI ĐIỂM
# ============================================================

_ket_qua = []


def kiem(ten, dung, ghi_chu=""):
    """Ghi lại một lần kiểm tra. `dung` là True/False."""
    _ket_qua.append((ten, bool(dung), ghi_chu))


def im_lang(ham, *tham_so):
    """Gọi một hàm có in ra màn hình, nuốt phần in đó, trả về chuỗi đã in."""
    cu = sys.stdout
    sys.stdout = io.StringIO()
    try:
        ham(*tham_so)
        return sys.stdout.getvalue()
    finally:
        sys.stdout = cu


def bao_cao():
    """In kết quả, trả về số phép kiểm tra bị sai."""
    sai = [d for d in _ket_qua if not d[1]]

    for ten, dung, ghi_chu in _ket_qua:
        dau = "  OK " if dung else "  SAI"
        print(f"{dau}  {ten}" + (f"   ({ghi_chu})" if ghi_chu else ""))

    print()
    print(f"  Tổng: {len(_ket_qua)} phép kiểm tra, "
          f"{len(_ket_qua) - len(sai)} đúng, {len(sai)} sai")
    return len(sai)


# ============================================================
# BẢNG CHƠI VÀ CÁC KHỐI
# ============================================================

def kiem_tra_ban_va_khoi(game):
    print("\nBẢNG CHƠI VÀ CÁC KHỐI")

    game.init_board()

    vien_tren = all(o == "#" for o in game.board[0])
    vien_duoi = all(o == "#" for o in game.board[game.H - 1])
    vien_trai = all(game.board[i][0] == "#" for i in range(game.H))
    trong_ruot = all(game.board[i][j] == " "
                     for i in range(1, game.H - 1)
                     for j in range(1, game.W - 1))

    kiem("init_board() dựng đủ bốn viền",
         vien_tren and vien_duoi and vien_trai)
    kiem("init_board() để trống phần ruột", trong_ruot)

    kiem("Đủ 7 loại khối lúc sinh ra", len(KHOI_BAN_DAU) == 7)

    du_loai = []
    for so, ten in zip(KHOI_BAN_DAU, TEN_KHOI):
        o = [c for hang in game.blocks[so] for c in hang if c != " "]
        du_loai.append(bool(o) and o[0] == ten)
    kiem("Mỗi số trong first_states đúng là khối nó nói",
         all(du_loai), "I O T S Z J L")

    # Khối nào cũng phải có đúng 4 ô, vì "tetromino" nghĩa là bốn ô
    du_bon_o = all(
        sum(1 for hang in game.blocks[so] for c in hang if c != " ") == 4
        for so in range(len(game.blocks))
    )
    kiem("Trạng thái nào cũng đúng 4 ô", du_bon_o,
         f"{len(game.blocks)} trạng thái")

    game.init_board()
    game.x, game.y, game.b = 5, 5, 2
    kiem("can_move() cho đi khi phía dưới trống", game.can_move(0, 1))

    game.x = 1
    kiem("can_move() chặn khi đụng viền trái", not game.can_move(-2, 0))

    game.x, game.y = 5, 5
    for j in range(1, game.W - 1):
        game.board[8][j] = "X"
    kiem("can_move() chặn khi đụng khối đã xếp", not game.can_move(0, 3))


# ============================================================
# XOAY KHỐI — phần của Trương Đình Nguyên
# ============================================================

def kiem_tra_xoay(game):
    print("\nXOAY KHỐI")

    # Số trạng thái của mỗi loại: I và O đối xứng nên ít, T J L có đủ 4 hướng
    vong_mong_doi = {"I": 2, "O": 1, "T": 4, "S": 2, "Z": 2, "J": 4, "L": 4}

    for so, ten in zip(KHOI_BAN_DAU, TEN_KHOI):
        game.init_board()
        game.x, game.y, game.b = 5, 5, so

        da_qua = [so]
        for _ in range(8):
            game.rotate_block()
            if game.b == so:
                break
            da_qua.append(game.b)

        kiem(f"Khối {ten} xoay hết {vong_mong_doi[ten]} trạng thái rồi về chỗ cũ",
             len(da_qua) == vong_mong_doi[ten] and game.b == so,
             f"đi qua {len(da_qua)} trạng thái")

    # Xoay sát tường không được phép xuyên qua
    game.init_board()
    game.x, game.y, game.b = 1, 5, 9      # khối Z nằm ngang, sát tường trái
    truoc = game.b
    game.rotate_block()
    hop_le = game.can_move(0, 0)
    kiem("Xoay sát tường: hoặc không xoay, hoặc xoay ra chỗ hợp lệ",
         hop_le, "không xuyên tường")

    # Xoay khi bị khối khác chặn thì phải giữ nguyên
    game.init_board()
    game.x, game.y, game.b = 5, 5, 0      # khối I dựng đứng
    for i in range(game.H - 6, game.H - 1):
        for j in range(1, game.W - 1):
            game.board[i][j] = "X"
    for j in range(1, game.W - 1):
        if j != 6:
            game.board[6][j] = "X"
    truoc = game.b
    game.rotate_block()
    kiem("Bị khối khác chặn thì giữ nguyên trạng thái",
         game.b == truoc or game.can_move(0, 0))


# ============================================================
# XOÁ HÀNG — phần của Vũ Anh Tuấn
# ============================================================

def _dung_hang_day(game, so_hang):
    """Lấp đầy `so_hang` hàng dưới cùng, trả về bảng đã dựng."""
    game.init_board()
    game.x, game.y, game.b = 5, 5, 2
    for k in range(so_hang):
        for j in range(1, game.W - 1):
            game.board[game.H - 2 - k][j] = "X"


def kiem_tra_xoa_hang(game):
    print("\nXOÁ HÀNG")

    for n in (1, 2, 3, 4):
        _dung_hang_day(game, n)
        so = im_lang(game.remove_line) and None
        # gọi lại cho sạch, lần trên chỉ để nuốt phần in ra
        _dung_hang_day(game, n)
        cu = sys.stdout
        sys.stdout = io.StringIO()
        try:
            so = game.remove_line()
        finally:
            sys.stdout = cu
        kiem(f"Xoá {n} hàng đầy thì trả về {n}", so == n, f"trả về {so}")

    # Hàng thiếu một ô thì không được tính là đầy
    game.init_board()
    game.x, game.y, game.b = 5, 5, 2
    for j in range(1, game.W - 2):
        game.board[game.H - 2][j] = "X"
    cu = sys.stdout
    sys.stdout = io.StringIO()
    try:
        so = game.remove_line()
    finally:
        sys.stdout = cu
    kiem("Hàng chưa đầy thì không xoá", so == 0, f"trả về {so}")

    # Lỗi trong bản C++ của thầy: hàng trên cùng bị biến thành tường
    _dung_hang_day(game, 1)
    cu = sys.stdout
    sys.stdout = io.StringIO()
    try:
        game.remove_line()
    finally:
        sys.stdout = cu
    hang_mot = game.board[1]
    kiem("Sau khi xoá, hàng 1 vẫn là hàng trống chứ không thành tường",
         hang_mot[0] == "#" and hang_mot[-1] == "#"
         and all(o == " " for o in hang_mot[1:-1]),
         "lỗi thứ 2 trong main.cpp")

    # Phần trên phải tụt xuống, không được biến mất
    game.init_board()
    game.x, game.y, game.b = 5, 5, 2
    for j in range(1, game.W - 1):
        game.board[game.H - 2][j] = "X"
    game.board[game.H - 3][3] = "T"       # một ô đánh dấu nằm ngay phía trên
    cu = sys.stdout
    sys.stdout = io.StringIO()
    try:
        game.remove_line()
    finally:
        sys.stdout = cu
    kiem("Phần phía trên tụt xuống đúng một hàng",
         game.board[game.H - 2][3] == "T")
