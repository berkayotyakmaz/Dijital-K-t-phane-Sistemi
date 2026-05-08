"""
Raporlar Sayfası - Editorial yıllık rapor.
"""
import csv
from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QLabel,
    QPushButton,
    QFrame,
    QFileDialog,
    QMessageBox,
    QScrollArea,
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor

from backend import VeriYoneticisi
from frontend.widgets.bilesenler import (
    EditorialHeader,
    Kart,
    MetrikKart,
    KategoriBarYatay,
    MuhurAvatar,
    Ayirici,
    AyiriciInce,
)


class RaporlarSayfasi(QWidget):
    def __init__(self, vy: VeriYoneticisi, parent=None):
        super().__init__(parent)
        self.vy = vy
        self._arayuz_olustur()
        self.yenile()

    def _arayuz_olustur(self):
        # Scroll
        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setStyleSheet("background-color: #fdfdfb; border: none;")

        ic = QWidget()
        scroll.setWidget(ic)

        ana = QVBoxLayout(ic)
        ana.setContentsMargins(48, 36, 48, 32)
        ana.setSpacing(28)

        # Header satırı
        header_satir = QHBoxLayout()
        header_satir.setSpacing(20)

        self.header = EditorialHeader(
            kategori="RAPORLAR",
            baslik="Genel Rapor",
            altyazi="Kütüphane istatistikleri ve dolaşım analizi.",
            sag_etiket="DETAY",
        )
        header_satir.addWidget(self.header, 1)

        # CSV indirme butonu
        export_btn = QPushButton("⬇  TÜM VERİLERİ CSV OLARAK İNDİR")
        export_btn.setObjectName("IkincilButon")
        export_btn.setStyleSheet(
            "QPushButton { background-color: #0e0e0c; color: #fdfdfb; "
            "border: 1px solid #0e0e0c; border-radius: 0; "
            "padding: 0 22px; font-family: 'Inter', sans-serif; "
            "font-size: 11px; font-weight: 800; letter-spacing: 2px; } "
            "QPushButton:hover { background-color: #c9302c; "
            "border: 1px solid #c9302c; }"
        )
        export_btn.setFixedHeight(46)
        export_btn.setMinimumWidth(280)
        export_btn.setCursor(Qt.PointingHandCursor)
        export_btn.clicked.connect(self._csv_export)

        btn_sarici = QVBoxLayout()
        btn_sarici.addStretch()
        btn_sarici.addWidget(export_btn)
        btn_sarici.addSpacing(20)
        header_satir.addLayout(btn_sarici)

        ana.addLayout(header_satir)

        # 4 büyük rakam blok
        grid = QGridLayout()
        grid.setSpacing(16)

        self.blok_kitap = MetrikKart("Toplam Kitap", "0", "Koleksiyon hacmi.")
        self.blok_uye = MetrikKart("Toplam Üye", "0", "Aktif okurlar.")
        self.blok_islem = MetrikKart("Toplam İşlem", "0", "Tüm zamanlar.")
        self.blok_oran = MetrikKart("Kullanım", "%0", "Anlık dolaşım oranı.", accent=True)

        grid.addWidget(self.blok_kitap, 0, 0)
        grid.addWidget(self.blok_uye, 0, 1)
        grid.addWidget(self.blok_islem, 0, 2)
        grid.addWidget(self.blok_oran, 0, 3)
        ana.addLayout(grid)

        # Alt: kategori dağılımı + en aktif okurlar
        alt = QHBoxLayout()
        alt.setSpacing(16)

        # Sol: Kategori Dağılımı
        kategori_kart = Kart(
            "Kategori Dağılımı",
            "Koleksiyondaki kitapların kategorilere göre dağılımı.",
        )
        self.kategori_widget = QWidget()
        kategori_layout = QVBoxLayout(self.kategori_widget)
        kategori_layout.setContentsMargins(0, 0, 0, 0)
        kategori_kart.layout.addWidget(self.kategori_widget)
        alt.addWidget(kategori_kart, 1)

        # Sağ: En Aktif Okurlar
        aktif_kart = Kart(
            "En Aktif Okurlar",
            "Tüm zamanlarda en çok ödünç alan beş üye.",
            accent=True,
        )
        self.aktif_uyeler_widget = QWidget()
        self.aktif_uyeler_layout = QVBoxLayout(self.aktif_uyeler_widget)
        self.aktif_uyeler_layout.setContentsMargins(0, 0, 0, 0)
        self.aktif_uyeler_layout.setSpacing(8)
        aktif_kart.layout.addWidget(self.aktif_uyeler_widget)
        alt.addWidget(aktif_kart, 1)

        ana.addLayout(alt)

        ana.addStretch()

        dis_layout = QVBoxLayout(self)
        dis_layout.setContentsMargins(0, 0, 0, 0)
        dis_layout.addWidget(scroll)

    def _layout_temizle(self, layout):
        """Layout'tan tüm widget ve spacer'ları çıkarır."""
        while layout.count():
            item = layout.takeAt(0)
            w = item.widget()
            if w is not None:
                w.setParent(None)
                w.deleteLater()

    def yenile(self):
        stats = self.vy.genel_istatistikler()

        self.blok_kitap.deger_ayarla(stats["toplam_kitap"])
        self.blok_kitap.altyazi_ayarla(
            f"{stats['musait_kitap']} müsait, {stats['odunc_kitap']} ödünçte."
        )

        self.blok_uye.deger_ayarla(stats["toplam_uye"])

        self.blok_islem.deger_ayarla(stats["toplam_islem"])
        self.blok_islem.altyazi_ayarla(
            f"{stats['aktif_odunc']} aktif, {stats['gecikmis_odunc']} geciken."
        )

        self.blok_oran.deger_ayarla(f"%{stats['kullanim_orani']}")

        # Kategori dağılım
        self._layout_temizle(self.kategori_widget.layout())
        dagilim = self.vy.kategori_dagilim()
        if dagilim:
            self.kategori_widget.layout().addWidget(KategoriBarYatay(dagilim))
            self.kategori_widget.layout().addStretch()
        else:
            bos = QLabel("— Henüz kayıtlı kitap yok. —")
            bos.setStyleSheet(
                "color: #7a7a72; "
                "font-family: 'Playfair Display', 'Georgia', serif; "
                "font-style: italic; padding: 30px; "
                "background: transparent; border: none;"
            )
            bos.setAlignment(Qt.AlignCenter)
            self.kategori_widget.layout().addWidget(bos)

        # En aktif okurlar
        self._layout_temizle(self.aktif_uyeler_layout)

        sayim = {}
        for o in self.vy.tum_oduncler():
            sayim[o.uye_id] = sayim.get(o.uye_id, 0) + 1

        sirali = sorted(sayim.items(), key=lambda x: -x[1])[:5]

        if not sirali:
            bos = QLabel("— Henüz işlem kaydı yok. —")
            bos.setStyleSheet(
                "color: #7a7a72; "
                "font-family: 'Playfair Display', 'Georgia', serif; "
                "font-style: italic; padding: 30px; "
                "background: transparent; border: none;"
            )
            bos.setAlignment(Qt.AlignCenter)
            self.aktif_uyeler_layout.addWidget(bos)
        else:
            for sira, (uye_id, sayi) in enumerate(sirali, 1):
                u = self.vy.uye_getir(uye_id)
                if not u:
                    continue
                self.aktif_uyeler_layout.addWidget(
                    self._uye_satiri(sira, u, sayi)
                )

        self.aktif_uyeler_layout.addStretch()

    def _uye_satiri(self, sira: int, uye, sayi: int) -> QFrame:
        """Editorial okur satırı: gazete sıra no + mühür + ad + ödünç."""
        f = QFrame()
        f.setStyleSheet(
            "QFrame { background-color: #fdfdfb; "
            "border-bottom: 1px solid #e8e7df; }"
        )

        layout = QHBoxLayout(f)
        layout.setContentsMargins(4, 12, 4, 12)
        layout.setSpacing(14)

        # Sıra no - büyük serif rakam
        no_lbl = QLabel(f"{sira:02d}")
        no_lbl.setFixedWidth(40)
        no_lbl.setStyleSheet(
            "color: #c9302c; "
            "font-family: 'Playfair Display', 'Georgia', serif; "
            "font-size: 28px; font-weight: 900; letter-spacing: -1px; "
            "background: transparent; border: none;"
        )
        no_lbl.setAlignment(Qt.AlignCenter)
        layout.addWidget(no_lbl)

        # Mühür avatar
        layout.addWidget(MuhurAvatar(uye.ad, boyut=36))

        # Ad + email
        bilgi = QVBoxLayout()
        bilgi.setSpacing(2)
        bilgi.setContentsMargins(0, 0, 0, 0)

        ad = QLabel(uye.ad)
        ad.setStyleSheet(
            "color: #0e0e0c; "
            "font-family: 'Playfair Display', 'Georgia', serif; "
            "font-size: 14px; font-weight: 800; "
            "background: transparent; border: none;"
        )
        email = QLabel(uye.email)
        email.setStyleSheet(
            "color: #7a7a72; font-family: 'Inter', sans-serif; "
            "font-size: 10px; "
            "background: transparent; border: none;"
        )
        bilgi.addWidget(ad)
        bilgi.addWidget(email)
        layout.addLayout(bilgi, 1)

        # Sayı (büyük serif)
        sayi_kutu = QVBoxLayout()
        sayi_kutu.setSpacing(0)
        sayi_kutu.setContentsMargins(0, 0, 0, 0)

        sayi_lbl = QLabel(str(sayi))
        sayi_lbl.setStyleSheet(
            "color: #0e0e0c; "
            "font-family: 'Playfair Display', 'Georgia', serif; "
            "font-size: 24px; font-weight: 900; letter-spacing: -0.5px; "
            "background: transparent; border: none;"
        )
        sayi_lbl.setAlignment(Qt.AlignRight)

        etiket = QLabel("ÖDÜNÇ")
        etiket.setStyleSheet(
            "color: #7a7a72; font-family: 'Inter', sans-serif; "
            "font-size: 8px; font-weight: 800; letter-spacing: 1.8px; "
            "background: transparent; border: none;"
        )
        etiket.setAlignment(Qt.AlignRight)

        sayi_kutu.addWidget(sayi_lbl)
        sayi_kutu.addWidget(etiket)
        layout.addLayout(sayi_kutu)

        return f

    def _csv_export(self):
        dosya_yolu, _ = QFileDialog.getSaveFileName(
            self, "CSV Olarak Kaydet",
            "the_library_raporu.csv", "CSV Dosyaları (*.csv)"
        )
        if not dosya_yolu:
            return

        try:
            with open(dosya_yolu, "w", newline="", encoding="utf-8-sig") as f:
                w = csv.writer(f)
                stats = self.vy.genel_istatistikler()

                w.writerow(["THE LIBRARY — YILLIK RAPOR"])
                w.writerow([])
                w.writerow(["Toplam Kitap", stats["toplam_kitap"]])
                w.writerow(["Müsait", stats["musait_kitap"]])
                w.writerow(["Ödünçte", stats["odunc_kitap"]])
                w.writerow(["Toplam Üye", stats["toplam_uye"]])
                w.writerow(["Aktif Ödünç", stats["aktif_odunc"]])
                w.writerow(["Geciken", stats["gecikmis_odunc"]])
                w.writerow(["Toplam İşlem", stats["toplam_islem"]])
                w.writerow(["Kullanım Oranı", f"%{stats['kullanim_orani']}"])
                w.writerow([])

                w.writerow(["KATEGORI DAĞILIMI"])
                for k, v in sorted(self.vy.kategori_dagilim().items(),
                                   key=lambda x: -x[1]):
                    w.writerow([k, v])
                w.writerow([])

                w.writerow(["TÜM ÖDÜNÇ KAYITLARI"])
                w.writerow([
                    "İşlem No", "Kitap", "Yazar", "Okur", "E-posta",
                    "Ödünç Tarihi", "Son Teslim", "İade Tarihi", "Durum"
                ])
                for o in self.vy.tum_oduncler():
                    k = self.vy.kitap_getir(o.kitap_id)
                    u = self.vy.uye_getir(o.uye_id)
                    if not k or not u:
                        continue
                    if not o.aktif_mi():
                        durum = "İade Edildi"
                    elif o.gecikme_var_mi():
                        durum = f"Gecikmiş ({abs(o.kalan_gun())} gün)"
                    else:
                        durum = f"Aktif ({o.kalan_gun()} gün)"
                    w.writerow([
                        o.odunc_id, k.ad, k.yazar, u.ad, u.email,
                        o.odunc_tarihi.strftime("%d.%m.%Y"),
                        o.son_teslim_tarihi.strftime("%d.%m.%Y"),
                        o.iade_tarihi.strftime("%d.%m.%Y") if o.iade_tarihi else "",
                        durum,
                    ])

            QMessageBox.information(
                self, "Başarılı", f"Rapor kaydedildi:\n{dosya_yolu}"
            )
        except Exception as ex:
            QMessageBox.critical(self, "Hata", f"Dosya kaydedilemedi:\n{ex}")
