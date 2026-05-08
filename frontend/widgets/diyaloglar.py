"""
Diyalog pencereleri - Editorial.
"""
from PyQt5.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QComboBox,
    QPushButton,
    QMessageBox,
    QFrame,
)
from PyQt5.QtCore import Qt

from backend import VeriYoneticisi, Kitap, Uye


def _form_satiri(etiket_metni: str, alan_widget) -> QVBoxLayout:
    layout = QVBoxLayout()
    layout.setSpacing(8)
    layout.setContentsMargins(0, 0, 0, 0)

    etiket = QLabel(etiket_metni.upper())
    etiket.setObjectName("FormEtiket")

    alan_widget.setMinimumHeight(42)

    layout.addWidget(etiket)
    layout.addWidget(alan_widget)
    return layout


def _diyalog_butonlari(iptal_metin="İPTAL", kaydet_metin="KAYDET"):
    iptal_btn = QPushButton(iptal_metin)
    iptal_btn.setObjectName("HayaletButon")
    iptal_btn.setFixedHeight(42)
    iptal_btn.setMinimumWidth(110)
    iptal_btn.setCursor(Qt.PointingHandCursor)

    kaydet_btn = QPushButton(kaydet_metin)
    kaydet_btn.setObjectName("PrimaryButon")
    kaydet_btn.setStyleSheet(
        "QPushButton { background-color: #0e0e0c; color: #fdfdfb; "
        "border: 1px solid #0e0e0c; border-radius: 0; "
        "padding: 0 22px; font-family: 'Inter', sans-serif; "
        "font-size: 11px; font-weight: 800; letter-spacing: 2px; } "
        "QPushButton:hover { background-color: #c9302c; "
        "border: 1px solid #c9302c; }"
    )
    kaydet_btn.setFixedHeight(42)
    kaydet_btn.setMinimumWidth(140)
    kaydet_btn.setCursor(Qt.PointingHandCursor)

    return iptal_btn, kaydet_btn


def _editorial_baslik(metin: str, kategori: str = "EDİTORYAL") -> QVBoxLayout:
    """Diyalog için gazete tarzı başlık bloğu."""
    l = QVBoxLayout()
    l.setSpacing(8)
    l.setContentsMargins(0, 0, 0, 0)

    # Kategori (kırmızı tag)
    kat = QLabel(kategori)
    kat.setStyleSheet(
        "color: #c9302c; font-family: 'Inter', sans-serif; "
        "font-size: 9px; font-weight: 800; letter-spacing: 2.5px; "
        "background: transparent; border: none;"
    )
    l.addWidget(kat)

    # Büyük başlık (serif)
    bl = QLabel(metin)
    bl.setStyleSheet(
        "color: #0e0e0c; font-family: 'Playfair Display', 'Georgia', serif; "
        "font-size: 28px; font-weight: 900; letter-spacing: -0.5px; "
        "background: transparent; border: none;"
    )
    l.addWidget(bl)

    # Kalın çizgi
    cizgi = QFrame()
    cizgi.setFixedHeight(2)
    cizgi.setStyleSheet("background-color: #0e0e0c;")
    l.addWidget(cizgi)

    return l


KATEGORILER = [
    "Roman", "Bilim Kurgu", "Distopya", "Tarih", "Bilim",
    "Felsefe", "Çocuk", "Fantastik", "Biyografi", "Hikaye",
    "Korku", "Şiir", "Genel",
]


