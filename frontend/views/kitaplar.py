"""
Kitaplar Sayfası - Editorial dergi grid.
"""
from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QLabel,
    QPushButton,
    QFrame,
    QMessageBox,
    QLineEdit,
    QComboBox,
    QScrollArea,
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QColor

from backend import VeriYoneticisi
from frontend.widgets.bilesenler import (
    EditorialHeader,
    KitapKapagi,
    Rozet,
)
from frontend.widgets.diyaloglar import KitapDiyalog


class _KitapKart(QFrame):
    """Tek bir kitap için editorial kart - kapak + bilgi + butonlar."""

    duzenle_isteniyor = pyqtSignal(int)
    sil_isteniyor = pyqtSignal(int)

    def __init__(self, kitap, parent=None):
        super().__init__(parent)
        self.kitap = kitap
        self.setStyleSheet(
            "QFrame { background-color: #ffffff; "
            "border: 1px solid #e8e7df; border-radius: 0; }"
            "QFrame:hover { border: 1px solid #0e0e0c; }"
        )
        self.setFixedHeight(360)

        ana = QVBoxLayout(self)
        ana.setContentsMargins(20, 20, 20, 20)
        ana.setSpacing(14)

        # Kapak ortalanmış
        kapak_sarici = QHBoxLayout()
        kapak_sarici.addStretch()
        kapak_sarici.addWidget(
            KitapKapagi(kitap.ad, kitap.yazar, kitap.kategori, kitap.musait_mi())
        )
        kapak_sarici.addStretch()
        ana.addLayout(kapak_sarici)

        # Kategori tag (kırmızı)
        kat = QLabel(kitap.kategori.upper())
        kat.setStyleSheet(
            "color: #c9302c; font-family: 'Inter', sans-serif; "
            "font-size: 9px; font-weight: 800; letter-spacing: 2px; "
            "background: transparent; border: none;"
        )
        ana.addWidget(kat)

        # Kitap adı (serif)
        ad = QLabel(kitap.ad)
        ad.setWordWrap(True)
        ad.setStyleSheet(
            "color: #0e0e0c; "
            "font-family: 'Playfair Display', 'Georgia', serif; "
            "font-size: 14px; font-weight: 800; letter-spacing: -0.2px; "
            "background: transparent; border: none;"
        )
        ad.setFixedHeight(40)
        ana.addWidget(ad)

        # Yazar (italic)
        yazar = QLabel(f"— {kitap.yazar}")
        yazar.setStyleSheet(
            "color: #7a7a72; "
            "font-family: 'Playfair Display', 'Georgia', serif; "
            "font-size: 11px; font-style: italic; "
            "background: transparent; border: none;"
        )
        ana.addWidget(yazar)

        ana.addStretch()


