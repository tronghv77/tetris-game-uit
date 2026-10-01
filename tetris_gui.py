"""Tetris — bản giao diện đồ hoạ.

Chạy:

    python tetris_gui.py

Dùng tkinter, có sẵn trong Python nên không phải cài thêm thư viện nào.

File này **chỉ lo phần hiển thị và điều khiển**. Toàn bộ luật chơi vẫn nằm
trong `tetris.py` và được gọi sang: bảng khối, `can_move()`, `rotate_block()`,
`init_board()`, `is_game_over()`. Làm vậy để hai bản không bao giờ lệch nhau:
sửa luật ở `tetris.py` là cả hai cùng đổi theo.

Bản dòng lệnh vẫn chạy bình thường bằng `python tetris.py`, file này không
sửa gì trong đó.
"""

import json
import os
import tkinter as tk
from datetime import datetime
from tkinter import font as tkfont

import tetris


# ============================================================
# MÀU SẮC VÀ KÍCH THƯỚC
# ============================================================

# Mỗi loại khối một màu, theo bảng màu quen thuộc của Tetris hiện đại
MAU_KHOI = {
    "I": "#22d3ee",
    "O": "#facc15",
    "T": "#a855f7",
    "S": "#22c55e",
    "Z": "#ef4444",
    "J": "#3b82f6",
    "L": "#f97316",
}

NEN = "#0b0d12"          # nền cửa sổ
NEN_BANG = "#11141c"     # nền bảng chơi
NEN_THE = "#161b26"      # nền các thẻ bên phải
VIEN = "#232a39"         # đường kẻ ô và viền thẻ
CHU = "#e8ebf2"          # chữ chính
CHU_MO = "#737d94"       # chữ phụ
NHAN = "#22d3ee"         # màu nhấn
VANG = "#facc15"         # màu cho kỷ lục mới

O = 30                   # cạnh một ô, tính bằng điểm ảnh
LE = 18                  # khoảng chừa quanh bảng
CAO_NUT = 150            # chiều cao bảng nút bấm phía dưới

NEN_NUT = "#1a2030"      # nền nút
NUT_RE = "#232c42"       # nền nút khi rê chuột lên
NUT_BAM = "#12161f"      # nền nút lúc đang bấm
NUT_CHINH = "#0e7490"    # nền nút Thả thẳng
NUT_CHINH_RE = "#0891b2"

# Vùng chơi thật, không tính viền '#' của bảng trong tetris.py
HANG = tetris.H - 2
COT = tetris.W - 2

RONG_BANG = COT * O
CAO_BANG = HANG * O
RONG_PANEL = 230

# Bảy trạng thái khối lúc mới sinh, lấy từ `first_states` trong tetris.py
KHOI_BAN_DAU = [0, 2, 3, 7, 9, 11, 15]

# Xoá 1 hàng 100 điểm, 2 hàng 300, 3 hàng 500, 4 hàng 800. Nhân với cấp độ.
DIEM = {1: 100, 2: 300, 3: 500, 4: 800}

CAP_TOI_DA = 10
FILE_DIEM_CAO = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             "diem_cao.json")


# ============================================================
# BẢNG ĐIỂM CAO
# ============================================================

def doc_diem_cao():
    """Đọc bảng điểm cao.

    File hỏng hay chưa có thì coi như bảng rỗng. Không vì một file điểm
    lỗi mà làm cả game không mở được.
    """
    try:
        with open(FILE_DIEM_CAO, encoding="utf-8") as f:
            bang = json.load(f)
        if isinstance(bang, list):
            return [d for d in bang
                    if isinstance(d, dict) and "diem" in d][:10]
    except (OSError, ValueError):
        pass
    return []


def luu_diem_cao(bang):
    try:
        with open(FILE_DIEM_CAO, "w", encoding="utf-8") as f:
            json.dump(bang[:10], f, ensure_ascii=False, indent=2)
    except OSError:
        pass            # ghi khong duoc thi thoi, van choi van xong binh thuong


def them_diem(diem, hang, cap):
    """Thêm một kết quả. Trả về thứ hạng, hoặc None nếu không lọt top 10."""
    bang = doc_diem_cao()
    moi = {"diem": diem, "hang": hang, "cap": cap,
           "ngay": datetime.now().strftime("%d/%m/%Y")}
    bang.append(moi)
    bang.sort(key=lambda d: d["diem"], reverse=True)
    bang = bang[:10]
    luu_diem_cao(bang)

    for i, d in enumerate(bang):
        if d is moi:
            return i + 1
    return None

# Thời gian rơi một hàng, tính bằng mili giây, theo từng cấp
def nhip_roi(cap):
    """Cấp càng cao khối rơi càng nhanh, nhưng không nhanh quá mức chơi nổi."""
    return max(90, 600 - (cap - 1) * 55)


# ============================================================
# VẼ MỘT Ô
# ============================================================

def to_mau(mau, do_sang):
    """Pha màu với trắng hoặc đen để lấy sắc độ sáng hơn hoặc tối hơn."""
    r = int(mau[1:3], 16)
    g = int(mau[3:5], 16)
    b = int(mau[5:7], 16)

    if do_sang > 0:
        r = int(r + (255 - r) * do_sang)
        g = int(g + (255 - g) * do_sang)
        b = int(b + (255 - b) * do_sang)
    else:
        r = int(r * (1 + do_sang))
        g = int(g * (1 + do_sang))
        b = int(b * (1 + do_sang))

    return f"#{r:02x}{g:02x}{b:02x}"


