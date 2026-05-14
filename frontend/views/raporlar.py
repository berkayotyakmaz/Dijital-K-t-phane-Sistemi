"""
Raporlar Sayfası - Editorial yıllık rapor.

CSV export'ta formula injection koruması: =, +, -, @, \\t, \\r ile başlayan
hücrelere ' ön eki konur (Excel/LibreOffice'in formula çalıştırmasını engeller).
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


# Excel/LibreOffice/Google Sheets formula injection için tehlikeli karakterler
# Bir hücre bu karakterlerden biriyle başlarsa formula olarak değerlendirilir.
_CSV_TEHLIKELI = ("=", "+", "-", "@", "\t", "\r")


def _csv_guvenli(deger) -> str:
    """Bir değeri CSV hücresi için güvenli string'e çevirir.

    Formula injection saldırılarını engellemek için tehlikeli karakterle
    başlayan değerlerin önüne tek tırnak (') ekler. None -> ''.
    """
    if deger is None:
        return ""
    s = str(deger)
    if s and s[0] in _CSV_TEHLIKELI:
        return "'" + s
    return s


class RaporlarSayfasi(QWidget):
    def __init__(self, vy: VeriYoneticisi, parent=None):
        super().__init__(parent)
        self.vy = vy
        self._arayuz_olustur()
        self.yenile()

    def _arayuz_olustur(self):
        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setStyleSheet("background-color: #fdfdfb; border: none;")

        ic = QWidget()
        scroll.setWidget(ic)

        ana = QVBoxLayout(ic)
        ana.setContentsMargins(48, 36, 48, 32)
        ana.setSpacing(28)

        header_satir = QHBoxLayout()
        header_satir.setSpacing(20)

        self.header = EditorialHeader(
            kategori="RAPORLAR",
            baslik="Genel Rapor",
            altyazi="Kütüphane istatistikleri ve dolaşım analizi.",
            sag_etiket="DETAY",
        )
        header_satir.addWidget(self.header, 1)

        # CSV indirme - PrimaryButon tema'dan
        export_btn = QPushButton("⬇  TÜM VERİLERİ CSV OLARAK İNDİR")
        export_btn.setObjectName("PrimaryButon")
        export_btn.setStyleSheet(
            "QPushButton { background-color: #0e0e0c; color: #fdfdfb; "
            "border: 1px solid #0e0e0c; border-radius: 0; "
            "padding: 0 22px; font-family: 'Inter', sans-serif; "
            "font-size: 11px; font-weight: 800; letter-spacing: 2px; } "
            "QPushButton:hover { background-color: #c9302c; "
            "border: 1px solid #c9302c; color: #fdfdfb; } "
            "QPushButton:pressed { background-color: #9a1f1c; "
            "border: 1px solid #9a1f1c; color: #fdfdfb; }"
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

        # 4 metrik
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

        alt = QHBoxLayout()
        alt.setSpacing(16)

        kategori_kart = Kart(
            "Kategori Dağılımı",
            "Koleksiyondaki kitapların kategorilere göre dağılımı.",
        )
        self.kategori_widget = QWidget()
        kategori_layout = QVBoxLayout(self.kategori_widget)
        kategori_layout.setContentsMargins(0, 0, 0, 0)
        kategori_kart.layout.addWidget(self.kategori_widget)
        alt.addWidget(kategori_kart, 1)

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
        f = QFrame()
        f.setStyleSheet(
            "QFrame { background-color: #fdfdfb; "
            "border-bottom: 1px solid #e8e7df; }"
        )

        layout = QHBoxLayout(f)
        layout.setContentsMargins(4, 12, 4, 12)
        layout.setSpacing(14)

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

        layout.addWidget(MuhurAvatar(uye.ad, boyut=36))

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

        def yaz(satir):
            """Satırdaki tüm hücreleri _csv_guvenli'den geçirip yazar."""
            return [_csv_guvenli(x) for x in satir]

        try:
            with open(dosya_yolu, "w", newline="", encoding="utf-8-sig") as f:
                w = csv.writer(f)
                stats = self.vy.genel_istatistikler()

                w.writerow(yaz(["THE LIBRARY — YILLIK RAPOR"]))
                w.writerow([])
                w.writerow(yaz(["Toplam Kitap", stats["toplam_kitap"]]))
                w.writerow(yaz(["Müsait", stats["musait_kitap"]]))
                w.writerow(yaz(["Ödünçte", stats["odunc_kitap"]]))
                w.writerow(yaz(["Toplam Üye", stats["toplam_uye"]]))
                w.writerow(yaz(["Aktif Ödünç", stats["aktif_odunc"]]))
                w.writerow(yaz(["Geciken", stats["gecikmis_odunc"]]))
                w.writerow(yaz(["Toplam İşlem", stats["toplam_islem"]]))
                w.writerow(yaz(["Kullanım Oranı", f"%{stats['kullanim_orani']}"]))
                w.writerow([])

                w.writerow(yaz(["KATEGORI DAĞILIMI"]))
                for k, v in sorted(self.vy.kategori_dagilim().items(),
                                   key=lambda x: -x[1]):
                    w.writerow(yaz([k, v]))
                w.writerow([])

                w.writerow(yaz([
                    "İşlem No", "Kitap", "Yazar", "Okur", "E-posta",
                    "Ödünç Tarihi", "Son Teslim", "İade Tarihi", "Durum"
                ]))
                # Silinmiş kitap/üye olsa bile kaydı atlamayalım - tarihçe önemli
                for o in self.vy.tum_oduncler():
                    k = self.vy.kitap_getir(o.kitap_id)
                    u = self.vy.uye_getir(o.uye_id)
                    if not o.aktif_mi():
                        durum = "İade Edildi"
                    elif o.gecikme_var_mi():
                        durum = f"Gecikmiş ({abs(o.kalan_gun())} gün)"
                    else:
                        durum = f"Aktif ({o.kalan_gun()} gün)"
                    w.writerow(yaz([
                        o.odunc_id,
                        k.ad if k else "(silinmiş kitap)",
                        k.yazar if k else "",
                        u.ad if u else "(silinmiş üye)",
                        u.email if u else "",
                        o.odunc_tarihi.strftime("%d.%m.%Y"),
                        o.son_teslim_tarihi.strftime("%d.%m.%Y"),
                        o.iade_tarihi.strftime("%d.%m.%Y") if o.iade_tarihi else "",
                        durum,
                    ]))

            QMessageBox.information(
                self, "Başarılı", f"Rapor kaydedildi:\n{dosya_yolu}"
            )
        except Exception as ex:
            QMessageBox.critical(self, "Hata", f"Dosya kaydedilemedi:\n{ex}")
