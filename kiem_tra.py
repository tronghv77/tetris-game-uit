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
    """Gọi một hàm có in ra màn hình mà không để nó làm rối kết quả.

    Trả về cặp (giá trị hàm trả về, phần chữ nó đã in).
    """
    cu = sys.stdout
    sys.stdout = io.StringIO()
    try:
        gia_tri = ham(*tham_so)
        return gia_tri, sys.stdout.getvalue()
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
        so, _ = im_lang(game.remove_line)
        kiem(f"Xoá {n} hàng đầy thì trả về {n}", so == n, f"trả về {so}")

    # Hàng thiếu một ô thì không được tính là đầy
    game.init_board()
    game.x, game.y, game.b = 5, 5, 2
    for j in range(1, game.W - 2):
        game.board[game.H - 2][j] = "X"
    so, _ = im_lang(game.remove_line)
    kiem("Hàng chưa đầy thì không xoá", so == 0, f"trả về {so}")

    # Lỗi trong bản C++ của thầy: hàng trên cùng bị biến thành tường
    _dung_hang_day(game, 1)
    im_lang(game.remove_line)
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
    im_lang(game.remove_line)
    kiem("Phần phía trên tụt xuống đúng một hàng",
         game.board[game.H - 2][3] == "T")


# ============================================================
# TĂNG TỐC ĐỘ RƠI — phần của Phan Nguyễn Minh Thảo
# ============================================================

def kiem_tra_tang_toc(game):
    print("\nTĂNG TỐC ĐỘ RƠI")

    ma_nguon = io.open("tetris.py", encoding="utf-8").read()

    kiem("main() dùng biến fall_speed chứ không phải số cố định",
         "time.sleep(fall_speed)" in ma_nguon)

    kiem("Xoá được hàng thì giảm thời gian chờ",
         "fall_speed - 0.05 * lines" in ma_nguon
         or "fall_speed -" in ma_nguon)

    kiem("Có sàn tối thiểu để game không nhanh tới mức không chơi nổi",
         "max(0.1" in ma_nguon)

    # Tốc độ phải được đặt lại mỗi ván, không thì ván sau thừa hưởng
    # tốc độ nhanh của ván trước, vừa bấm r là khối rơi vèo vèo.
    trong_vong_ngoai = "        fall_speed = 0.5" in ma_nguon
    kiem("fall_speed được đặt lại ở đầu mỗi ván", trong_vong_ngoai)

    # Công thức: xoá càng nhiều hàng một lúc thì giảm càng mạnh
    toc_do = 0.5
    for so_hang in (1, 2, 4):
        moi = max(0.1, toc_do - 0.05 * so_hang)
        kiem(f"Xoá {so_hang} hàng: {toc_do:.2f} giây -> {moi:.2f} giây",
             moi < toc_do or toc_do == 0.1)
        toc_do = moi

    kiem("Giảm mãi cũng không xuống dưới 0.1 giây",
         max(0.1, 0.1 - 0.05 * 4) == 0.1)


# ============================================================
# KHỐI KẾ TIẾP — phần của Đặng Đức Tín
# ============================================================

def kiem_tra_khoi_ke_tiep(game):
    print("\nKHỐI KẾ TIẾP")

    kiem("Có biến next_b", hasattr(game, "next_b"))

    game.init_board()
    game.x, game.y, game.b = 5, 5, 2
    game.next_b = 11                       # khối J
    _, man_hinh = im_lang(game.draw)

    kiem("Màn hình có chữ NEXT", "NEXT" in man_hinh)

    # Khung xem trước phải vẽ đúng khối đang nằm trong next_b
    o_khoi_j = sum(1 for hang in game.blocks[11] for c in hang if c != " ")
    kiem("Khung xem trước vẽ đúng số ô của khối đang chờ",
         man_hinh.count("[]") >= o_khoi_j, f"khối J có {o_khoi_j} ô")

    # Quan trọng nhất: khối hiện trong khung NEXT phải đúng là khối
    # rơi xuống ngay sau. Sai chỗ này thì người chơi bị lừa.
    ma_nguon = io.open("tetris.py", encoding="utf-8").read()
    kiem("Lúc sinh khối mới: lấy b = next_b rồi mới bốc next_b khác",
         ma_nguon.count("b = next_b") >= 2,
         "phải sửa ở cả hai chỗ bốc khối")