def bo_tron(canvas, x0, y0, x1, y1, r, **kw):
    """Vẽ hình chữ nhật bo góc. Canvas của tkinter không có sẵn hình này."""
    diem = [
        x0 + r, y0, x1 - r, y0, x1, y0, x1, y0 + r,
        x1, y1 - r, x1, y1, x1 - r, y1, x0 + r, y1,
        x0, y1, x0, y1 - r, x0, y0 + r, x0, y0,
    ]
    return canvas.create_polygon(diem, smooth=True, **kw)


class Nut:
    """Một nút bấm vẽ bằng tay trên canvas.

    Nút mặc định của tkinter trên Windows trông cũ và không đổi màu nền
    được, nên tự vẽ. Nút tự sáng lên khi rê chuột, lõm xuống khi bấm.

    `lap=True` thì giữ chuột sẽ lặp lại thao tác, dùng cho các nút dịch
    chuyển và rơi nhanh.
    """

    def __init__(self, canvas, x, y, rong, cao, bieu_tuong, nhan, ham,
                 lap=False, chinh=False, nhan_dong=None, co_chu=None):
        self.canvas = canvas
        self.x, self.y = x, y
        self.rong, self.cao = rong, cao
        self.bieu_tuong = bieu_tuong
        self.nhan = nhan
        self.ham = ham
        self.lap = lap
        self.chinh = chinh
        self.nhan_dong = nhan_dong        # hàm trả về nhãn, cho nút đổi chữ
        self.co_chu = co_chu              # cỡ chữ của biểu tượng

        self.the = f"nut{id(self)}"
        self.dang_re = False
        self.dang_bam = False
        self.hen = None
        self.doi_hien = 0

        self._tao_hinh()
        self._gan_su_kien()

    def _mau_nen(self):
        if self.dang_bam:
            return NUT_BAM
        if self.chinh:
            return NUT_CHINH_RE if self.dang_re else NUT_CHINH
        return NUT_RE if self.dang_re else NEN_NUT

    def _tao_hinh(self):
        """Tạo các hình của nút đúng một lần. Về sau chỉ đổi màu và chữ."""
        x0, y0 = self.x, self.y
        x1, y1 = x0 + self.rong, y0 + self.cao
        giua = x0 + self.rong / 2

        self.id_nen = bo_tron(
            self.canvas, x0, y0, x1, y1, 10,
            fill=self._mau_nen(),
            outline=NHAN if self.chinh else VIEN,
            width=1, tags=self.the)

        nhan = self.nhan_dong() if self.nhan_dong else self.nhan
        co = self.co_chu or 15
        if nhan:
            self.id_bieu_tuong = self.canvas.create_text(
                giua, y0 + self.cao * 0.36, text=self.bieu_tuong,
                fill=CHU, font=("Segoe UI Symbol", co), tags=self.the)
            self.id_nhan = self.canvas.create_text(
                giua, y0 + self.cao * 0.74, text=nhan,
                fill=CHU if self.chinh else CHU_MO,
                font=("Segoe UI", 8, "bold"), tags=self.the)
        else:
            self.id_bieu_tuong = self.canvas.create_text(
                giua, y0 + self.cao / 2, text=self.bieu_tuong,
                fill=CHU, font=("Segoe UI Symbol", co + 2), tags=self.the)
            self.id_nhan = None

    def ve(self):
        """Cập nhật màu và chữ của nút.

        Cố ý **không** xoá rồi vẽ lại các hình. Xoá một hình ngay trong lúc
        chính nó đang xử lý sự kiện chuột sẽ làm Tk mất luôn sự kiện nhả
        chuột: nút cứ tưởng mình còn bị giữ nên lặp thao tác mãi, mà mỗi
        lần bấm lại đẻ thêm một chuỗi lặp nữa. Đó là lý do cửa sổ từng
        chiếm trọn một nhân CPU rồi đơ.
        """
        self.canvas.itemconfig(self.id_nen, fill=self._mau_nen())

        if self.id_nhan is not None and self.nhan_dong:
            self.canvas.itemconfig(self.id_nhan, text=self.nhan_dong())

        self._dat_do_lun(1 if self.dang_bam else 0)

    def _dat_do_lun(self, muc):
        """Nút lún xuống 1 điểm ảnh khi bấm, nhô lại khi nhả."""
        if muc == self.doi_hien:
            return
        buoc = muc - self.doi_hien
        for hinh in (self.id_nen, self.id_bieu_tuong, self.id_nhan):
            if hinh is not None:
                self.canvas.move(hinh, 0, buoc)
        self.doi_hien = muc

    def _gan_su_kien(self):
        self.canvas.tag_bind(self.the, "<Enter>", self._vao)
        self.canvas.tag_bind(self.the, "<Leave>", self._ra)
        self.canvas.tag_bind(self.the, "<ButtonPress-1>", self._bam)
        self.canvas.tag_bind(self.the, "<ButtonRelease-1>", self._tha)

    def _vao(self, _=None):
        self.dang_re = True
        self.canvas.config(cursor="hand2")
        self.ve()

    def _ra(self, _=None):
        self.dang_re = False
        self.dang_bam = False
        self.canvas.config(cursor="")
        self._dung_lap()
        self.ve()

    def _bam(self, _=None):
        self._dung_lap()            # huỷ chuỗi lặp cũ nếu còn sót
        self.dang_bam = True
        self.ve()
        self.ham()
        if self.lap:
            self.hen = self.canvas.after(260, self._lap_lai)

    def _lap_lai(self):
        self.hen = None
        if not self.dang_bam:
            return
        self.ham()
        self.hen = self.canvas.after(70, self._lap_lai)

    def _tha(self, _=None):
        self.dang_bam = False
        self._dung_lap()
        self.ve()

    def _dung_lap(self):
        if self.hen:
            self.canvas.after_cancel(self.hen)
            self.hen = None


