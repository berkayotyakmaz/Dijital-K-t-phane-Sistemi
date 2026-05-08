"""
Ödünç İşlemleri Sayfası - Editorial.
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
    QComboBox,
    QFrame,
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QColor

from backend import VeriYoneticisi
from frontend.widgets.bilesenler import (
    EditorialHeader,
    Rozet,
    HucreSarmalayici,
    ButonGrubu,
)
from frontend.widgets.diyaloglar import OduncVerDiyalog


class OdunclerSayfasi(QWidget):
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
            kategori="ÖDÜNÇLER",
            baslik="Ödünç İşlemleri",
            altyazi="Tüm ödünç ve iade hareketleri.",
            sag_etiket="KAYIT",
        )
        header_satir.addWidget(self.header, 1)

        olustur_btn = QPushButton("＋  YENİ ÖDÜNÇ")
        olustur_btn.setStyleSheet(
            "QPushButton { background-color: #0e0e0c; color: #fdfdfb; "
            "border: 1px solid #0e0e0c; border-radius: 0; "
            "padding: 0 22px; font-family: 'Inter', sans-serif; "
            "font-size: 11px; font-weight: 800; letter-spacing: 2px; } "
            "QPushButton:hover { background-color: #c9302c; "
            "border: 1px solid #c9302c; }"
        )
        olustur_btn.setFixedHeight(46)
        olustur_btn.setMinimumWidth(170)
        olustur_btn.setCursor(Qt.PointingHandCursor)
        olustur_btn.clicked.connect(self._odunc_ver)

        btn_sarici = QVBoxLayout()
        btn_sarici.addStretch()
        btn_sarici.addWidget(olustur_btn)
        btn_sarici.addSpacing(20)
        header_satir.addLayout(btn_sarici)

        ana.addLayout(header_satir)

        # Filtre
        filtre = QHBoxLayout()
        filtre.setSpacing(12)

        self.arama = QLineEdit()
        self.arama.setObjectName("AramaInput")
        self.arama.setPlaceholderText("ARA  ·  Kitap, üye ya da işlem no...")
        self.arama.setFixedHeight(44)
        self.arama.textChanged.connect(self.yenile)
        filtre.addWidget(self.arama, 1)

        self.durum_filtre = QComboBox()
        self.durum_filtre.addItem("TÜMÜ", "tumu")
        self.durum_filtre.addItem("AKTİF", "aktif")
        self.durum_filtre.addItem("GECİKMİŞ", "gecikmis")
        self.durum_filtre.addItem("İADE EDİLDİ", "iade")
        self.durum_filtre.setFixedHeight(44)
        self.durum_filtre.setMinimumWidth(180)
        self.durum_filtre.currentIndexChanged.connect(self.yenile)
        filtre.addWidget(self.durum_filtre)

        ana.addLayout(filtre)

        # Tablo
        self.tablo = QTableWidget(0, 6)
        self.tablo.setHorizontalHeaderLabels(
            ["NO.", "KİTAP", "OKUR", "ÖDÜNÇ TARİHİ", "DURUM", "İŞLEM"]
        )
        self.tablo.verticalHeader().setVisible(False)
        self.tablo.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tablo.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tablo.setShowGrid(False)
        self.tablo.setFocusPolicy(Qt.NoFocus)
        self.tablo.setAlternatingRowColors(True)

        h = self.tablo.horizontalHeader()
        h.setSectionResizeMode(0, QHeaderView.Fixed)
        h.setSectionResizeMode(1, QHeaderView.Stretch)
        h.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        h.setSectionResizeMode(3, QHeaderView.Fixed)
        h.setSectionResizeMode(4, QHeaderView.Fixed)
        h.setSectionResizeMode(5, QHeaderView.Fixed)
        self.tablo.setColumnWidth(0, 80)
        self.tablo.setColumnWidth(3, 140)
        self.tablo.setColumnWidth(4, 170)
        self.tablo.setColumnWidth(5, 130)

        ana.addWidget(self.tablo, 1)

    def yenile(self):
        filtre = self.arama.text().strip().lower()
        durum_filtre = self.durum_filtre.currentData()

        oduncler = self.vy.tum_oduncler()

        if durum_filtre == "aktif":
            oduncler = [o for o in oduncler if o.aktif_mi()]
        elif durum_filtre == "gecikmis":
            oduncler = [o for o in oduncler if o.gecikme_var_mi()]
        elif durum_filtre == "iade":
            oduncler = [o for o in oduncler if not o.aktif_mi()]

        if filtre:
            filtrelenen = []
            for o in oduncler:
                k = self.vy.kitap_getir(o.kitap_id)
                u = self.vy.uye_getir(o.uye_id)
                metin = f"{o.odunc_id} {k.ad if k else ''} {u.ad if u else ''} {u.email if u else ''}".lower()
                if filtre in metin:
                    filtrelenen.append(o)
            oduncler = filtrelenen

        self.tablo.setRowCount(len(oduncler))

        for satir, o in enumerate(oduncler):
            kitap = self.vy.kitap_getir(o.kitap_id)
            uye = self.vy.uye_getir(o.uye_id)

            # Numara - serif büyük
            no_lbl = QLabel(f"{o.odunc_id:03d}")
            no_lbl.setStyleSheet(
                "color: #a5a59c; "
                "font-family: 'Playfair Display', 'Georgia', serif; "
                "font-size: 18px; font-weight: 900; letter-spacing: -0.5px; "
                "padding-left: 14px; "
                "background: transparent; border: none;"
            )
            no_lbl.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            self.tablo.setCellWidget(satir, 0, no_lbl)

            # Kitap (serif)
            kitap_lbl = QLabel(kitap.ad if kitap else "?")
            kitap_lbl.setStyleSheet(
                "color: #0e0e0c; "
                "font-family: 'Playfair Display', 'Georgia', serif; "
                "font-size: 14px; font-weight: 700; "
                "padding-left: 14px; padding-right: 14px; "
                "background: transparent; border: none;"
            )
            self.tablo.setCellWidget(satir, 1, kitap_lbl)

            # Üye
            uye_item = QTableWidgetItem(uye.ad if uye else "?")
            uye_item.setForeground(QColor("#3d3d3a"))
            f = QFont("Inter", 11)
            uye_item.setFont(f)
            self.tablo.setItem(satir, 2, uye_item)

            # Tarih
            tarih_item = QTableWidgetItem(o.odunc_tarihi.strftime("%d.%m.%Y"))
            tarih_item.setForeground(QColor("#7a7a72"))
            f = QFont("Inter", 11)
            tarih_item.setFont(f)
            self.tablo.setItem(satir, 3, tarih_item)

            # Durum
            if not o.aktif_mi():
                iade_str = o.iade_tarihi.strftime("%d.%m.%y")
                rozet = Rozet(f"İADE  {iade_str}", "notr")
            elif o.gecikme_var_mi():
                gun = abs(o.kalan_gun())
                rozet = Rozet(f"GECİKTİ {gun}G", "tehlike")
            elif o.kalan_gun() <= 3:
                rozet = Rozet(f"SON {o.kalan_gun()} GÜN", "uyari")
            else:
                rozet = Rozet(f"{o.kalan_gun()} GÜN", "basari")
            self.tablo.setCellWidget(satir, 4, HucreSarmalayici(rozet))

            # İşlem - sadece aktiflerde "İade Al"
            if o.aktif_mi():
                iade_btn = QPushButton("İADE AL")
                iade_btn.setStyleSheet(
                    "QPushButton { background-color: transparent; "
                    "color: #0e0e0c; "
                    "border: 1px solid #0e0e0c; "
                    "border-radius: 0; "
                    "padding-left: 12px; padding-right: 12px; "
                    "font-family: 'Inter', sans-serif; "
                    "font-size: 10px; font-weight: 800; letter-spacing: 1.5px; } "
                    "QPushButton:hover { background-color: #0e0e0c; color: #fdfdfb; }"
                )
                iade_btn.setFixedHeight(30)
                iade_btn.setFixedWidth(96)
                iade_btn.setCursor(Qt.PointingHandCursor)
                iade_btn.clicked.connect(lambda _, oid=o.odunc_id: self._iade_al(oid))
                self.tablo.setCellWidget(satir, 5, ButonGrubu([iade_btn]))
            else:
                bos = QLabel("—")
                bos.setStyleSheet(
                    "color: #cfcec5; font-size: 16px; "
                    "background: transparent; border: none;"
                )
                bos.setAlignment(Qt.AlignCenter)
                self.tablo.setCellWidget(satir, 5, HucreSarmalayici(bos))

            self.tablo.setRowHeight(satir, 56)

    def _odunc_ver(self):
        if not self.vy.musait_kitaplar():
            QMessageBox.warning(self, "Müsait Kitap Yok",
                                "Şu anda ödünç verilebilecek müsait kitap yok.")
            return
        if not self.vy.tum_uyeler():
            QMessageBox.warning(self, "Üye Yok",
                                "Önce en az bir üye eklemelisiniz.")
            return

        d = OduncVerDiyalog(self.vy, parent=self)
        if d.exec_():
            self.yenile()
            self.veri_degisti.emit()

    def _iade_al(self, odunc_id: int):
        o = self.vy.odunc_getir(odunc_id)
        if not o:
            return
        kitap = self.vy.kitap_getir(o.kitap_id)
        uye = self.vy.uye_getir(o.uye_id)

        cevap = QMessageBox.question(
            self, "İade Al",
            f"'{kitap.ad if kitap else ''}' kitabını {uye.ad if uye else ''} "
            f"üyesinden geri almak istiyor musunuz?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes,
        )
        if cevap == QMessageBox.Yes:
            try:
                self.vy.iade_et(odunc_id)
                self.yenile()
                self.veri_degisti.emit()
                QMessageBox.information(
                    self, "İade Alındı",
                    f"'{kitap.ad if kitap else ''}' kitabı başarıyla iade alındı.",
                )
            except ValueError as e:
                QMessageBox.warning(self, "Hata", str(e))