class KitapDiyalog(QDialog):
    def __init__(self, vy: VeriYoneticisi, kitap: Kitap = None, parent=None):
        super().__init__(parent)
        self.vy = vy
        self.kitap = kitap
        self.duzenleme_modu = kitap is not None

        self.setWindowTitle("Yeni Yayın")
        self.setMinimumWidth(520)
        self.setModal(True)

        self._arayuz_olustur()
        if self.duzenleme_modu:
            self._mevcut_verileri_yukle()

    def _arayuz_olustur(self):
        ana = QVBoxLayout(self)
        ana.setContentsMargins(36, 32, 36, 28)
        ana.setSpacing(24)

        baslik = "Kitabı Düzenle" if self.duzenleme_modu else "Yeni Kitap"
        kategori = "DÜZENLE" if self.duzenleme_modu else "YENİ KİTAP"
        ana.addLayout(_editorial_baslik(baslik, kategori))

        # Açıklama
        aciklama = QLabel(
            "Tüm alanlar zorunludur. Kategori, koleksiyon "
            "etiketlemesinde kullanılır."
        )
        aciklama.setStyleSheet(
            "color: #7a7a72; font-family: 'Playfair Display', 'Georgia', serif; "
            "font-size: 13px; font-style: italic; "
            "background: transparent; border: none;"
        )
        aciklama.setWordWrap(True)
        ana.addWidget(aciklama)

        self.ad_input = QLineEdit()
        self.ad_input.setPlaceholderText("Örn: Suç ve Ceza")
        self.ad_input.returnPressed.connect(lambda: self.yazar_input.setFocus())

        self.yazar_input = QLineEdit()
        self.yazar_input.setPlaceholderText("Örn: Fyodor Dostoyevski")
        self.yazar_input.returnPressed.connect(self._kaydet)

        self.kategori_combo = QComboBox()
        self.kategori_combo.setEditable(True)
        for k in KATEGORILER:
            self.kategori_combo.addItem(k)

        ana.addLayout(_form_satiri("Eser Adı", self.ad_input))
        ana.addLayout(_form_satiri("Yazar", self.yazar_input))
        ana.addLayout(_form_satiri("Kategori", self.kategori_combo))

        ana.addStretch()

        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)

        iptal_btn, kaydet_btn = _diyalog_butonlari(
            kaydet_metin="GÜNCELLE" if self.duzenleme_modu else "KİTABI EKLE"
        )
        iptal_btn.clicked.connect(self.reject)
        kaydet_btn.clicked.connect(self._kaydet)

        btn_layout.addStretch()
        btn_layout.addWidget(iptal_btn)
        btn_layout.addWidget(kaydet_btn)
        ana.addLayout(btn_layout)

    def _mevcut_verileri_yukle(self):
        self.ad_input.setText(self.kitap.ad)
        self.yazar_input.setText(self.kitap.yazar)
        idx = self.kategori_combo.findText(self.kitap.kategori)
        if idx >= 0:
            self.kategori_combo.setCurrentIndex(idx)
        else:
            self.kategori_combo.setCurrentText(self.kitap.kategori)

    def _kaydet(self):
        ad = self.ad_input.text().strip()
        yazar = self.yazar_input.text().strip()
        kategori = self.kategori_combo.currentText().strip() or "Genel"

        if not ad:
            QMessageBox.warning(self, "Eksik Bilgi", "Eser adı boş olamaz.")
            self.ad_input.setFocus()
            return
        if not yazar:
            QMessageBox.warning(self, "Eksik Bilgi", "Yazar adı boş olamaz.")
            self.yazar_input.setFocus()
            return

        try:
            if self.duzenleme_modu:
                self.vy.kitap_guncelle(self.kitap.kitap_id, ad, yazar, kategori)
            else:
                self.vy.kitap_ekle(ad, yazar, kategori)
            self.accept()
        except ValueError as e:
            QMessageBox.warning(self, "Hata", str(e))