class Game:
    """Cửa sổ game: vẽ, nhận phím, và giữ trạng thái một ván."""

    def __init__(self, root):
        self.root = root
        self.root.title("TETRIS  —  Nhóm 07, UIT")
        self.root.configure(bg=NEN)
        self.root.resizable(False, False)

        # Hai cờ này phải có trước khi dựng nút, vì nút Tạm dừng đọc
        # `dang_dung` ngay lúc vẽ lần đầu
        self.man = "menu"
        self.cap_bat_dau = 1

        self.dang_dung = False
        self.da_thua = False
        self.dang_xoa = None
        self.hen_gio = None
        self.hen_dem = None
        self.dem_con = 0
        self.hang_moi = None        # thu hang vua dat, neu lot bang diem cao

        self.diem = 0
        self.so_hang = 0
        self.cap = 1
        self.khoi_sau = KHOI_BAN_DAU[0]

        self._dung_font()
        self._dung_giao_dien()
        self._dung_phim()

        self._doi_man("menu")

    # --------------------------------------------------------
    # Dựng giao diện
    # --------------------------------------------------------

    def _dung_font(self):
        self.f_tieu_de = tkfont.Font(family="Segoe UI", size=22, weight="bold")
        self.f_nhan = tkfont.Font(family="Segoe UI", size=9, weight="bold")
        self.f_so = tkfont.Font(family="Consolas", size=20, weight="bold")
        self.f_phim = tkfont.Font(family="Consolas", size=9)
        self.f_lon = tkfont.Font(family="Segoe UI", size=26, weight="bold")
        self.f_vua = tkfont.Font(family="Segoe UI", size=11)
        self.f_ten = tkfont.Font(family="Segoe UI", size=44, weight="bold")
        self.f_dem = tkfont.Font(family="Segoe UI", size=72, weight="bold")
        self.f_bang = tkfont.Font(family="Consolas", size=11)

    def _dung_giao_dien(self):
        rong = LE * 3 + RONG_BANG + RONG_PANEL
        cao = LE * 2 + CAO_BANG

        self.canvas = tk.Canvas(
            self.root,
            width=rong,
            height=cao,
            bg=NEN,
            highlightthickness=0,
        )
        self.canvas.pack()

        # Bảng nút nằm trên canvas riêng, vẽ một lần rồi thôi. Canvas chính
        # bị xoá sạch mỗi khung hình nên không đặt nút lên đó được.
        self.bang_nut = tk.Canvas(
            self.root,
            width=rong,
            height=CAO_NUT,
            bg=NEN,
            highlightthickness=0,
        )
        self.bang_nut.pack()

        self.rong_cua_so = rong
        self.cao_canvas = cao
        self.x_bang = LE
        self.y_bang = LE
        self.x_panel = LE * 2 + RONG_BANG
        self.nut = []

        # Nha chuot o bat ky dau cung thoi lap, phong khi su kien nha
        # khong toi duoc dung nut.
        self.root.bind("<ButtonRelease-1>", self._tha_het_nut, add="+")

    def _dung_phim(self):
        # Nhận cả phím mũi tên lẫn bộ phím của bản dòng lệnh, cho ai quen tay nào
        gan = {
            "<Left>": lambda e: self.dich(-1),
            "<Right>": lambda e: self.dich(1),
            "<Down>": lambda e: self.roi_mot_hang(),
            "<Up>": lambda e: self.xoay(False),
            "<space>": lambda e: self._phim_cach(),
            "<Return>": lambda e: self._phim_cach(),
            "a": lambda e: self.dich(-1),
            "d": lambda e: self.dich(1),
            "x": lambda e: self.roi_mot_hang(),
            "w": lambda e: self.xoay(False),
            "s": lambda e: self.xoay(True),
            "p": lambda e: self.tam_dung(),
            "r": lambda e: self._phim_r(),
            "q": lambda e: self._phim_q(),
            "<Escape>": lambda e: self._phim_q(),
        }
        for phim, ham in gan.items():
            self.root.bind(phim, ham)
            if len(phim) == 1:
                self.root.bind(phim.upper(), ham)

    def _phim_cach(self):
        """Phím cách và Enter: ở menu là bắt đầu, trong ván là thả thẳng."""
        if self.man == "menu":
            self.bat_dau()
        elif self.man == "choi":
            if self.dang_dung:
                self.tam_dung()
            else:
                self.tha_thang()
        elif self.man == "thua":
            self.bat_dau()
        elif self.man in ("huong_dan", "diem_cao"):
            self.sang_man("menu")

    def _phim_r(self):
        if self.man in ("choi", "thua"):
            self.bat_dau()

    def _phim_q(self):
        """Thoát dần: đang trong game thì về menu, ở menu mới đóng cửa sổ."""
        if self.man in ("choi", "thua", "huong_dan", "diem_cao"):
            self.sang_man("menu")
        else:
            self.root.destroy()

    def _vach(self):
        self.bang_nut.create_line(LE, 2, self.rong_cua_so - LE, 2, fill=VIEN)

    def _nut_menu(self):
        self._vach()
        x, y, cao = LE, 20, 60

        self.nut.append(Nut(self.bang_nut, x, y, 168, cao, "▶",
                            "BẮT ĐẦU CHƠI", self.bat_dau, chinh=True,
                            co_chu=17))
        x += 178

        self.nut.append(Nut(self.bang_nut, x, y, 50, cao, "◀", "",
                            lambda: self.doi_cap(-1), co_chu=13))
        x += 56
        self.bang_nut.create_text(x + 36, y + cao / 2 - 12,
                                  text="CẤP BẮT ĐẦU", fill=CHU_MO,
                                  font=self.f_nhan)
        self.id_cap_so = self.bang_nut.create_text(
            x + 36, y + cao / 2 + 12, text=str(self.cap_bat_dau),
            fill=NHAN, font=self.f_so)
        x += 82
        self.nut.append(Nut(self.bang_nut, x, y, 50, cao, "▶", "",
                            lambda: self.doi_cap(1), co_chu=13))
        x += 62

        self.nut.append(Nut(self.bang_nut, x, y, 118, cao, "?",
                            "HƯỚNG DẪN",
                            lambda: self.sang_man("huong_dan")))
        x += 126
        self.nut.append(Nut(self.bang_nut, x, y, 118, cao, "★",
                            "ĐIỂM CAO",
                            lambda: self.sang_man("diem_cao")))

        self.bang_nut.create_text(
            LE, y + cao + 20, anchor="nw", fill=CHU_MO, font=self.f_phim,
            text="Phím cách hoặc Enter để bắt đầu        Q để thoát")

    def _nut_quay_lai(self):
        self._vach()
        self.nut.append(Nut(self.bang_nut, LE, 20, 210, 60, "←",
                            "VỀ MENU CHÍNH",
                            lambda: self.sang_man("menu"),
                            chinh=True, co_chu=17))
        self.bang_nut.create_text(
            LE + 230, 50, anchor="w", fill=CHU_MO, font=self.f_phim,
            text="Phím cách, Enter hoặc Q cũng về menu")

    def _nut_thua(self):
        self._vach()
        x, y, cao = LE, 20, 60

        self.nut.append(Nut(self.bang_nut, x, y, 184, cao, "↻",
                            "CHƠI VÁN MỚI", self.bat_dau, chinh=True,
                            co_chu=17))
        x += 196
        self.nut.append(Nut(self.bang_nut, x, y, 160, cao, "★",
                            "XEM ĐIỂM CAO",
                            lambda: self.sang_man("diem_cao")))
        x += 172
        self.nut.append(Nut(self.bang_nut, x, y, 160, cao, "←",
                            "VỀ MENU CHÍNH",
                            lambda: self.sang_man("menu")))

    def _nut_choi(self):
        """Bộ nút của màn đang chơi."""
        self._vach()

        # Hàng trên: dịch chuyển và xoay
        x = LE
        y = 16
        cao = 58
        for bieu_tuong, nhan, ham, lap in (
            ("◀", "TRÁI", lambda: self.dich(-1), True),
            ("▼", "XUỐNG", self.roi_mot_hang, True),
            ("▶", "PHẢI", lambda: self.dich(1), True),
            ("▲", "XOAY", lambda: self.xoay(False), False),
            ("↺", "NGƯỢC", lambda: self.xoay(True), False),
        ):
            self.nut.append(
                Nut(self.bang_nut, x, y, 74, cao, bieu_tuong, nhan,
                    ham, lap=lap))
            x += 82

        # Hàng dưới: thả thẳng, tạm dừng, chơi lại, thoát
        x = LE
        y = 84
        cao = 48

        self.nut.append(
            Nut(self.bang_nut, x, y, 156, cao, "⇓", "THẢ THẲNG XUỐNG",
                self.tha_thang, chinh=True))
        x += 164

        self.nut.append(
            Nut(self.bang_nut, x, y, 124, cao, "❚❚", "TẠM DỪNG",
                self.tam_dung,
                nhan_dong=lambda: ("CHƠI TIẾP" if self.dang_dung
                                   else "TẠM DỪNG")))
        x += 132

        self.nut.append(
            Nut(self.bang_nut, x, y, 124, cao, "↻", "CHƠI LẠI",
                self.bat_dau))
        x += 132

        self.nut.append(
            Nut(self.bang_nut, x, y, 100, cao, "←", "VỀ MENU",
                lambda: self.sang_man("menu")))

    # --------------------------------------------------------
    # Một ván chơi
    # --------------------------------------------------------

    def sang_man(self, ten):
        """Đổi màn sau khi Tk xử lý xong sự kiện hiện tại.

        Phải hoãn lại: đổi màn sẽ xoá sạch các nút, mà lệnh đổi màn
        thường phát ra từ chính một nút đang xử lý cú bấm của nó. Xoá
        hình ngay giữa lúc nó đang phát sự kiện là điều đã từng làm
        cửa sổ đơ.
        """
        self.root.after_idle(lambda: self._doi_man(ten))

    def _doi_man(self, ten):
        self._dung_het_hen()
        self.man = ten

        for nut in self.nut:
            nut._dung_lap()
        self.nut = []
        self.bang_nut.delete("all")

        {
            "menu": self._nut_menu,
            "huong_dan": self._nut_quay_lai,
            "diem_cao": self._nut_quay_lai,
            "choi": self._nut_choi,
            "thua": self._nut_thua,
        }.get(ten, lambda: None)()

        self.ve()

    def _dung_het_hen(self):
        for ten in ("hen_gio", "hen_dem"):
            h = getattr(self, ten, None)
            if h:
                try:
                    self.root.after_cancel(h)
                except Exception:
                    pass
                setattr(self, ten, None)

    def doi_cap(self, buoc):
        self.cap_bat_dau = max(1, min(CAP_TOI_DA, self.cap_bat_dau + buoc))
        self.bang_nut.itemconfig(self.id_cap_so, text=str(self.cap_bat_dau))

    def bat_dau(self):
        """Dựng ván mới rồi vào màn đếm ngược."""
        tetris.init_board()

        self.diem = 0
        self.so_hang = 0
        self.cap = self.cap_bat_dau
        self.dang_dung = False
        self.da_thua = False
        self.dang_xoa = None
        self.hang_moi = None

        self.khoi_sau = tetris.random.choice(KHOI_BAN_DAU)
        self.sinh_khoi()

        self.dem_con = 3

        # Phai doi man qua sang_man: lenh bat dau thuong phat ra tu mot nut
        # dang xu ly cu bam, ma doi man se xoa sach cac nut do.
        self.sang_man("dem_nguoc")
        self.root.after_idle(self._nhip_dem)

    def _nhip_dem(self):
        self.hen_dem = None
        if self.man != "dem_nguoc":
            return
        self.ve()
        if self.dem_con <= 0:
            self._doi_man("choi")
            self.hen_nhip()
            return
        self.dem_con -= 1
        self.hen_dem = self.root.after(700, self._nhip_dem)

    def thua(self):
        self.da_thua = True
        self._dung_het_hen()
        self.hang_moi = them_diem(self.diem, self.so_hang, self.cap)
        self.sang_man("thua")

    def sinh_khoi(self):
        tetris.b = self.khoi_sau
        self.khoi_sau = tetris.random.choice(KHOI_BAN_DAU)

        tetris.x = tetris.W // 2 - 2
        tetris.y = 1 - self._hang_tren_cung(tetris.b)

        # Khối mới không có chỗ đứng nghĩa là bảng đã đầy tới đỉnh
        if not tetris.can_move(0, 0):
            self.thua()

    @staticmethod
    def _hang_tren_cung(so):
        """Hàng đầu tiên có ô trong lưới 4x4 của một trạng thái khối.

        Bản dòng lệnh thả khối từ `y = 0`, nên khối I, T, J, L có ô nằm đè
        lên hàng viền trên cùng. Hậu quả là mọi phép `can_move` ở nhịp đầu
        đều trả về sai: bấm sang trái hay xoay đều không ăn.

        Ở đây đặt khối sao cho hàng trên cùng của nó nằm đúng hàng 1, tức
        là vừa lọt vào trong bảng. Từ nhịp đầu tiên người chơi đã điều
        khiển được.
        """
        for i in range(4):
            if any(o != " " for o in tetris.blocks[so][i]):
                return i
        return 0

    def hen_nhip(self):
        if self.hen_gio:
            self.root.after_cancel(self.hen_gio)
        self.hen_gio = self.root.after(nhip_roi(self.cap), self.nhip)

    def nhip(self):
        self.hen_gio = None
        if self.man != "choi":
            return
        if not (self.dang_dung or self.da_thua or self.dang_xoa):
            if tetris.can_move(0, 1):
                tetris.y += 1
            else:
                self.dat_khoi()
            self.ve()
        self.hen_nhip()

    # --------------------------------------------------------
    # Thao tác của người chơi
    # --------------------------------------------------------

    def _choi_duoc(self):
        return (self.man == "choi" and not self.dang_dung
                and not self.da_thua and not self.dang_xoa)

    def dich(self, dx):
        if self._choi_duoc() and tetris.can_move(dx, 0):
            tetris.x += dx
            self.ve()

    def roi_mot_hang(self):
        if self._choi_duoc() and tetris.can_move(0, 1):
            tetris.y += 1
            self.ve()

    def xoay(self, nguoc):
        if self._choi_duoc():
            tetris.rotate_block(nguoc=nguoc)
            self.ve()

    def tha_thang(self):
        """Thả khối rơi thẳng xuống đáy, cộng điểm theo số hàng đã rơi."""
        if not self._choi_duoc():
            return

        roi = 0
        while tetris.can_move(0, 1):
            tetris.y += 1
            roi += 1

        self.diem += roi * 2
        self.dat_khoi()
        self.ve()

    def tam_dung(self):
        if self.man == "choi" and not self.da_thua:
            self.dang_dung = not self.dang_dung
            self._ve_lai_nut()
            self.ve()

    def _tha_het_nut(self, _=None):
        for nut in getattr(self, "nut", []):
            if nut.dang_bam:
                nut._tha()

    def _ve_lai_nut(self):
        """Vẽ lại những nút có chữ thay đổi theo trạng thái ván chơi."""
        for nut in getattr(self, "nut", []):
            if nut.nhan_dong:
                nut.ve()

    # --------------------------------------------------------
    # Cố định khối và xoá hàng
    # --------------------------------------------------------

    def dat_khoi(self):
        tetris.block_to_board()

        day = self.tim_hang_day()
        if not day:
            self.sinh_khoi()
            return

        # Cho hàng đầy nháy trắng một nhịp rồi mới sập xuống. Phải hẹn giờ
        # chứ không được chờ tại chỗ: gọi root.update() ngay trong một
        # callback của Tk sẽ khiến hàm này tự chạy lồng vào chính nó và
        # treo cả cửa sổ.
        self.dang_xoa = day
        self.ve()
        self.root.after(110, self._xong_nhay)

    def _xong_nhay(self):
        day = self.dang_xoa
        self.dang_xoa = None

        if day:
            self.xoa_hang(day)
        if not self.da_thua:
            self.sinh_khoi()
        self.ve()

    def tim_hang_day(self):
        """Trả về danh sách chỉ số các hàng đã được lấp kín."""
        return [
            i for i in range(1, tetris.H - 1)
            if " " not in tetris.board[i]
        ]

    def xoa_hang(self, day):
        so = len(day)
        self.so_hang += so
        self.diem += DIEM.get(so, 800 + (so - 4) * 200) * self.cap

        # Cứ mười hàng thì lên một cấp, khối rơi nhanh hơn
        cap_moi = min(CAP_TOI_DA, self.cap_bat_dau + self.so_hang // 10)
        if cap_moi != self.cap:
            self.cap = cap_moi
            self.hen_nhip()

        for i in sorted(day):
            del tetris.board[i]
            tetris.board.insert(1, ["#"] + [" "] * (tetris.W - 2) + ["#"])

    # --------------------------------------------------------
    # Vẽ
    # --------------------------------------------------------

    def ve(self):
        self.canvas.delete("all")
        {
            "menu": self._ve_menu,
            "huong_dan": self._ve_huong_dan,
            "diem_cao": self._ve_diem_cao,
            "dem_nguoc": self._ve_dem_nguoc,
            "choi": self._ve_man_choi,
            "thua": self._ve_man_choi,
        }.get(self.man, lambda: None)()

    def _ve_man_choi(self):
        self._ve_nen_bang()
        self._ve_bong()
        self._ve_cac_o_da_xep(self.dang_xoa or [])
        self._ve_khoi_dang_roi()
        self._ve_panel()

        if self.da_thua:
            self._phu_thua()
        elif self.dang_dung:
            self._phu("TẠM DỪNG", "",
                      "P hoặc nút Chơi tiếp để vào lại ván")

    def _toa_do(self, cot, hang):
        """Đổi vị trí ô trên bảng của tetris.py sang toạ độ điểm ảnh."""
        return (
            self.x_bang + (cot - 1) * O,
            self.y_bang + (hang - 1) * O,
        )

    def _ve_nen_bang(self):
        self.canvas.create_rectangle(
            self.x_bang - 2, self.y_bang - 2,
            self.x_bang + RONG_BANG + 2, self.y_bang + CAO_BANG + 2,
            fill=NEN_BANG, outline=VIEN, width=2,
        )

        for c in range(1, COT):
            x = self.x_bang + c * O
            self.canvas.create_line(x, self.y_bang, x,
                                    self.y_bang + CAO_BANG, fill="#161a24")
        for h in range(1, HANG):
            y = self.y_bang + h * O
            self.canvas.create_line(self.x_bang, y,
                                    self.x_bang + RONG_BANG, y, fill="#161a24")

    def _ve_o(self, x, y, mau, canh=O):
        """Một ô có vát sáng ở trên và vát tối ở dưới, nhìn nổi khối lên."""
        d = canh
        self.canvas.create_rectangle(x, y, x + d, y + d,
                                     fill=to_mau(mau, -0.45), outline="")
        self.canvas.create_rectangle(x + 2, y + 2, x + d - 2, y + d - 2,
                                     fill=mau, outline="")
        self.canvas.create_polygon(
            x + 2, y + 2, x + d - 2, y + 2, x + d - 5, y + 5, x + 5, y + 5,
            fill=to_mau(mau, 0.35), outline="",
        )
        self.canvas.create_polygon(
            x + 2, y + 2, x + 5, y + 5, x + 5, y + d - 5, x + 2, y + d - 2,
            fill=to_mau(mau, 0.18), outline="",
        )

    def _ve_cac_o_da_xep(self, nhay):
        for hang in range(1, tetris.H - 1):
            for cot in range(1, tetris.W - 1):
                ky_tu = tetris.board[hang][cot]
                if ky_tu == " ":
                    continue

                x, y = self._toa_do(cot, hang)
                if hang in nhay:
                    self.canvas.create_rectangle(x, y, x + O, y + O,
                                                 fill="#ffffff", outline="")
                else:
                    self._ve_o(x, y, MAU_KHOI.get(ky_tu, "#64748b"))

    def _ve_khoi_dang_roi(self):
        if self.da_thua or self.dang_xoa:
            return

        mau = self._mau_khoi(tetris.b)
        for i in range(4):
            for j in range(4):
                if tetris.blocks[tetris.b][i][j] == " ":
                    continue
                hang = tetris.y + i
                cot = tetris.x + j
                if hang < 1:
                    continue
                x, y = self._toa_do(cot, hang)
                self._ve_o(x, y, mau)

    def _ve_bong(self):
        """Bóng mờ cho biết khối sẽ dừng ở đâu nếu thả thẳng xuống."""
        if self.da_thua or self.dang_xoa:
            return

        y_cu = tetris.y
        while tetris.can_move(0, 1):
            tetris.y += 1
        y_bong = tetris.y
        tetris.y = y_cu

        if y_bong == y_cu:
            return

        for i in range(4):
            for j in range(4):
                if tetris.blocks[tetris.b][i][j] == " ":
                    continue
                hang = y_bong + i
                cot = tetris.x + j
                if hang < 1:
                    continue
                x, y = self._toa_do(cot, hang)
                self.canvas.create_rectangle(
                    x + 3, y + 3, x + O - 3, y + O - 3,
                    outline="#2f3748", width=2,
                )

    def _mau_khoi(self, so):
        for hang in tetris.blocks[so]:
            for ky_tu in hang:
                if ky_tu != " ":
                    return MAU_KHOI.get(ky_tu, "#64748b")
        return "#64748b"

    # --------------------------------------------------------
    # Bảng thông tin bên phải
    # --------------------------------------------------------

    def _the(self, y, cao, tieu_de):
        x = self.x_panel
        self.canvas.create_rectangle(x, y, x + RONG_PANEL, y + cao,
                                     fill=NEN_THE, outline=VIEN)
        self.canvas.create_text(x + 14, y + 13, text=tieu_de, anchor="w",
                                fill=CHU_MO, font=self.f_nhan)
        return x

    def _ve_panel(self):
        x = self.x_panel
        y = self.y_bang

        self.canvas.create_text(x, y + 4, text="TETRIS", anchor="nw",
                                fill=CHU, font=self.f_tieu_de)
        self.canvas.create_text(x + 2, y + 36, text="Nhóm 07  ·  UIT",
                                anchor="nw", fill=NHAN, font=self.f_vua)

        y += 62
        for nhan, gia_tri in (("ĐIỂM", f"{self.diem:,}".replace(",", " ")),
                              ("HÀNG ĐÃ XOÁ", str(self.so_hang)),
                              ("CẤP ĐỘ", str(self.cap))):
            self._the(y, 58, nhan)
            self.canvas.create_text(x + 14, y + 38, text=gia_tri, anchor="w",
                                    fill=CHU, font=self.f_so)
            y += 68

        # Khung xem trước khối kế tiếp
        self._the(y, 128, "KHỐI KẾ TIẾP")
        self._ve_xem_truoc(x, y + 24)
        y += 142

        con = 10 - (self.so_hang % 10)
        self.canvas.create_text(
            x + 2, y, anchor="nw", fill=CHU_MO, font=self.f_phim,
            text=(f"Còn {con} hàng nữa lên cấp"
                  if self.cap < CAP_TOI_DA else "Đã đạt cấp cao nhất"))

    def _ve_xem_truoc(self, x_the, y_the):
        canh = 22
        o = [(i, j) for i in range(4) for j in range(4)
             if tetris.blocks[self.khoi_sau][i][j] != " "]
        if not o:
            return

        hang_min = min(i for i, _ in o)
        hang_max = max(i for i, _ in o)
        cot_min = min(j for _, j in o)
        cot_max = max(j for _, j in o)

        rong = (cot_max - cot_min + 1) * canh
        cao = (hang_max - hang_min + 1) * canh
        x0 = x_the + (RONG_PANEL - rong) / 2
        y0 = y_the + (104 - cao) / 2

        mau = self._mau_khoi(self.khoi_sau)
        for i, j in o:
            self._ve_o(x0 + (j - cot_min) * canh,
                       y0 + (i - hang_min) * canh, mau, canh)

    # --------------------------------------------------------
    # Lớp phủ khi tạm dừng hoặc thua
    # --------------------------------------------------------

    def _phu(self, tieu_de, phu_de, huong_dan):
        self.canvas.create_rectangle(
            self.x_bang, self.y_bang,
            self.x_bang + RONG_BANG, self.y_bang + CAO_BANG,
            fill="#000000", outline="", stipple="gray75",
        )

        giua_x = self.x_bang + RONG_BANG / 2
        giua_y = self.y_bang + CAO_BANG / 2

        self.canvas.create_text(giua_x, giua_y - 30, text=tieu_de,
                                fill=CHU, font=self.f_lon)
        if phu_de:
            self.canvas.create_text(giua_x, giua_y + 8, text=phu_de,
                                    fill=NHAN, font=self.f_vua)
        self.canvas.create_text(giua_x, giua_y + 46, text=huong_dan,
                                fill=CHU_MO, font=self.f_phim)


    # --------------------------------------------------------
    # MÀN MENU
    # --------------------------------------------------------

    def _ve_menu(self):
        giua = self.rong_cua_so / 2

        self.canvas.create_text(giua, 92, text="TETRIS", fill=CHU,
                                font=self.f_ten)
        self.canvas.create_line(giua - 120, 132, giua + 120, 132, fill=NHAN)
        self.canvas.create_text(giua, 156, fill=NHAN, font=self.f_vua,
                                text="Đồ án Kỹ năng nghề nghiệp  ·  Nhóm 07")
        self.canvas.create_text(giua, 180, fill=CHU_MO, font=self.f_vua,
                                text="Trường Đại học Công nghệ Thông tin")

        # Bày bảy loại khối thành một hàng cho sinh động
        canh = 18
        hinh = []
        for so in KHOI_BAN_DAU:
            o = [(i, j) for i in range(4) for j in range(4)
                 if tetris.blocks[so][i][j] != " "]
            cot_min = min(j for _, j in o)
            cot_max = max(j for _, j in o)
            hinh.append((so, o, cot_min, (cot_max - cot_min + 1) * canh))

        tong = sum(r for *_, r in hinh) + 18 * (len(hinh) - 1)
        x = giua - tong / 2
        for so, o, cot_min, rong in hinh:
            hang_min = min(i for i, _ in o)
            mau = self._mau_khoi(so)
            for i, j in o:
                self._ve_o(x + (j - cot_min) * canh,
                           236 + (i - hang_min) * canh, mau, canh)
            x += rong + 18

        bang = doc_diem_cao()
        if bang:
            self.canvas.create_text(
                giua, 334, fill=VANG, font=self.f_vua,
                text="Điểm cao nhất: {:,}".format(bang[0]["diem"]).replace(",", " "))

        self.canvas.create_text(
            giua, self.cao_canvas - 48, fill=CHU_MO, font=self.f_vua,
            text="Xếp khối cho kín một hàng ngang thì hàng đó biến mất.")
        self.canvas.create_text(
            giua, self.cao_canvas - 26, fill=CHU_MO, font=self.f_vua,
            text="Bảng đầy tới đỉnh là thua.")

    # --------------------------------------------------------
    # MÀN HƯỚNG DẪN
    # --------------------------------------------------------

    def _ve_huong_dan(self):
        giua = self.rong_cua_so / 2
        self.canvas.create_text(giua, 42, text="HƯỚNG DẪN CHƠI",
                                fill=CHU, font=self.f_tieu_de)

        x1, x2, y = LE + 10, giua + 24, 92

        self.canvas.create_text(x1, y, anchor="nw", text="ĐIỀU KHIỂN",
                                fill=NHAN, font=self.f_nhan)
        self.canvas.create_text(
            x1, y + 24, anchor="nw", fill=CHU, font=self.f_phim,
            text=("←  \→      dịch trái, dịch phải\n"
                  "\↑  hoặc W   xoay khối\n"
                  "S           xoay ngược chiều\n"
                  "\↓           rơi nhanh một hàng\n"
                  "Phím cách   thả thẳng xuống đáy\n"
                  "P           tạm dừng\n"
                  "R           chơi ván mới\n"
                  "Q           quay về menu"))

        self.canvas.create_text(x2, y, anchor="nw", text="CÁCH TÍNH ĐIỂM",
                                fill=NHAN, font=self.f_nhan)
        self.canvas.create_text(
            x2, y + 24, anchor="nw", fill=CHU, font=self.f_phim,
            text=("Xoá 1 hàng       100 điểm\n"
                  "Xoá 2 hàng       300 điểm\n"
                  "Xoá 3 hàng       500 điểm\n"
                  "Xoá 4 hàng       800 điểm\n"
                  "\n"
                  "Điểm nhân với cấp hiện tại.\n"
                  "Thả thẳng thêm 2 điểm mỗi\n"
                  "hàng rơi được."))

        y2 = y + 228
        self.canvas.create_text(x1, y2, anchor="nw", text="CẤP ĐỘ",
                                fill=NHAN, font=self.f_nhan)
        self.canvas.create_text(
            x1, y2 + 24, anchor="nw", fill=CHU, font=self.f_phim,
            text=("Cứ xoá đủ 10 hàng thì lên một cấp,\n"
                  "khối rơi nhanh hơn. Tối đa cấp 10.\n"
                  "Chọn cấp bắt đầu ở menu chính."))

        self.canvas.create_text(x2, y2, anchor="nw",
                                text="MẸO CHO NGƯỜI MỚI",
                                fill=NHAN, font=self.f_nhan)
        self.canvas.create_text(
            x2, y2 + 24, anchor="nw", fill=CHU, font=self.f_phim,
            text=("Giữ bề mặt phẳng, đừng tạo khe sâu.\n"
                  "Đừng xếp khối đè lên lỗ hổng.\n"
                  "Nhìn khung NEXT để tính trước.\n"
                  "Chừa một cột cho khối I ăn 800."))

    # --------------------------------------------------------
    # MÀN ĐIỂM CAO
    # --------------------------------------------------------

    def _ve_diem_cao(self):
        giua = self.rong_cua_so / 2
        self.canvas.create_text(giua, 42, text="BẢNG ĐIỂM CAO",
                                fill=CHU, font=self.f_tieu_de)

        bang = doc_diem_cao()
        if not bang:
            self.canvas.create_text(
                giua, 230, fill=CHU_MO, font=self.f_vua,
                text="Chưa có ván nào được ghi. Chơi một ván đi!")
            return

        x, y = giua - 215, 96
        self.canvas.create_text(x, y, anchor="nw", fill=CHU_MO,
                                font=self.f_nhan,
                                text="  #      ĐIỂM     HÀNG    CẤP    NGÀY")
        y += 28

        for i, d in enumerate(bang, 1):
            moi = (self.hang_moi == i)
            dong = ("{:>3}   {:>7,}".format(i, d["diem"]).replace(",", " ")
                    + "   {:>5}   {:>4}   {}".format(
                        d.get("hang", 0), d.get("cap", 1), d.get("ngay", "")))
            self.canvas.create_text(x, y, anchor="nw", text=dong,
                                    fill=VANG if moi else CHU,
                                    font=self.f_bang)
            if moi:
                self.canvas.create_text(x + 400, y, anchor="nw",
                                        text="◀ ván vừa rồi",
                                        fill=VANG, font=self.f_bang)
            y += 26

        self.canvas.create_text(
            giua, self.cao_canvas - 28, fill=CHU_MO, font=self.f_vua,
            text="Lưu trong " + os.path.basename(FILE_DIEM_CAO))

    # --------------------------------------------------------
    # MÀN ĐẾM NGƯỢC
    # --------------------------------------------------------

    def _ve_dem_nguoc(self):
        self._ve_nen_bang()
        self._ve_panel()

        giua_x = self.x_bang + RONG_BANG / 2
        giua_y = self.y_bang + CAO_BANG / 2

        chu = str(self.dem_con) if self.dem_con > 0 else "BẮT ĐẦU"
        self.canvas.create_text(
            giua_x, giua_y, text=chu, fill=NHAN,
            font=self.f_dem if self.dem_con > 0 else self.f_lon)
        self.canvas.create_text(giua_x, giua_y + 72, fill=CHU_MO,
                                font=self.f_vua,
                                text="Cấp bắt đầu: " + str(self.cap))

    # --------------------------------------------------------
    # LỚP PHỦ KHI THUA
    # --------------------------------------------------------

    def _phu_thua(self):
        self.canvas.create_rectangle(
            self.x_bang, self.y_bang,
            self.x_bang + RONG_BANG, self.y_bang + CAO_BANG,
            fill="#000000", outline="", stipple="gray75")

        giua_x = self.x_bang + RONG_BANG / 2
        y = self.y_bang + CAO_BANG / 2 - 92

        self.canvas.create_text(giua_x, y, text="GAME OVER", fill=CHU,
                                font=self.f_lon)
        y += 46

        if self.hang_moi:
            self.canvas.create_text(
                giua_x, y, fill=VANG, font=self.f_vua,
                text="★  Lọt bảng điểm cao, hạng " + str(self.hang_moi))
            y += 32

        for nhan, gia_tri in (
                ("Điểm", "{:,}".format(self.diem).replace(",", " ")),
                ("Hàng đã xoá", str(self.so_hang)),
                ("Cấp đạt được", str(self.cap))):
            self.canvas.create_text(giua_x - 12, y, anchor="e", text=nhan,
                                    fill=CHU_MO, font=self.f_vua)
            self.canvas.create_text(giua_x + 12, y, anchor="w",
                                    text=gia_tri, fill=CHU, font=self.f_vua)
            y += 26

        self.canvas.create_text(giua_x, y + 24, fill=CHU_MO,
                                font=self.f_phim,
                                text="R chơi lại        Q về menu")


def main():
    root = tk.Tk()
    Game(root)
    root.mainloop()


if __name__ == "__main__":
    main()
