"""
Üyeler Sayfası - Editorial liste.
"""
from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QAbstractItemView,
    QMessageBox,
    QLineEdit,
    QFrame,
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QColor

from backend import VeriYoneticisi
from frontend.widgets.bilesenler import (
    EditorialHeader,
    MuhurAvatar,
    Rozet,
    HucreSarmalayici,
    ButonGrubu,
)
from frontend.widgets.diyaloglar import UyeDiyalog


class _UyeHucresi(QWidget):
    """Avatar mühür + ad + email birleşik hücre."""

    def __init__(self, ad: str, email: str, uid: int, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 6, 12, 6)
        layout.setSpacing(14)

        layout.addWidget(MuhurAvatar(ad, boyut=40))

        bilgi = QVBoxLayout()
        bilgi.setSpacing(2)
        bilgi.setContentsMargins(0, 0, 0, 0)

        ad_lbl = QLabel(ad)
        ad_lbl.setStyleSheet(
            "color: #0e0e0c; "
            "font-family: 'Playfair Display', 'Georgia', serif; "
            "font-weight: 800; font-size: 14px; "
            "background: transparent; border: none;"
        )

        meta_lbl = QLabel(
            f"<span style=\"color:#a5a59c; font-family:'Inter',sans-serif; "
            f"font-size:10px; font-weight:700; letter-spacing:1.5px;\">"
            f"#{uid:03d}  ·  </span>"
            f"<span style=\"color:#7a7a72; font-family:'Inter',sans-serif; "
            f"font-size:11px;\">{email}</span>"
        )
        meta_lbl.setStyleSheet("background: transparent; border: none;")

        bilgi.addWidget(ad_lbl)
        bilgi.addWidget(meta_lbl)

        layout.addLayout(bilgi)
        layout.addStretch()


class UyelerSayfasi(QWidget):
    veri_degisti = pyqtSignal()

    def __init__(self, vy: VeriYoneticisi, parent=None):
        super().__init__(parent)
        self.vy = vy
        self._arayuz_olustur()
        self.yenile()

    def _arayuz_olustur(self):
        ana = QVBoxLayout(self)
        ana.setContentsMargins(48, 36, 48, 32)
        ana.setSpacing(20)

        # Header
        header_satir = QHBoxLayout()
        header_satir.setSpacing(20)

        self.header = EditorialHeader(
            kategori="ÜYELER",
            baslik="Üyeler",
            altyazi="Sisteme kayıtlı tüm okurlar.",
            sag_etiket="LİSTE",
        )
        header_satir.addWidget(self.header, 1)

        ekle_btn = QPushButton("＋  YENİ ÜYE")
        ekle_btn.setStyleSheet(
            "QPushButton { background-color: #0e0e0c; color: #fdfdfb; "
            "border: 1px solid #0e0e0c; border-radius: 0; "
            "padding: 0 22px; font-family: 'Inter', sans-serif; "
            "font-size: 11px; font-weight: 800; letter-spacing: 2px; } "
            "QPushButton:hover { background-color: #c9302c; "
            "border: 1px solid #c9302c; }"
        )
        ekle_btn.setFixedHeight(46)
        ekle_btn.setMinimumWidth(150)
        ekle_btn.setCursor(Qt.PointingHandCursor)
        ekle_btn.clicked.connect(self._ekle)

        btn_sarici = QVBoxLayout()
        btn_sarici.addStretch()
        btn_sarici.addWidget(ekle_btn)
        btn_sarici.addSpacing(20)
        header_satir.addLayout(btn_sarici)

        ana.addLayout(header_satir)

        # Arama
        self.arama = QLineEdit()
        self.arama.setObjectName("AramaInput")
        self.arama.setPlaceholderText("ARA  ·  İsim veya e-posta...")
        self.arama.setFixedHeight(44)
        self.arama.textChanged.connect(self.yenile)
        ana.addWidget(self.arama)

        # Tablo
        self.tablo = QTableWidget(0, 3)
        self.tablo.setHorizontalHeaderLabels(["OKUR", "AKTİF ÖDÜNÇ", "İŞLEMLER"])
        self.tablo.verticalHeader().setVisible(False)
        self.tablo.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tablo.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tablo.setShowGrid(False)
        self.tablo.setFocusPolicy(Qt.NoFocus)
        self.tablo.setAlternatingRowColors(True)

        h = self.tablo.horizontalHeader()
        h.setSectionResizeMode(0, QHeaderView.Stretch)
        h.setSectionResizeMode(1, QHeaderView.Fixed)
        h.setSectionResizeMode(2, QHeaderView.Fixed)
        self.tablo.setColumnWidth(1, 150)
        self.tablo.setColumnWidth(2, 220)

        ana.addWidget(self.tablo, 1)

    def yenile(self):
        filtre = self.arama.text().strip().lower()
        uyeler = [
            u for u in self.vy.tum_uyeler()
            if filtre in u.ad.lower() or filtre in u.email.lower()
        ]

        aktif_sayilari = {}
        for o in self.vy.aktif_oduncler():
            aktif_sayilari[o.uye_id] = aktif_sayilari.get(o.uye_id, 0) + 1

        self.tablo.setRowCount(len(uyeler))

        for satir, u in enumerate(uyeler):
            self.tablo.setCellWidget(satir, 0, _UyeHucresi(u.ad, u.email, u.uye_id))

            aktif_n = aktif_sayilari.get(u.uye_id, 0)
            if aktif_n > 0:
                rozet = Rozet(f"{aktif_n} ÖDÜNÇ", "basari")
            else:
                rozet = Rozet("YOK", "notr")
            self.tablo.setCellWidget(satir, 1, HucreSarmalayici(rozet))

            duzen_btn = QPushButton("DÜZENLE")
            duzen_btn.setObjectName("KucukIkincilButon")
            duzen_btn.setFixedHeight(30)
            duzen_btn.setFixedWidth(94)
            duzen_btn.setCursor(Qt.PointingHandCursor)
            duzen_btn.clicked.connect(
                lambda _, uid=u.uye_id: self._duzenle(uid)
            )

            sil_btn = QPushButton("SİL")
            sil_btn.setObjectName("KucukTehlikeButon")
            sil_btn.setFixedHeight(30)
            sil_btn.setFixedWidth(56)
            sil_btn.setCursor(Qt.PointingHandCursor)
            sil_btn.clicked.connect(lambda _, uid=u.uye_id: self._sil(uid))

            self.tablo.setCellWidget(satir, 2, ButonGrubu([duzen_btn, sil_btn]))
            self.tablo.setRowHeight(satir, 64)

    def _ekle(self):
        d = UyeDiyalog(self.vy, parent=self)
        if d.exec_():
            self.yenile()
            self.veri_degisti.emit()

    def _duzenle(self, uye_id: int):
        u = self.vy.uye_getir(uye_id)
        if not u:
            return
        d = UyeDiyalog(self.vy, uye=u, parent=self)
        if d.exec_():
            self.yenile()
            self.veri_degisti.emit()

    def _sil(self, uye_id: int):
        u = self.vy.uye_getir(uye_id)
        if not u:
            return
        cevap = QMessageBox.question(
            self, "Üyeyi Sil",
            f"'{u.ad}' adlı üyeyi silmek istediğinizden emin misiniz?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No,
        )
        if cevap == QMessageBox.Yes:
            try:
                self.vy.uye_sil(uye_id)
                self.yenile()
                self.veri_degisti.emit()
            except ValueError as e:
                QMessageBox.warning(self, "Silinemedi", str(e))
