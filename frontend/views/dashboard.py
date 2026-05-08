"""
Dashboard / Kontrol Paneli - Sade editorial.
"""
from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QLabel,
    QFrame,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QAbstractItemView,
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor

from backend import VeriYoneticisi
from frontend.widgets.bilesenler import (
    EditorialHeader,
    Kart,
    Rozet,
    HucreSarmalayici,
    MetrikKart,
)


class DashboardSayfasi(QWidget):
    def __init__(self, vy: VeriYoneticisi, aktif_kullanici=None, parent=None):
        super().__init__(parent)
        self.vy = vy
        self.aktif_kullanici = aktif_kullanici
        self._arayuz_olustur()
        self.yenile()

    def _arayuz_olustur(self):
        ana = QVBoxLayout(self)
        ana.setContentsMargins(48, 36, 48, 32)
        ana.setSpacing(24)

        # Header
        self.header = EditorialHeader(
            kategori="DASHBOARD",
            baslik="Kontrol Paneli",
            altyazi="Kütüphanenin anlık durumu.",
            sag_etiket="GENEL BAKIŞ",
        )
        ana.addWidget(self.header)

        # 4 metric kart
        grid = QGridLayout()
        grid.setSpacing(16)

        self.kart_kitap = MetrikKart("Toplam Kitap", "0", "Koleksiyon hacmi.")
        self.kart_uye = MetrikKart("Kayıtlı Üye", "0", "Aktif okurlar.")
        self.kart_aktif = MetrikKart("Aktif Ödünç", "0", "Şu an dışarıda.")
        self.kart_geciken = MetrikKart("Geciken İade", "0", "Hatırlatma gerekli.", accent=True)

        grid.addWidget(self.kart_kitap, 0, 0)
        grid.addWidget(self.kart_uye, 0, 1)
        grid.addWidget(self.kart_aktif, 0, 2)
        grid.addWidget(self.kart_geciken, 0, 3)
        ana.addLayout(grid)

        # Aktif ödünç tablosu
        tablo_kart = Kart(
            "Aktif Ödünç İşlemleri",
            "Şu anda dışarıda olan kitaplar — son teslim tarihine göre.",
        )

        self.tablo = QTableWidget(0, 4)
        self.tablo.setHorizontalHeaderLabels(["KİTAP", "OKUR", "ÖDÜNÇ TARİHİ", "DURUM"])
        self.tablo.verticalHeader().setVisible(False)
        self.tablo.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tablo.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tablo.setShowGrid(False)
        self.tablo.setFocusPolicy(Qt.NoFocus)
        self.tablo.setAlternatingRowColors(True)

        h = self.tablo.horizontalHeader()
        h.setSectionResizeMode(0, QHeaderView.Stretch)
        h.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        h.setSectionResizeMode(2, QHeaderView.Fixed)
        h.setSectionResizeMode(3, QHeaderView.Fixed)
        self.tablo.setColumnWidth(2, 140)
        self.tablo.setColumnWidth(3, 170)

        self.tablo.setMinimumHeight(340)
        tablo_kart.layout.addWidget(self.tablo)

        ana.addWidget(tablo_kart, 1)

    def yenile(self):
        stats = self.vy.genel_istatistikler()

        self.kart_kitap.deger_ayarla(stats["toplam_kitap"])
        self.kart_kitap.altyazi_ayarla(
            f"{stats['musait_kitap']} müsait, {stats['odunc_kitap']} ödünçte."
        )

        self.kart_uye.deger_ayarla(stats["toplam_uye"])
        self.kart_uye.altyazi_ayarla("Kayıtlı okur sayısı.")

        self.kart_aktif.deger_ayarla(stats["aktif_odunc"])
        self.kart_aktif.altyazi_ayarla(f"Toplam {stats['toplam_islem']} işlem.")

        self.kart_geciken.deger_ayarla(stats["gecikmis_odunc"])
        if stats["gecikmis_odunc"] == 0:
            self.kart_geciken.altyazi_ayarla("Tüm iadeler zamanında.")
        else:
            self.kart_geciken.altyazi_ayarla("Gecikmiş okurlara haber verin.")

        # Aktif ödünç tablosu
        oduncler = sorted(
            self.vy.aktif_oduncler(),
            key=lambda o: o.kalan_gun(),
        )[:8]

        self.tablo.setRowCount(len(oduncler) if oduncler else 1)

        if not oduncler:
            bos = QTableWidgetItem("  Aktif ödünç bulunmuyor.")
            bos.setForeground(QColor("#7a7a72"))
            f = QFont("Playfair Display", 11)
            f.setItalic(True)
            bos.setFont(f)
            self.tablo.setSpan(0, 0, 1, 4)
            self.tablo.setItem(0, 0, bos)
            self.tablo.setRowHeight(0, 80)
            return

        for satir, o in enumerate(oduncler):
            kitap = self.vy.kitap_getir(o.kitap_id)
            uye = self.vy.uye_getir(o.uye_id)

            # Kitap (serif)
            kitap_item = QTableWidgetItem("  " + (kitap.ad if kitap else "?"))
            f = QFont("Playfair Display", 12)
            if not f.exactMatch():
                f = QFont("Georgia", 12)
            f.setBold(True)
            kitap_item.setFont(f)
            kitap_item.setForeground(QColor("#0e0e0c"))
            self.tablo.setItem(satir, 0, kitap_item)

            # Üye
            uye_item = QTableWidgetItem(uye.ad if uye else "?")
            uye_item.setForeground(QColor("#3d3d3a"))
            self.tablo.setItem(satir, 1, uye_item)

            # Tarih
            tarih_item = QTableWidgetItem(o.odunc_tarihi.strftime("%d.%m.%Y"))
            tarih_item.setForeground(QColor("#7a7a72"))
            self.tablo.setItem(satir, 2, tarih_item)

            # Durum rozeti
            kalan = o.kalan_gun()
            if kalan < 0:
                rozet = Rozet(f"GECİKTİ {abs(kalan)}G", "tehlike")
            elif kalan <= 3:
                rozet = Rozet(f"SON {kalan} GÜN", "uyari")
            else:
                rozet = Rozet(f"{kalan} GÜN", "basari")
            self.tablo.setCellWidget(satir, 3, HucreSarmalayici(rozet))

            self.tablo.setRowHeight(satir, 56)
