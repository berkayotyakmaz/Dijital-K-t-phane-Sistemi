"""
Login Penceresi - Editorial / gazete kapağı tarzı.
"""
from PyQt5.QtWidgets import (
    QDialog,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QFrame,
    QCheckBox,
    QSizePolicy,
)
from PyQt5.QtCore import Qt, QRectF, QPointF
from PyQt5.QtGui import (
    QPainter,
    QColor,
    QPen,
    QFont,
    QPainterPath,
    QFontMetrics,
)

from backend import AuthYoneticisi, Kullanici


# Renkler
INK = QColor("#0e0e0c")
INK_DIM = QColor("#3d3d3a")
INK_MUTED = QColor("#7a7a72")
PAPER = QColor("#fdfdfb")
PAPER_OFF = QColor("#f6f5f0")
PAPER_INSET = QColor("#f0eee8")
RULE_THIN = QColor("#cfcec5")
RULE_HAIR = QColor("#e8e7df")
RED = QColor("#c9302c")
GOLD = QColor("#a08145")


class _GazeteKapagiPanel(QWidget):
    """Login penceresinin sol tarafı - gazete kapağı."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(560)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        rect = self.rect()
        w = rect.width()
        h = rect.height()

        # Kağıt arka plan
        p.fillRect(rect, PAPER)

        # Sağ kenarlık
        p.setPen(QPen(RULE_HAIR, 1))
        p.drawLine(w - 1, 0, w - 1, h)

        margin = 48

        # ─── MASTHEAD ────────────────────────────────────
        # Üst hairline
        p.setPen(QPen(RULE_HAIR, 1))
        p.drawLine(margin, 56, w - margin, 56)

        # Üst etiket
        p.setPen(INK_MUTED)
        font = QFont("Inter", 9, QFont.Bold)
        font.setLetterSpacing(QFont.AbsoluteSpacing, 2.5)
        p.setFont(font)
        p.drawText(QRectF(margin, 64, w - margin * 2, 18),
                   Qt.AlignLeft | Qt.AlignVCenter, "KÜTÜPHANE SİSTEMİ")

        # Büyük başlık
        p.setPen(INK)
        font = QFont("Playfair Display", 52, QFont.Black)
        if not font.exactMatch():
            font = QFont("Georgia", 52, QFont.Black)
        font.setLetterSpacing(QFont.AbsoluteSpacing, -1.8)
        p.setFont(font)
        p.drawText(QRectF(margin, 90, w - margin * 2, 70),
                   Qt.AlignLeft | Qt.AlignVCenter, "The Library")

        # Hairline
        p.setPen(QPen(INK, 1))
        p.drawLine(margin, 168, w - margin, 168)

        # ─── KISA SLOGAN ─────────────────────────────────
        p.setPen(INK_DIM)
        font = QFont("Playfair Display", 18)
        if not font.exactMatch():
            font = QFont("Georgia", 18)
        font.setItalic(True)
        p.setFont(font)
        slogan_y = 220
        p.drawText(QRectF(margin, slogan_y, w - margin * 2, 30),
                   Qt.AlignLeft, "Kitabınızı, üyenizi, ödüncünüzü")
        p.drawText(QRectF(margin, slogan_y + 32, w - margin * 2, 30),
                   Qt.AlignLeft, "tek panelden yönetin.")

        # ─── ÖZELLİKLER LİSTESİ ──────────────────────────
        ozellik_y = 320
        ozellikler = [
            "Kitap koleksiyonu yönetimi",
            "Üye kayıtları ve takibi",
            "Ödünç ve iade işlemleri",
            "Detaylı raporlar ve analiz",
        ]

        for i, oz in enumerate(ozellikler):
            y = ozellik_y + i * 38

            # Bullet (kırmızı küçük kare)
            p.setBrush(RED)
            p.setPen(Qt.NoPen)
            p.drawRect(QRectF(margin, y - 6, 6, 6))

            # Metin
            p.setPen(INK)
            font = QFont("Inter", 12)
            font.setWeight(QFont.Medium)
            p.setFont(font)
            p.drawText(margin + 18, y, oz)

        # ─── ALT FOOTER ──────────────────────────────────
        p.setPen(QPen(RULE_HAIR, 1))
        p.drawLine(margin, h - 48, w - margin, h - 48)

        p.setPen(INK_MUTED)
        font = QFont("Inter", 9)
        font.setLetterSpacing(QFont.AbsoluteSpacing, 1.5)
        p.setFont(font)
        p.drawText(QRectF(margin, h - 36, w - margin * 2, 16),
                   Qt.AlignLeft | Qt.AlignVCenter, "© 2026 The Library")
        p.drawText(QRectF(margin, h - 36, w - margin * 2, 16),
                   Qt.AlignRight | Qt.AlignVCenter, "v1.0")


class LoginPenceresi(QDialog):
    """Editorial login dialog."""

    def __init__(self, auth: AuthYoneticisi, parent=None):
        super().__init__(parent)
        self.auth = auth
        self.dogrulanan_kullanici: Kullanici | None = None

        self.setWindowTitle("The Library — Giriş")
        self.setFixedSize(1080, 680)
        self.setModal(True)

        self._arayuz_olustur()

    def _arayuz_olustur(self):
        ana = QHBoxLayout(self)
        ana.setContentsMargins(0, 0, 0, 0)
        ana.setSpacing(0)

        ana.addWidget(_GazeteKapagiPanel())

        # Sağ form alanı
        sag = QFrame()
        sag.setStyleSheet("background-color: #fdfdfb;")
        sag_layout = QVBoxLayout(sag)
        sag_layout.setContentsMargins(56, 64, 56, 48)
        sag_layout.setSpacing(0)

        # Kategori tag
        kat = QLabel("GİRİŞ")
        kat.setStyleSheet(
            "color: #c9302c; font-family: 'Inter', sans-serif; "
            "font-size: 10px; font-weight: 800; "
            "letter-spacing: 2.5px; "
            "background: transparent; border: none;"
        )
        sag_layout.addWidget(kat)
        sag_layout.addSpacing(14)

        # Hoş Geldin
        baslik = QLabel("Hoş Geldin")
        baslik.setStyleSheet(
            "color: #0e0e0c; font-family: 'Playfair Display', 'Georgia', serif; "
            "font-size: 42px; font-weight: 900; letter-spacing: -1px; "
            "background: transparent; border: none;"
        )
        sag_layout.addWidget(baslik)

        alt = QLabel("Devam etmek için hesabına giriş yap.")
        alt.setStyleSheet(
            "color: #7a7a72; font-family: 'Playfair Display', 'Georgia', serif; "
            "font-size: 14px; font-style: italic; "
            "background: transparent; border: none;"
        )
        sag_layout.addWidget(alt)

        sag_layout.addSpacing(12)

        # 2px ayraç
        ayrac = QFrame()
        ayrac.setFixedHeight(2)
        ayrac.setStyleSheet("background-color: #0e0e0c;")
        sag_layout.addWidget(ayrac)

        sag_layout.addSpacing(28)

        # Form
        sag_layout.addWidget(self._etiket("KULLANICI ADI"))
        sag_layout.addSpacing(8)

        self.kul_input = QLineEdit()
        self.kul_input.setPlaceholderText("kullanıcı adınızı girin")
        self.kul_input.setFixedHeight(46)
        self.kul_input.setStyleSheet(self._input_stil())
        self.kul_input.returnPressed.connect(lambda: self.sifre_input.setFocus())
        sag_layout.addWidget(self.kul_input)
        sag_layout.addSpacing(20)

        sag_layout.addWidget(self._etiket("ŞİFRE"))
        sag_layout.addSpacing(8)

        self.sifre_input = QLineEdit()
        self.sifre_input.setPlaceholderText("••••••••")
        self.sifre_input.setEchoMode(QLineEdit.Password)
        self.sifre_input.setFixedHeight(46)
        self.sifre_input.setStyleSheet(self._input_stil())
        self.sifre_input.returnPressed.connect(self._giris_yap)
        sag_layout.addWidget(self.sifre_input)

        sag_layout.addSpacing(14)

        # Göster checkbox
        self.goster_chk = QCheckBox("Şifreyi göster")
        self.goster_chk.setStyleSheet(
            "QCheckBox { color: #7a7a72; font-family: 'Inter', sans-serif; "
            "font-size: 11px; font-weight: 600; letter-spacing: 0.5px; "
            "background: transparent; border: none; spacing: 8px; }"
            "QCheckBox::indicator { width: 14px; height: 14px; "
            "border: 1px solid #0e0e0c; border-radius: 0; "
            "background-color: #fdfdfb; }"
            "QCheckBox::indicator:checked { background-color: #0e0e0c; }"
        )
        self.goster_chk.toggled.connect(self._sifre_goster)
        sag_layout.addWidget(self.goster_chk)

        sag_layout.addSpacing(24)

        # Hata kutusu
        self.hata_lbl = QLabel("")
        self.hata_lbl.setStyleSheet(
            "background-color: #fbeae8; color: #c9302c; "
            "border: 1px solid #c9302c; border-radius: 0; "
            "padding: 12px 16px; "
            "font-family: 'Inter', sans-serif; font-size: 12px; font-weight: 600;"
        )
        self.hata_lbl.setVisible(False)
        sag_layout.addWidget(self.hata_lbl)

        # Giriş butonu
        self.giris_btn = QPushButton("OTURUM AÇ")
        self.giris_btn.setFixedHeight(50)
        self.giris_btn.setCursor(Qt.PointingHandCursor)
        self.giris_btn.setStyleSheet(
            "QPushButton { background-color: #0e0e0c; color: #fdfdfb; "
            "border: 1px solid #0e0e0c; border-radius: 0; "
            "font-family: 'Inter', sans-serif; font-size: 12px; "
            "font-weight: 800; letter-spacing: 3px; } "
            "QPushButton:hover { background-color: #c9302c; "
            "border: 1px solid #c9302c; }"
        )
        self.giris_btn.clicked.connect(self._giris_yap)
        sag_layout.addWidget(self.giris_btn)

        sag_layout.addSpacing(20)

        # Hairline
        hr = QFrame()
        hr.setFixedHeight(1)
        hr.setStyleSheet("background-color: #cfcec5;")
        sag_layout.addWidget(hr)
        sag_layout.addSpacing(16)

        # İpucu - editorial dipnot tarzında
        ipucu = QLabel(
            "<span style=\"color:#7a7a72; font-family:'Inter',sans-serif; font-size:11px; font-weight:700; letter-spacing:1.5px;\">VARSAYILAN ERİŞİM</span><br><br>"
            "<span style=\"color:#0e0e0c; font-family:'Inter',sans-serif; font-size:13px; font-weight:600;\">"
            "admin <span style='color:#c9302c;'>·</span> admin123</span>"
        )
        ipucu.setStyleSheet(
            "background-color: #f6f5f0; "
            "border-left: 3px solid #c9302c; "
            "padding: 14px 18px; border-radius: 0;"
        )
        sag_layout.addWidget(ipucu)

        sag_layout.addStretch()

        # Footer
        footer = QLabel("© 2026 The Library")
        footer.setStyleSheet(
            "color: #a5a59c; font-family: 'Inter', sans-serif; "
            "font-size: 10px; letter-spacing: 1px; "
            "background: transparent; border: none;"
        )
        footer.setAlignment(Qt.AlignCenter)
        sag_layout.addWidget(footer)

        ana.addWidget(sag, 1)

    def _etiket(self, metin: str) -> QLabel:
        lbl = QLabel(metin)
        lbl.setStyleSheet(
            "color: #3d3d3a; font-family: 'Inter', sans-serif; "
            "font-size: 10px; font-weight: 800; letter-spacing: 1.8px; "
            "background: transparent; border: none;"
        )
        return lbl

    def _input_stil(self) -> str:
        return (
            "QLineEdit { background-color: #fdfdfb; "
            "border: 1px solid #cfcec5; border-bottom: 2px solid #0e0e0c; "
            "border-radius: 0; padding: 0 14px; "
            "color: #0e0e0c; font-family: 'Inter', sans-serif; font-size: 14px; "
            "selection-background-color: #0e0e0c; selection-color: #fdfdfb; } "
            "QLineEdit:focus { border: 1px solid #0e0e0c; "
            "border-bottom: 2px solid #c9302c; background-color: #f6f5f0; } "
            "QLineEdit:hover { border-bottom: 2px solid #c9302c; }"
        )

    def _sifre_goster(self, checked: bool):
        self.sifre_input.setEchoMode(
            QLineEdit.Normal if checked else QLineEdit.Password
        )

    def _hata_goster(self, mesaj: str):
        self.hata_lbl.setText(f"⚠  {mesaj.upper()}")
        self.hata_lbl.setVisible(True)

    def _hata_gizle(self):
        self.hata_lbl.setVisible(False)

    def _giris_yap(self):
        kul = self.kul_input.text().strip()
        sifre = self.sifre_input.text()

        if not kul:
            self._hata_goster("Kullanıcı adı boş olamaz.")
            self.kul_input.setFocus()
            return
        if not sifre:
            self._hata_goster("Şifre boş olamaz.")
            self.sifre_input.setFocus()
            return

        kullanici = self.auth.dogrula(kul, sifre)
        if kullanici is None:
            self._hata_goster("Kullanıcı adı veya şifre hatalı.")
            self.sifre_input.clear()
            self.sifre_input.setFocus()
            return

        self.dogrulanan_kullanici = kullanici
        self.accept()