class UyeDiyalog(QDialog):
    def __init__(self, vy: VeriYoneticisi, uye: Uye = None, parent=None):
        super().__init__(parent)
        self.vy = vy
        self.uye = uye
        self.duzenleme_modu = uye is not None

        self.setWindowTitle("Yeni Üye")
        self.setMinimumWidth(520)
        self.setModal(True)

        self._arayuz_olustur()
        if self.duzenleme_modu:
            self._mevcut_verileri_yukle()

    def _arayuz_olustur(self):
        ana = QVBoxLayout(self)
        ana.setContentsMargins(36, 32, 36, 28)
        ana.setSpacing(24)

        baslik = "Üyeyi Düzenle" if self.duzenleme_modu else "Yeni Üye"
        kategori = "DÜZENLE" if self.duzenleme_modu else "YENİ ÜYE"
        ana.addLayout(_editorial_baslik(baslik, kategori))

        aciklama = QLabel(
            "E-posta adresi sistem genelinde benzersiz olmalıdır."
        )
        aciklama.setStyleSheet(
            "color: #7a7a72; font-family: 'Playfair Display', 'Georgia', serif; "
            "font-size: 13px; font-style: italic; "
            "background: transparent; border: none;"
        )
        ana.addWidget(aciklama)

        self.ad_input = QLineEdit()
        self.ad_input.setPlaceholderText("Örn: Beko Yılmaz")
        self.ad_input.returnPressed.connect(lambda: self.email_input.setFocus())

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("ornek@domain.com")
        self.email_input.returnPressed.connect(self._kaydet)

        ana.addLayout(_form_satiri("Ad Soyad", self.ad_input))
        ana.addLayout(_form_satiri("E-posta", self.email_input))

        ana.addStretch()

        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)

        iptal_btn, kaydet_btn = _diyalog_butonlari(
            kaydet_metin="GÜNCELLE" if self.duzenleme_modu else "KAYIT OLUŞTUR"
        )
        iptal_btn.clicked.connect(self.reject)
        kaydet_btn.clicked.connect(self._kaydet)

        btn_layout.addStretch()
        btn_layout.addWidget(iptal_btn)
        btn_layout.addWidget(kaydet_btn)
        ana.addLayout(btn_layout)

    def _mevcut_verileri_yukle(self):
        self.ad_input.setText(self.uye.ad)
        self.email_input.setText(self.uye.email)

    def _kaydet(self):
        ad = self.ad_input.text().strip()
        email = self.email_input.text().strip()

        if not ad:
            QMessageBox.warning(self, "Eksik Bilgi", "Ad soyad boş olamaz.")
            self.ad_input.setFocus()
            return
        if not email:
            QMessageBox.warning(self, "Eksik Bilgi", "E-posta boş olamaz.")
            self.email_input.setFocus()
            return
        if "@" not in email or "." not in email.split("@")[-1]:
            QMessageBox.warning(
                self, "Geçersiz E-posta",
                "Lütfen geçerli bir e-posta adresi girin.\nÖrnek: ornek@domain.com"
            )
            self.email_input.setFocus()
            return

        try:
            if self.duzenleme_modu:
                self.vy.uye_guncelle(self.uye.uye_id, ad, email)
            else:
                self.vy.uye_ekle(ad, email)
            self.accept()
        except ValueError as e:
            QMessageBox.warning(self, "Hata", str(e))
            self.email_input.setFocus()