class KitaplarSayfasi(QWidget):
    veri_degisti = pyqtSignal()

    def __init__(self, vy: VeriYoneticisi, parent=None):
        super().__init__(parent)
        self.vy = vy
        self._arayuz_olustur()
        self.yenile()

    def _arayuz_olustur(self):
        ana = QVBoxLayout(self)
        ana.setContentsMargins(0, 0, 0, 0)
        ana.setSpacing(0)

        # Üst bar (sabit)
        ust_bar = QWidget()
        ust_bar.setStyleSheet("background-color: #fdfdfb;")
        ust_layout = QVBoxLayout(ust_bar)
        ust_layout.setContentsMargins(48, 36, 48, 24)
        ust_layout.setSpacing(20)

        # Header
        header_satir = QHBoxLayout()
        header_satir.setSpacing(20)

        self.header = EditorialHeader(
            kategori="KİTAPLAR",
            baslik="Kitaplar",
            altyazi="Tüm yayınlar — alfabetik sırayla.",
            sag_etiket="KOLEKSİYON",
        )
        header_satir.addWidget(self.header, 1)

        # Yeni Kitap butonu (sağ üst)
        ekle_btn = QPushButton("＋  YENİ KİTAP")
        ekle_btn.setObjectName("PrimaryButon")
        ekle_btn.setStyleSheet(
            "QPushButton { background-color: #0e0e0c; color: #fdfdfb; "
            "border: 1px solid #0e0e0c; border-radius: 0; "
            "padding: 0 22px; font-family: 'Inter', sans-serif; "
            "font-size: 11px; font-weight: 800; letter-spacing: 2px; } "
            "QPushButton:hover { background-color: #c9302c; "
            "border: 1px solid #c9302c; }"
        )
        ekle_btn.setFixedHeight(46)
        ekle_btn.setMinimumWidth(170)
        ekle_btn.setCursor(Qt.PointingHandCursor)
        ekle_btn.clicked.connect(self._ekle)

        # Header'ın sağına butonu hizala
        btn_sarici = QVBoxLayout()
        btn_sarici.addStretch()
        btn_sarici.addWidget(ekle_btn)
        btn_sarici.addSpacing(20)
        header_satir.addLayout(btn_sarici)

        ust_layout.addLayout(header_satir)

        # Filtre satırı
        filtre = QHBoxLayout()
        filtre.setSpacing(12)

        self.arama = QLineEdit()
        self.arama.setObjectName("AramaInput")
        self.arama.setPlaceholderText("ARA  ·  Kitap adı, yazar veya kategori...")
        self.arama.setFixedHeight(44)
        self.arama.textChanged.connect(self.yenile)
        filtre.addWidget(self.arama, 1)

        self.durum_filtre = QComboBox()
        self.durum_filtre.addItem("TÜM DURUMLAR", "tumu")
        self.durum_filtre.addItem("MÜSAİT", "musait")
        self.durum_filtre.addItem("ÖDÜNÇTE", "odunc")
        self.durum_filtre.setFixedHeight(44)
        self.durum_filtre.setMinimumWidth(180)
        self.durum_filtre.currentIndexChanged.connect(self.yenile)
        filtre.addWidget(self.durum_filtre)

        ust_layout.addLayout(filtre)

        # Sayım göstergesi
        self.sayim_lbl = QLabel("")
        self.sayim_lbl.setStyleSheet(
            "color: #7a7a72; font-family: 'Inter', sans-serif; "
            "font-size: 10px; font-weight: 700; letter-spacing: 2px; "
            "background: transparent; border: none;"
        )
        ust_layout.addWidget(self.sayim_lbl)

        ana.addWidget(ust_bar)

        # Scroll içeriği
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QFrame.NoFrame)
        self.scroll.setStyleSheet("background-color: #f6f5f0; border: none;")

        self.icerik = QWidget()
        self.scroll.setWidget(self.icerik)
        self.grid = QGridLayout(self.icerik)
        self.grid.setContentsMargins(48, 24, 48, 36)
        self.grid.setSpacing(16)
        self.grid.setAlignment(Qt.AlignTop)

        ana.addWidget(self.scroll, 1)

    def yenile(self):
        # Grid'i temizle
        while self.grid.count():
            item = self.grid.takeAt(0)
            w = item.widget()
            if w:
                w.setParent(None)
                w.deleteLater()

        filtre = self.arama.text().strip().lower()
        durum_filtre = self.durum_filtre.currentData()

        kitaplar = self.vy.tum_kitaplar()

        if filtre:
            kitaplar = [
                k for k in kitaplar
                if filtre in k.ad.lower()
                or filtre in k.yazar.lower()
                or filtre in k.kategori.lower()
            ]

        if durum_filtre != "tumu":
            kitaplar = [k for k in kitaplar if k.durum == durum_filtre]

        toplam = len(kitaplar)
        musait = sum(1 for k in kitaplar if k.musait_mi())
        self.sayim_lbl.setText(
            f"{toplam} ESER  ·  {musait} MÜSAİT  ·  {toplam - musait} DOLAŞIMDA"
        )

        if not kitaplar:
            bos = QLabel("— Aranan ölçütlerde eser bulunamadı. —")
            bos.setStyleSheet(
                "color: #7a7a72; font-family: 'Playfair Display', 'Georgia', serif; "
                "font-size: 16px; font-style: italic; padding: 60px; "
                "background: transparent; border: none;"
            )
            bos.setAlignment(Qt.AlignCenter)
            self.grid.addWidget(bos, 0, 0, 1, 4)
            return

        # 4 sütunlu grid
        cols = 4
        for i, k in enumerate(kitaplar):
            row = i // cols
            col = i % cols
            kart = self._kitap_karti(k)
            self.grid.addWidget(kart, row, col)

        for c in range(cols):
            self.grid.setColumnStretch(c, 1)

        # Her satıra minimum yükseklik vererek kapakların ezilmemesini sağla
        n_satir = (len(kitaplar) + cols - 1) // cols
        for r in range(n_satir):
            self.grid.setRowMinimumHeight(r, 460)

    def _kitap_karti(self, kitap) -> QFrame:
        """Editorial kitap kartı - kapak + bilgi + butonlar."""
        kart = QFrame()
        kart.setStyleSheet(
            "QFrame { background-color: #ffffff; "
            "border: 1px solid #e8e7df; border-radius: 0; }"
        )
        kart.setMinimumHeight(440)
        kart.setMaximumHeight(440)

        ana = QVBoxLayout(kart)
        ana.setContentsMargins(18, 18, 18, 18)
        ana.setSpacing(10)

        # Kapak ortalanmış - sabit yükseklik garantisi
        kapak_sarici_w = QWidget()
        kapak_sarici_w.setFixedHeight(225)
        kapak_sarici = QHBoxLayout(kapak_sarici_w)
        kapak_sarici.setContentsMargins(0, 0, 0, 0)
        kapak_sarici.addStretch()
        kapak = KitapKapagi(kitap.ad, kitap.yazar, kitap.kategori, kitap.musait_mi())
        kapak_sarici.addWidget(kapak)
        kapak_sarici.addStretch()
        ana.addWidget(kapak_sarici_w)

        # Hairline
        hr = QFrame()
        hr.setFixedHeight(1)
        hr.setStyleSheet("background-color: #e8e7df;")
        ana.addWidget(hr)

        # Kategori
        kat = QLabel(kitap.kategori.upper())
        kat.setStyleSheet(
            "color: #c9302c; font-family: 'Inter', sans-serif; "
            "font-size: 9px; font-weight: 800; letter-spacing: 2px; "
            "background: transparent; border: none;"
        )
        ana.addWidget(kat)

        # Kitap adı
        ad = QLabel(kitap.ad)
        ad.setWordWrap(True)
        ad.setMaximumHeight(46)
        ad.setStyleSheet(
            "color: #0e0e0c; "
            "font-family: 'Playfair Display', 'Georgia', serif; "
            "font-size: 15px; font-weight: 800; letter-spacing: -0.2px; "
            "background: transparent; border: none;"
        )
        ana.addWidget(ad)

        # Yazar
        yazar = QLabel(f"— {kitap.yazar}")
        yazar.setStyleSheet(
            "color: #7a7a72; "
            "font-family: 'Playfair Display', 'Georgia', serif; "
            "font-size: 11px; font-style: italic; "
            "background: transparent; border: none;"
        )
        yazar.setWordWrap(True)
        ana.addWidget(yazar)

        ana.addStretch()

        # Alt buton satırı
        alt = QHBoxLayout()
        alt.setSpacing(6)

        duzen_btn = QPushButton("DÜZENLE")
        duzen_btn.setObjectName("KucukIkincilButon")
        duzen_btn.setFixedHeight(30)
        duzen_btn.setCursor(Qt.PointingHandCursor)
        duzen_btn.clicked.connect(
            lambda _, kid=kitap.kitap_id: self._duzenle(kid)
        )

        sil_btn = QPushButton("SİL")
        sil_btn.setObjectName("KucukTehlikeButon")
        sil_btn.setFixedHeight(30)
        sil_btn.setFixedWidth(60)
        sil_btn.setCursor(Qt.PointingHandCursor)
        sil_btn.clicked.connect(lambda _, kid=kitap.kitap_id: self._sil(kid))

        alt.addWidget(duzen_btn, 1)
        alt.addWidget(sil_btn)
        ana.addLayout(alt)

        return kart

    def _ekle(self):
        d = KitapDiyalog(self.vy, parent=self)
        if d.exec_():
            self.yenile()
            self.veri_degisti.emit()

    def _duzenle(self, kitap_id: int):
        k = self.vy.kitap_getir(kitap_id)
        if not k:
            return
        d = KitapDiyalog(self.vy, kitap=k, parent=self)
        if d.exec_():
            self.yenile()
            self.veri_degisti.emit()

    def _sil(self, kitap_id: int):
        k = self.vy.kitap_getir(kitap_id)
        if not k:
            return
        cevap = QMessageBox.question(
            self, "Yayını Sil",
            f"'{k.ad}' kaydını silmek istediğinizden emin misiniz?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No,
        )
        if cevap == QMessageBox.Yes:
            try:
                self.vy.kitap_sil(kitap_id)
                self.yenile()
                self.veri_degisti.emit()
            except ValueError as e:
                QMessageBox.warning(self, "Silinemedi", str(e))
