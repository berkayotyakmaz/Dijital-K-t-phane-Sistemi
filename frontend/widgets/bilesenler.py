"""
Editorial widget'ları - Gazete/dergi tipografisi.
"""
import math
from PyQt5.QtWidgets import (
    QWidget,
    QFrame,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QSizePolicy,
)
from PyQt5.QtCore import Qt, QRectF, QPointF, QSize
from PyQt5.QtGui import (
    QPainter,
    QColor,
    QPen,
    QBrush,
    QFont,
    QPainterPath,
    QFontMetrics,
)


# Renkler
INK = QColor("#0e0e0c")
INK_DIM = QColor("#3d3d3a")
INK_MUTED = QColor("#7a7a72")
INK_SUBTLE = QColor("#a5a59c")
INK_FAINT = QColor("#d4d3cb")
PAPER = QColor("#fdfdfb")
PAPER_OFF = QColor("#f6f5f0")
PAPER_PANEL = QColor("#ffffff")
PAPER_INSET = QColor("#f0eee8")
RULE_THIN = QColor("#cfcec5")
RULE_HAIR = QColor("#e8e7df")
RED = QColor("#c9302c")
RED_DARK = QColor("#9a1f1c")
GOLD = QColor("#a08145")


# ============================================================
# METRİK KART — Sade rakam + etiket + altyazı
# ============================================================
class MetrikKart(QFrame):
    """Sade metric kart - üst kalın çizgi + etiket + serif rakam + altyazı."""

    def __init__(self, etiket: str, deger: str = "0", altyazi: str = "",
                 accent: bool = False, parent=None):
        super().__init__(parent)
        renk = "#c9302c" if accent else "#0e0e0c"
        self.setStyleSheet(
            "QFrame { background-color: #ffffff; "
            "border: 1px solid #e8e7df; "
            f"border-top: 2px solid {renk}; "
            "border-radius: 0; }"
        )
        self.setFixedHeight(140)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 18, 20, 18)
        layout.setSpacing(8)

        et = QLabel(etiket.upper())
        et.setStyleSheet(
            "color: #7a7a72; font-family: 'Inter', sans-serif; "
            "font-size: 10px; font-weight: 800; letter-spacing: 1.8px; "
            "background: transparent; border: none;"
        )
        layout.addWidget(et)
        layout.addStretch()

        self.deger_lbl = QLabel(str(deger))
        font = QFont("Playfair Display", 36, QFont.Black)
        if not font.exactMatch():
            font = QFont("Georgia", 36, QFont.Black)
        font.setLetterSpacing(QFont.AbsoluteSpacing, -1)
        self.deger_lbl.setFont(font)
        self.deger_lbl.setStyleSheet(
            "color: #0e0e0c; "
            "font-family: 'Playfair Display', 'Georgia', serif; "
            "background: transparent; border: none;"
        )
        layout.addWidget(self.deger_lbl)

        self.alt_lbl = QLabel(altyazi)
        self.alt_lbl.setStyleSheet(
            "color: #7a7a72; font-family: 'Inter', sans-serif; "
            "font-size: 11px; "
            "background: transparent; border: none;"
        )
        layout.addWidget(self.alt_lbl)

    def deger_ayarla(self, deger):
        # Uzun değer için font küçült
        deger_str = str(deger)
        n = len(deger_str)
        if n <= 3:
            size = 36
        elif n == 4:
            size = 30
        else:
            size = 26
        font = QFont("Playfair Display", size, QFont.Black)
        if not font.exactMatch():
            font = QFont("Georgia", size, QFont.Black)
        font.setLetterSpacing(QFont.AbsoluteSpacing, -0.8)
        self.deger_lbl.setFont(font)
        self.deger_lbl.setText(deger_str)

    def altyazi_ayarla(self, altyazi):
        self.alt_lbl.setText(altyazi)