class OduncVerDiyalog(QDialog):
    def __init__(self, vy: VeriYoneticisi, parent=None):
        super().__init__(parent)
        self.vy = vy

        self.setWindowTitle("Yeni Ödünç")
        self.setMinimumWidth(560)
        self.setModal(True)

        self._arayuz_olustur()

    def _arayuz_olustur(self):
        ana = QVBoxLayout(self)
        ana.setContentsMargins(36, 32, 36, 28)
        ana.setSpacing(24)

        ana.addLayout(_editorial_baslik("Ödünç İşlemi", "ÖDÜNÇ"))

        aciklama = QLabel(
            "Müsait kitaplar arasından seçim yapın. "
            "Ödünç süresi 14 gündür."
        )
        aciklama.setStyleSheet(
            "color: #7a7a72; font-family: 'Playfair Display', 'Georgia', serif; "
            "font-size: 13px; font-style: italic; "
            "background: transparent; border: none;"
        )
        ana.addWidget(aciklama)

        self.kitap_combo = QComboBox()
        self._kitaplari_yukle()

        self.uye_combo = QComboBox()
        self._uyeleri_yukle()

        ana.addLayout(_form_satiri("Kitap", self.kitap_combo))
        ana.addLayout(_form_satiri("Üye", self.uye_combo))

        # Bilgi kutu - editorial alıntı stili
        bilgi_kutu = QFrame()
        bilgi_kutu.setStyleSheet(
            "background-color: #f6f5f0; "
            "border-left: 3px solid #c9302c; "
            "border-radius: 0;"
        )
        bilgi_layout = QHBoxLayout(bilgi_kutu)
        bilgi_layout.setContentsMargins(16, 14, 16, 14)

        bilgi = QLabel(
            "Kitap, ödünç alındığı tarihten itibaren "
            "<b>14 gün</b> içinde iade edilmelidir."
        )
        bilgi.setStyleSheet(
            "color: #0e0e0c; font-family: 'Playfair Display', 'Georgia', serif; "
            "font-size: 13px; font-style: italic; "
            "background: transparent; border: none;"
        )
        bilgi.setWordWrap(True)
        bilgi_layout.addWidget(bilgi)

        ana.addWidget(bilgi_kutu)

        ana.addStretch()

        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)

        iptal_btn = QPushButton("İPTAL")
        iptal_btn.setObjectName("HayaletButon")
        iptal_btn.setFixedHeight(42)
        iptal_btn.setMinimumWidth(110)
        iptal_btn.setCursor(Qt.PointingHandCursor)
        iptal_btn.clicked.connect(self.reject)

        olustur_btn = QPushButton("ÖDÜNÇ VER")
        olustur_btn.setStyleSheet(
            "QPushButton { background-color: #0e0e0c; color: #fdfdfb; "
            "border: 1px solid #0e0e0c; border-radius: 0; "
            "padding: 0 22px; font-family: 'Inter', sans-serif; "
            "font-size: 11px; font-weight: 800; letter-spacing: 2px; } "
            "QPushButton:hover { background-color: #c9302c; "
            "border: 1px solid #c9302c; }"
        )
        olustur_btn.setFixedHeight(42)
        olustur_btn.setMinimumWidth(160)
        olustur_btn.setCursor(Qt.PointingHandCursor)
        olustur_btn.clicked.connect(self._kaydet)

        btn_layout.addStretch()
        btn_layout.addWidget(iptal_btn)
        btn_layout.addWidget(olustur_btn)
        ana.addLayout(btn_layout)

    def _kitaplari_yukle(self):
        self.kitap_combo.clear()
        for k in self.vy.musait_kitaplar():
            etiket = f"{k.ad}   ·   {k.yazar}"
            self.kitap_combo.addItem(etiket, k.kitap_id)

    def _uyeleri_yukle(self):
        self.uye_combo.clear()
        for u in self.vy.tum_uyeler():
            self.uye_combo.addItem(f"{u.ad}   ·   {u.email}", u.uye_id)

    def _kaydet(self):
        kid = self.kitap_combo.currentData()
        uid = self.uye_combo.currentData()

        if kid is None or uid is None:
            QMessageBox.warning(self, "Eksik Veri", "Lütfen kitap ve üye seçin.")
            return

        try:
            odunc = self.vy.odunc_ver(kid, uid)
            kitap = self.vy.kitap_getir(kid)
            uye = self.vy.uye_getir(uid)
            QMessageBox.information(
                self, "Ödünç Verildi",
                f"'{kitap.ad}' kitabı {uye.ad} üyesine ödünç verildi.\n\n"
                f"Son teslim tarihi: "
                f"{odunc.son_teslim_tarihi.strftime('%d.%m.%Y')}",
            )
            self.accept()
        except ValueError as e:
            QMessageBox.warning(self, "Hata", str(e))
