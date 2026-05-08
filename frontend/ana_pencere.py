"""
Ana Pencere - Editorial sidebar.
"""
from PyQt5.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QStackedWidget,
    QButtonGroup,
    QFrame,
)
from PyQt5.QtCore import Qt

from backend import VeriYoneticisi
from frontend.tema import ANA_STIL
from frontend.widgets.bilesenler import Masthead, MuhurAvatar
from frontend.views.dashboard import DashboardSayfasi
from frontend.views.kitaplar import KitaplarSayfasi
from frontend.views.uyeler import UyelerSayfasi
from frontend.views.oduncler import OdunclerSayfasi
from frontend.views.raporlar import RaporlarSayfasi


class AnaPencere(QMainWindow):
    def __init__(self, vy: VeriYoneticisi, aktif_kullanici=None):
        super().__init__()
        self.vy = vy
        self.aktif_kullanici = aktif_kullanici

        self.setWindowTitle("The Library — Dijital Kütüphane Günlüğü")
        self.setMinimumSize(1180, 760)
        self.resize(1380, 880)

        self._arayuz_olustur()

    def _arayuz_olustur(self):
        merkez = QWidget()
        ana = QHBoxLayout(merkez)
        ana.setContentsMargins(0, 0, 0, 0)
        ana.setSpacing(0)

        sidebar = self._sidebar_olustur()
        ana.addWidget(sidebar)

        # İçerik alanı
        icerik_sarici = QWidget()
        icerik_sarici.setStyleSheet("background-color: #fdfdfb;")
        icerik_layout = QVBoxLayout(icerik_sarici)
        icerik_layout.setContentsMargins(0, 0, 0, 0)
        icerik_layout.setSpacing(0)

        self.yigin = QStackedWidget()

        self.sayfa_dashboard = DashboardSayfasi(self.vy, self.aktif_kullanici)
        self.sayfa_kitaplar = KitaplarSayfasi(self.vy)
        self.sayfa_uyeler = UyelerSayfasi(self.vy)
        self.sayfa_oduncler = OdunclerSayfasi(self.vy)
        self.sayfa_raporlar = RaporlarSayfasi(self.vy)

        self.sayfa_kitaplar.veri_degisti.connect(self._tumunu_yenile)
        self.sayfa_uyeler.veri_degisti.connect(self._tumunu_yenile)
        self.sayfa_oduncler.veri_degisti.connect(self._tumunu_yenile)

        self.yigin.addWidget(self.sayfa_dashboard)
        self.yigin.addWidget(self.sayfa_kitaplar)
        self.yigin.addWidget(self.sayfa_uyeler)
        self.yigin.addWidget(self.sayfa_oduncler)
        self.yigin.addWidget(self.sayfa_raporlar)

        icerik_layout.addWidget(self.yigin)

        ana.addWidget(icerik_sarici, 1)

        self.setCentralWidget(merkez)
        self.yigin.setCurrentIndex(0)

    def _sidebar_olustur(self) -> QFrame:
        sidebar = QFrame()
        sidebar.setObjectName("Sidebar")
        sidebar.setFixedWidth(264)

        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(0, 0, 0, 16)
        layout.setSpacing(0)

        # Masthead
        layout.addWidget(Masthead())
        layout.addSpacing(28)

        # Tek menü bölümü - sade
        layout.addWidget(self._menu_baslik("MENÜ"))

        self.buton_grubu = QButtonGroup(self)
        self.buton_grubu.setExclusive(True)

        self._menu_butonu_ekle(layout, "Dashboard", 0)
        self._menu_butonu_ekle(layout, "Kitaplar", 1)
        self._menu_butonu_ekle(layout, "Üyeler", 2)
        self._menu_butonu_ekle(layout, "Ödünç İşlemleri", 3)
        self._menu_butonu_ekle(layout, "Raporlar", 4)

        self.buton_grubu.button(0).setChecked(True)

        layout.addStretch()

        # Kullanıcı kartı
        kart_sarici = QHBoxLayout()
        kart_sarici.setContentsMargins(16, 0, 16, 0)

        kullanici_kart = QFrame()
        kullanici_kart.setObjectName("KullaniciKart")

        kk_layout = QHBoxLayout(kullanici_kart)
        kk_layout.setContentsMargins(14, 14, 14, 14)
        kk_layout.setSpacing(12)

        if self.aktif_kullanici:
            ad_str = self.aktif_kullanici.ad
            rol_str = self.aktif_kullanici.rol.upper()
        else:
            ad_str = "Kullanıcı"
            rol_str = "MİSAFİR"

        avatar = MuhurAvatar(ad_str, boyut=40)

        kullanici_bilgi = QVBoxLayout()
        kullanici_bilgi.setSpacing(2)
        kullanici_bilgi.setContentsMargins(0, 0, 0, 0)

        ust_satir = QHBoxLayout()
        ust_satir.setSpacing(8)
        ust_satir.setContentsMargins(0, 0, 0, 0)

        ad = QLabel(ad_str)
        ad.setObjectName("KullaniciAd")

        plan = QLabel("EDİTÖR")
        plan.setObjectName("PlanRozet")
        plan.setAlignment(Qt.AlignCenter)
        plan.setMinimumWidth(54)
        plan.setMinimumHeight(20)

        ust_satir.addWidget(ad)
        ust_satir.addWidget(plan)
        ust_satir.addStretch()

        durum = QLabel(rol_str)
        durum.setObjectName("KullaniciDurum")

        kullanici_bilgi.addLayout(ust_satir)
        kullanici_bilgi.addWidget(durum)

        kk_layout.addWidget(avatar)
        kk_layout.addLayout(kullanici_bilgi)
        kk_layout.addStretch()

        cikis_btn = QPushButton("⎋")
        cikis_btn.setFixedSize(30, 30)
        cikis_btn.setCursor(Qt.PointingHandCursor)
        cikis_btn.setToolTip("Çıkış yap")
        cikis_btn.setStyleSheet(
            "QPushButton { background-color: transparent; "
            "color: #7a7a72; border: 1px solid #cfcec5; "
            "border-radius: 0; font-size: 14px; padding: 0; "
            "letter-spacing: 0; } "
            "QPushButton:hover { color: #fdfdfb; "
            "background-color: #c9302c; "
            "border: 1px solid #c9302c; }"
        )
        cikis_btn.clicked.connect(self._cikis_yap)
        kk_layout.addWidget(cikis_btn, 0, Qt.AlignVCenter)

        kart_sarici.addWidget(kullanici_kart)
        layout.addLayout(kart_sarici)

        return sidebar

    def _menu_baslik(self, metin: str) -> QLabel:
        lbl = QLabel(metin)
        lbl.setObjectName("MenuBaslik")
        lbl.setContentsMargins(24, 0, 24, 10)
        return lbl

    def _menu_butonu_ekle(self, layout, metin: str, indeks: int):
        btn = QPushButton(metin)
        btn.setObjectName("MenuButon")
        btn.setCheckable(True)
        btn.setFixedHeight(38)
        btn.setCursor(Qt.PointingHandCursor)
        # Editorial menu butonu -- text-transform önemli (dergi tarzı)
        btn.clicked.connect(lambda _, i=indeks: self._sayfa_degistir(i))
        self.buton_grubu.addButton(btn, indeks)
        layout.addWidget(btn)

    def _cikis_yap(self):
        from PyQt5.QtWidgets import QMessageBox
        cevap = QMessageBox.question(
            self, "Oturum Sonlandır",
            "Oturumu kapatıp giriş ekranına dönmek istediğinize emin misiniz?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No,
        )
        if cevap == QMessageBox.Yes:
            from PyQt5.QtWidgets import QApplication
            QApplication.quit()

    def _sayfa_degistir(self, indeks: int):
        self.yigin.setCurrentIndex(indeks)
        sayfa = self.yigin.widget(indeks)
        if hasattr(sayfa, "yenile"):
            sayfa.yenile()

    def _tumunu_yenile(self):
        for i in range(self.yigin.count()):
            sayfa = self.yigin.widget(i)
            if hasattr(sayfa, "yenile"):
                sayfa.yenile()