# ============================================================
# MASTHEAD — Gazete logosu (sidebar üstünde)
# ============================================================
class Masthead(QWidget):
    """Sidebar'ın üstünde sade logo: 'The Library' + alt etiket."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(86)

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        w = self.width()
        h = self.height()

        # Sade üst hairline
        p.setPen(QPen(RULE_HAIR, 1))
        p.drawLine(22, 18, w - 22, 18)

        # Ana isim - serif
        p.setPen(INK)
        font = QFont("Playfair Display", 22, QFont.Black)
        if not font.exactMatch():
            font = QFont("Georgia", 22, QFont.Black)
        font.setLetterSpacing(QFont.AbsoluteSpacing, -0.8)
        p.setFont(font)
        p.drawText(QRectF(22, 28, w - 44, 32),
                   Qt.AlignLeft | Qt.AlignVCenter, "The Library")

        # Alt küçük etiket
        p.setPen(INK_MUTED)
        font = QFont("Inter", 8, QFont.Bold)
        font.setLetterSpacing(QFont.AbsoluteSpacing, 2)
        p.setFont(font)
        p.drawText(QRectF(22, 60, w - 44, 14),
                   Qt.AlignLeft | Qt.AlignVCenter, "KÜTÜPHANE SİSTEMİ")

        # Alt hairline
        p.setPen(QPen(RULE_HAIR, 1))
        p.drawLine(22, h - 8, w - 22, h - 8)


# ============================================================
# KAPAK — Editorial sayfa başlık paneli
# ============================================================
class EditorialHeader(QWidget):
    """
    Sayfa üstünde gazete tarzı header:
      [Sol: kategori tag + büyük başlık + altyazı]
      [Sağ: by-line + tarih + read time]
    """

    def __init__(
        self,
        kategori: str,
        baslik: str,
        altyazi: str,
        sag_etiket: str = "EDİTORYAL",
        sag_meta: str = "",
        parent=None,
    ):
        super().__init__(parent)
        self.kategori = kategori
        self.baslik = baslik
        self.altyazi = altyazi
        self.sag_etiket = sag_etiket
        self.sag_meta = sag_meta
        self.setMinimumHeight(180)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        w = self.width()
        h = self.height()

        # Üst hairline + 3 çizgi
        p.setPen(QPen(INK, 1))
        p.drawLine(0, 0, w, 0)

        # Kategori tag (sol üst, kırmızı)
        p.setPen(RED)
        font = QFont("Inter", 9, QFont.Bold)
        font.setLetterSpacing(QFont.AbsoluteSpacing, 2.5)
        p.setFont(font)
        kat_y = 30
        p.drawText(0, kat_y, self.kategori)

        # Sağ etiket
        p.setPen(INK_MUTED)
        font = QFont("Inter", 9, QFont.Bold)
        font.setLetterSpacing(QFont.AbsoluteSpacing, 2.5)
        p.setFont(font)
        fm = QFontMetrics(font)
        sag_x = w - fm.horizontalAdvance(self.sag_etiket)
        p.drawText(sag_x, kat_y, self.sag_etiket)

        # Büyük başlık
        p.setPen(INK)
        font = QFont("Playfair Display", 42, QFont.Black)
        if not font.exactMatch():
            font = QFont("Georgia", 42, QFont.Black)
        font.setLetterSpacing(QFont.AbsoluteSpacing, -1.2)
        p.setFont(font)
        p.drawText(QRectF(0, 50, w, 60),
                   Qt.AlignLeft | Qt.AlignTop, self.baslik)

        # Altyazı (italic serif, ince mürekkep)
        p.setPen(INK_DIM)
        font = QFont("Playfair Display", 14)
        if not font.exactMatch():
            font = QFont("Georgia", 14)
        font.setItalic(True)
        p.setFont(font)
        p.drawText(QRectF(0, 110, w, 28),
                   Qt.AlignLeft | Qt.AlignTop, self.altyazi)

        # Alt meta (sağ alt)
        if self.sag_meta:
            p.setPen(INK_MUTED)
            font = QFont("Inter", 10)
            p.setFont(font)
            fm = QFontMetrics(font)
            meta_x = w - fm.horizontalAdvance(self.sag_meta)
            p.drawText(meta_x, h - 16, self.sag_meta)

        # Alt rule (kalın siyah)
        p.setPen(QPen(INK, 2))
        p.drawLine(0, h - 1, w, h - 1)


# ============================================================
# DASHBOARD HERO — Manşet kartı (büyük editorial banner)
# ============================================================
class ManseteKart(QWidget):
    """
    Dashboard üstünde manşet:
    Sol: kategori tag + büyük serif başlık + altyazı + by-line
    Sağ: 4 büyük rakam grid (gazete istatistik bloğu)
    """

    def __init__(
        self,
        baslik: str,
        altyazi: str,
        by_line: str = "",
        sag_metrikler: list = None,
        parent=None,
    ):
        super().__init__(parent)
        self.baslik = baslik
        self.altyazi = altyazi
        self.by_line = by_line
        self.sag_metrikler = sag_metrikler or []
        self.setMinimumHeight(280)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

    def metrikleri_ayarla(self, metrikler: list):
        self.sag_metrikler = metrikler
        self.update()

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        w = self.width()
        h = self.height()

        # Beyaz panel + kalın çerçeve
        p.fillRect(self.rect(), PAPER_PANEL)

        # Üst kalın çizgi
        p.setPen(QPen(INK, 3))
        p.drawLine(0, 0, w, 0)
        # Üst ince ayraç altında
        p.setPen(QPen(INK, 1))
        p.drawLine(0, 6, w, 6)

        # SOL TARAF
        sol_x = 32
        sol_w = int(w * 0.55)

        # Kategori tag (kırmızı)
        p.setPen(RED)
        font = QFont("Inter", 9, QFont.Bold)
        font.setLetterSpacing(QFont.AbsoluteSpacing, 2.5)
        p.setFont(font)
        p.drawText(sol_x, 38, "MANŞET  ·  KÜTÜPHANE GÜNLÜĞÜ")

        # Başlık (büyük serif)
        p.setPen(INK)
        font = QFont("Playfair Display", 38, QFont.Black)
        if not font.exactMatch():
            font = QFont("Georgia", 38, QFont.Black)
        font.setLetterSpacing(QFont.AbsoluteSpacing, -1.2)
        p.setFont(font)

        # Başlığı 2 satıra böl (manuel)
        baslik_y = 60
        # Sol genişliğe sığacak şekilde wrap
        fm = QFontMetrics(font)
        kelimeler = self.baslik.split()
        satirlar = []
        kalan = ""
        for k in kelimeler:
            test = kalan + (" " if kalan else "") + k
            if fm.horizontalAdvance(test) <= sol_w - 32:
                kalan = test
            else:
                if kalan:
                    satirlar.append(kalan)
                kalan = k
        if kalan:
            satirlar.append(kalan)
        # En çok 2 satır
        satirlar = satirlar[:2]

        line_h = 48
        for i, satir in enumerate(satirlar):
            p.drawText(sol_x, baslik_y + (i + 1) * line_h, satir)

        # Altyazı
        alt_y = baslik_y + len(satirlar) * line_h + 28
        p.setPen(INK_DIM)
        font = QFont("Playfair Display", 14)
        if not font.exactMatch():
            font = QFont("Georgia", 14)
        font.setItalic(True)
        p.setFont(font)

        # Altyazıyı da wrap et
        fm = QFontMetrics(font)
        kelimeler = self.altyazi.split()
        alt_satirlar = []
        kalan = ""
        for k in kelimeler:
            test = kalan + (" " if kalan else "") + k
            if fm.horizontalAdvance(test) <= sol_w - 32:
                kalan = test
            else:
                if kalan:
                    alt_satirlar.append(kalan)
                kalan = k
        if kalan:
            alt_satirlar.append(kalan)
        alt_satirlar = alt_satirlar[:2]

        for i, satir in enumerate(alt_satirlar):
            p.drawText(sol_x, alt_y + i * 22, satir)

        # By-line (alt sol)
        if self.by_line:
            p.setPen(INK_MUTED)
            font = QFont("Inter", 10)
            font.setLetterSpacing(QFont.AbsoluteSpacing, 1.2)
            p.setFont(font)
            p.drawText(sol_x, h - 24, self.by_line)

        # Dikey ayraç
        ayrac_x = int(w * 0.58)
        p.setPen(QPen(RULE_HAIR, 1))
        p.drawLine(ayrac_x, 24, ayrac_x, h - 24)

        # SAĞ TARAF - 4 metrik 2x2 grid
        sag_x = ayrac_x + 32
        sag_w = w - sag_x - 32

        # "BU SAYIDA" mini başlık
        p.setPen(RED)
        font = QFont("Inter", 9, QFont.Bold)
        font.setLetterSpacing(QFont.AbsoluteSpacing, 2.5)
        p.setFont(font)
        p.drawText(sag_x, 38, "BU SAYIDA")

        # 2x2 grid
        m = self.sag_metrikler[:4]
        if len(m) >= 4:
            cell_w = sag_w / 2
            cell_h = (h - 80) / 2
            grid_y = 60

            for i, (etiket, deger) in enumerate(m):
                row = i // 2
                col = i % 2
                cx = sag_x + col * cell_w
                cy = grid_y + row * cell_h

                # Etiket
                p.setPen(INK_MUTED)
                font = QFont("Inter", 8, QFont.Bold)
                font.setLetterSpacing(QFont.AbsoluteSpacing, 2)
                p.setFont(font)
                p.drawText(int(cx), int(cy + 16), etiket.upper())

                # Değer (büyük serif)
                p.setPen(INK)
                font = QFont("Playfair Display", 36, QFont.Black)
                if not font.exactMatch():
                    font = QFont("Georgia", 36, QFont.Black)
                font.setLetterSpacing(QFont.AbsoluteSpacing, -1.5)
                p.setFont(font)
                p.drawText(int(cx), int(cy + 60), str(deger))

                # Mini kırmızı çizgi
                p.setBrush(RED)
                p.setPen(Qt.NoPen)
                p.drawRect(QRectF(cx, cy + 70, 24, 2))

        # Alt çift çizgi
        p.setPen(QPen(INK, 1))
        p.drawLine(0, h - 6, w, h - 6)
        p.drawLine(0, h - 1, w, h - 1)


# ============================================================
# RAKAM BLOK — Editorial istatistik (büyük serif rakam + etiket)
# ============================================================
class RakamBlok(QFrame):
    """
    Gazete istatistik bloğu:
      üstte ince üst çizgi + tag
      ortada büyük serif rakam
      altta altyazı (italic)
    """

    def __init__(
        self,
        etiket: str,
        deger: str = "0",
        altyazi: str = "",
        accent: bool = False,
        parent=None,
    ):
        super().__init__(parent)
        self.etiket = etiket
        self.deger = str(deger)
        self.altyazi = altyazi
        self.accent = accent
        self.setMinimumHeight(160)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

    def deger_ayarla(self, yeni: str):
        self.deger = str(yeni)
        self.update()

    def altyazi_ayarla(self, yeni: str):
        self.altyazi = yeni
        self.update()

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        w = self.width()
        h = self.height()

        # Beyaz panel
        p.fillRect(self.rect(), PAPER_PANEL)

        # Üst kalın çizgi (accent ise kırmızı)
        cizgi_renk = RED if self.accent else INK
        p.setPen(QPen(cizgi_renk, 2))
        p.drawLine(0, 0, w, 0)

        # Sol kenarlık ve diğer kenarlıklar (hairline)
        p.setPen(QPen(RULE_HAIR, 1))
        p.drawLine(0, 0, 0, h)
        p.drawLine(w - 1, 0, w - 1, h)
        p.drawLine(0, h - 1, w, h - 1)

        # Etiket
        p.setPen(INK_MUTED)
        font = QFont("Inter", 9, QFont.Bold)
        font.setLetterSpacing(QFont.AbsoluteSpacing, 2)
        p.setFont(font)
        p.drawText(QRectF(20, 18, w - 40, 18),
                   Qt.AlignLeft | Qt.AlignVCenter, self.etiket.upper())

        # Çok büyük rakam - uzunluğa göre font ayarla
        p.setPen(INK)
        n = len(self.deger)
        if n <= 3:
            font_size = 56
        elif n == 4:
            font_size = 46
        else:
            font_size = 38
        font = QFont("Playfair Display", font_size, QFont.Black)
        if not font.exactMatch():
            font = QFont("Georgia", font_size, QFont.Black)
        font.setLetterSpacing(QFont.AbsoluteSpacing, -1.5)
        p.setFont(font)
        p.drawText(QRectF(18, 36, w - 36, 80),
                   Qt.AlignLeft | Qt.AlignVCenter, self.deger)

        # Altyazı (italic)
        if self.altyazi:
            p.setPen(INK_MUTED)
            font = QFont("Playfair Display", 11)
            if not font.exactMatch():
                font = QFont("Georgia", 11)
            font.setItalic(True)
            p.setFont(font)
            p.drawText(QRectF(20, h - 30, w - 40, 18),
                       Qt.AlignLeft | Qt.AlignVCenter, "— " + self.altyazi)


# ============================================================
# KİTAP KAPAĞI — 3D ciltli kitap mockup
# ============================================================
class KitapKapagi(QWidget):
    """3D efektli kitap kapağı görseli."""

    PALETLER = [
        # (kapak rengi, sırt yan yüzü)
        (QColor("#3a2820"), QColor("#26190f")),  # koyu kahve deri
        (QColor("#5e2a26"), QColor("#3a1a18")),  # bordo
        (QColor("#1e3a4d"), QColor("#0f2030")),  # lacivert
        (QColor("#2d4a2a"), QColor("#1a2f18")),  # orman yeşili
        (QColor("#4a3a1d"), QColor("#2a210f")),  # hardal
        (QColor("#5a2a4a"), QColor("#3a1830")),  # mor şarap
        (QColor("#3a3a3a"), QColor("#222222")),  # kömür
        (QColor("#6b3520"), QColor("#42200f")),  # kestane
    ]

    def __init__(self, kitap_ad: str, yazar: str, kategori: str = "",
                 musait: bool = True, parent=None):
        super().__init__(parent)
        self.kitap_ad = kitap_ad
        self.yazar = yazar
        self.kategori = kategori
        self.musait = musait
        self.setFixedSize(150, 220)

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        w = self.width()
        h = self.height()

        # Renk seç (isimden hash)
        idx = hash(self.kitap_ad) % len(self.PALETLER)
        kapak, sirt = self.PALETLER[idx]

        # Gölge (kitap altında)
        p.setBrush(QColor(0, 0, 0, 30))
        p.setPen(Qt.NoPen)
        p.drawRect(QRectF(8, h - 8, w - 16, 5))

        # Sırt (sağ yan, 3D etkisi için biraz aşağı sağa)
        sirt_w = 8
        kapak_x = 4
        kapak_y = 4
        kapak_w = w - 12
        kapak_h = h - 12

        # Sırt parlama
        p.setBrush(sirt)
        p.setPen(Qt.NoPen)
        p.drawRect(QRectF(kapak_x + kapak_w, kapak_y + 3, sirt_w, kapak_h - 3))

        # Ana kapak
        p.setBrush(kapak)
        p.setPen(QPen(QColor(0, 0, 0, 80), 1))
        p.drawRect(QRectF(kapak_x, kapak_y, kapak_w, kapak_h))

        # Ciltleme bordürü (iç kenardan 4px)
        p.setBrush(Qt.NoBrush)
        p.setPen(QPen(QColor(255, 255, 255, 35), 1))
        p.drawRect(QRectF(kapak_x + 6, kapak_y + 6, kapak_w - 12, kapak_h - 12))

        # Üst dekoratif çizgi
        p.setPen(QPen(QColor(255, 255, 255, 50), 1))
        p.drawLine(int(kapak_x + 12), int(kapak_y + 22),
                   int(kapak_x + kapak_w - 12), int(kapak_y + 22))

        # Kitap adı (beyaz, küçük serif)
        p.setPen(QColor(255, 255, 255, 230))
        font = QFont("Playfair Display", 11, QFont.Bold)
        if not font.exactMatch():
            font = QFont("Georgia", 11, QFont.Bold)
        font.setLetterSpacing(QFont.AbsoluteSpacing, -0.2)
        p.setFont(font)
        p.drawText(
            QRectF(kapak_x + 12, kapak_y + 32, kapak_w - 24, 60),
            Qt.AlignHCenter | Qt.AlignTop | Qt.TextWordWrap,
            self.kitap_ad,
        )

        # Yazar
        p.setPen(QColor(255, 255, 255, 160))
        font = QFont("Inter", 8)
        font.setItalic(True)
        p.setFont(font)
        p.drawText(
            QRectF(kapak_x + 12, kapak_y + kapak_h - 50, kapak_w - 24, 16),
            Qt.AlignHCenter | Qt.AlignTop,
            "— " + self.yazar,
        )

        # Alt çizgi
        p.setPen(QPen(QColor(255, 255, 255, 60), 1))
        cizgi_y = kapak_y + kapak_h - 28
        p.drawLine(int(kapak_x + 24), int(cizgi_y),
                   int(kapak_x + kapak_w - 24), int(cizgi_y))

        # Kategori (en altta küçük)
        if self.kategori:
            p.setPen(QColor(255, 255, 255, 130))
            font = QFont("Inter", 7, QFont.Bold)
            font.setLetterSpacing(QFont.AbsoluteSpacing, 1.5)
            p.setFont(font)
            p.drawText(
                QRectF(kapak_x, kapak_y + kapak_h - 20, kapak_w, 14),
                Qt.AlignHCenter | Qt.AlignTop,
                self.kategori.upper(),
            )

        # Müsait değilse "ÖDÜNÇTE" mührü (kırmızı, çapraz)
        if not self.musait:
            p.save()
            p.translate(w / 2, h / 2)
            p.rotate(-15)

            # Kırmızı çapraz mühür
            p.setBrush(Qt.NoBrush)
            p.setPen(QPen(RED, 3))
            muh_w, muh_h = 110, 32
            p.drawRect(QRectF(-muh_w / 2, -muh_h / 2, muh_w, muh_h))

            p.setPen(RED)
            font = QFont("Inter", 11, QFont.Black)
            font.setLetterSpacing(QFont.AbsoluteSpacing, 3)
            p.setFont(font)
            p.drawText(QRectF(-muh_w / 2, -muh_h / 2, muh_w, muh_h),
                       Qt.AlignCenter, "ÖDÜNÇTE")
            p.restore()


# ============================================================
# MÜHÜR AVATAR — Editorial baş harf rozeti
# ============================================================
class MuhurAvatar(QWidget):
    """Çift halka ile mühür gibi baş harf avatarı."""

    def __init__(self, ad: str, boyut: int = 40, parent=None):
        super().__init__(parent)
        self.ad = ad.strip()
        self.bas_harf = self.ad[0].upper() if self.ad else "?"
        self.setFixedSize(boyut, boyut)

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        w = self.width()
        h = self.height()

        # İsme göre belirleyici renk: çoğunlukla mürekkep, bazıları kırmızı
        secim = hash(self.ad) % 5
        if secim == 0:
            renk = RED
        elif secim == 1:
            renk = GOLD
        else:
            renk = INK

        # Dış halka
        p.setBrush(Qt.NoBrush)
        p.setPen(QPen(renk, 1.5))
        p.drawEllipse(2, 2, w - 4, h - 4)

        # İç halka (boşluk bırakarak)
        p.drawEllipse(5, 5, w - 10, h - 10)

        # Harf
        p.setPen(renk)
        font = QFont("Playfair Display", int(w * 0.42), QFont.Black)
        if not font.exactMatch():
            font = QFont("Georgia", int(w * 0.42), QFont.Black)
        p.setFont(font)
        p.drawText(self.rect(), Qt.AlignCenter, self.bas_harf)


# ============================================================
# KART (basit) - başlık + içerik
# ============================================================
class Kart(QFrame):
    """Editorial kart - üstte siyah çizgi, başlık, ayraç, içerik."""

    def __init__(self, baslik: str = None, alt_baslik: str = None,
                 accent: bool = False, parent=None):
        super().__init__(parent)
        self.setObjectName("Kart")
        self.accent = accent

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(28, 24, 28, 24)
        self.layout.setSpacing(14)

        if baslik:
            ust = QHBoxLayout()
            ust.setContentsMargins(0, 0, 0, 0)
            ust.setSpacing(0)

            # Sol kırmızı dikey marker (accent ise)
            if accent:
                marker = QFrame()
                marker.setFixedSize(3, 28)
                marker.setStyleSheet("background-color: #c9302c; border: none;")
                ust.addWidget(marker, 0, Qt.AlignVCenter)
                ust.addSpacing(10)

            baslik_l = QVBoxLayout()
            baslik_l.setSpacing(2)
            baslik_l.setContentsMargins(0, 0, 0, 0)

            self.baslik_lbl = QLabel(baslik)
            self.baslik_lbl.setObjectName("KartBaslik")
            baslik_l.addWidget(self.baslik_lbl)

            if alt_baslik:
                self.alt_baslik_lbl = QLabel(alt_baslik)
                self.alt_baslik_lbl.setObjectName("KartAltBaslik")
                baslik_l.addWidget(self.alt_baslik_lbl)

            ust.addLayout(baslik_l)
            ust.addStretch()
            self.layout.addLayout(ust)

            # İnce ayraç
            ayrac = QFrame()
            ayrac.setObjectName("AyiriciInce")
            ayrac.setFixedHeight(1)
            ayrac.setStyleSheet("background-color: #e8e7df;")
            self.layout.addWidget(ayrac)


# ============================================================
# KATEGORİ BAR (gazete tablosu tarzı)
# ============================================================
class KategoriBarYatay(QWidget):
    """Editorial bar grafiği - siyah dolu, ince çizgi sınır."""

    def __init__(self, dagilim: dict, parent=None):
        super().__init__(parent)
        self.dagilim = dagilim
        n = len(dagilim) if dagilim else 1
        self.setMinimumHeight(n * 40 + 10)

    def paintEvent(self, e):
        if not self.dagilim:
            return
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        w = self.width()

        sirali = sorted(self.dagilim.items(), key=lambda x: -x[1])
        max_v = max(v for _, v in sirali) if sirali else 1

        # Sol numara, kategori, bar, sağ rakam
        no_w = 36
        kat_w = 130
        sag_w = 50
        bar_x = no_w + kat_w + 6
        bar_w = w - bar_x - sag_w - 6

        satir_y = 4

        for i, (kategori, sayi) in enumerate(sirali):
            cy = satir_y + 12

            # Sol numara (büyük serif, hafif)
            p.setPen(INK_FAINT)
            font = QFont("Playfair Display", 18, QFont.Black)
            if not font.exactMatch():
                font = QFont("Georgia", 18, QFont.Black)
            p.setFont(font)
            p.drawText(QRectF(0, satir_y, no_w, 32),
                       Qt.AlignLeft | Qt.AlignVCenter, f"{i + 1:02d}")

            # Kategori adı
            p.setPen(INK)
            font = QFont("Inter", 12, QFont.DemiBold)
            p.setFont(font)
            p.drawText(QRectF(no_w, satir_y, kat_w, 32),
                       Qt.AlignLeft | Qt.AlignVCenter, kategori)

            # Bar arka plan (ince çizgi)
            p.setPen(QPen(INK_FAINT, 1))
            p.drawLine(bar_x, satir_y + 22, bar_x + bar_w, satir_y + 22)

            # Bar dolu (siyah blok)
            dolu_w = (sayi / max_v) * bar_w
            renk = RED if i == 0 else INK
            p.setBrush(renk)
            p.setPen(Qt.NoPen)
            p.drawRect(QRectF(bar_x, satir_y + 18, dolu_w, 8))

            # Sayı (sağ, serif)
            p.setPen(INK)
            font = QFont("Playfair Display", 16, QFont.Black)
            if not font.exactMatch():
                font = QFont("Georgia", 16, QFont.Black)
            p.setFont(font)
            p.drawText(QRectF(bar_x + bar_w + 6, satir_y, sag_w, 32),
                       Qt.AlignRight | Qt.AlignVCenter, str(sayi))

            satir_y += 40


# ============================================================
# Yardımcı Sarmalayıcılar
# ============================================================
class Rozet(QLabel):
    """Editorial pill rozet - inline stil ile."""

    STILLER = {
        "basari": (
            "background-color: transparent; color: #1f6b3a; "
            "border: 1px solid #1f6b3a;"
        ),
        "uyari": (
            "background-color: transparent; color: #a37004; "
            "border: 1px solid #a37004;"
        ),
        "tehlike": (
            "background-color: #c9302c; color: #fdfdfb; "
            "border: 1px solid #c9302c;"
        ),
        "notr": (
            "background-color: transparent; color: #7a7a72; "
            "border: 1px solid #cfcec5;"
        ),
    }

    def __init__(self, metin: str, tip: str = "basari", parent=None):
        super().__init__(metin, parent)
        self.setAlignment(Qt.AlignCenter)
        self.setMinimumHeight(28)
        self.setMinimumWidth(96)

        renk_stil = self.STILLER.get(tip, self.STILLER["notr"])
        self.setStyleSheet(
            f"QLabel {{ {renk_stil} "
            f"border-radius: 0; "
            f"padding: 4px 12px; "
            f"font-family: 'Inter', sans-serif; "
            f"font-size: 9px; font-weight: 800; "
            f"letter-spacing: 1.5px; }}"
        )


class HucreSarmalayici(QWidget):
    def __init__(self, icerik: QWidget, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 6, 10, 6)
        layout.setSpacing(0)
        layout.addWidget(icerik, 0, Qt.AlignVCenter)


class ButonGrubu(QWidget):
    def __init__(self, butonlar: list, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 6, 8, 6)
        layout.setSpacing(6)
        for b in butonlar:
            layout.addWidget(b)
        layout.addStretch()


class Ayirici(QFrame):
    """Kalın yatay çizgi (gazete kuralı)."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("Ayirici")
        self.setFixedHeight(2)


class AyiriciInce(QFrame):
    """1px ince ayraç."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("AyiriciInce")
        self.setFixedHeight(1)
