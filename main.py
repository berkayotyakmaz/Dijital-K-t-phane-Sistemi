"""
LibraryHub - Dijital Kütüphane Yönetim Sistemi
================================================

Çalıştırma:
    python main.py

Gereksinimler:
    pip install PyQt5

Varsayılan Giriş:
    Kullanıcı adı: admin
    Şifre:        admin123

Geliştirici: Beko
"""
import sys
import os

from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from backend import (
    VeriYoneticisi,
    AuthYoneticisi,
    seed_gerekli_mi,
    seed_uygula,
)
from frontend.ana_pencere import AnaPencere
from frontend.login import LoginPenceresi


def main():
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    app = QApplication(sys.argv)
    app.setApplicationName("LibraryHub - Dijital Kütüphane")
    app.setStyle("Fusion")

    from frontend.tema import ANA_STIL
    app.setStyleSheet(ANA_STIL)

    font = QFont("Segoe UI", 10)
    app.setFont(font)

    veri_klasoru = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "data"
    )
    os.makedirs(veri_klasoru, exist_ok=True)

    # Auth
    auth = AuthYoneticisi(os.path.join(veri_klasoru, "kullanicilar.json"))
    if not auth.kullanici_var_mi():
        auth.varsayilan_kullanici_olustur()
        print("[Auth] Varsayılan kullanıcı oluşturuldu (admin / admin123)")

    # Login
    login = LoginPenceresi(auth)
    if login.exec_() != QDialog.Accepted:
        sys.exit(0)

    aktif_kullanici = login.dogrulanan_kullanici
    print(f"[Auth] Giriş başarılı: {aktif_kullanici.ad}")

    # Veri yöneticisi
    vy = VeriYoneticisi(veri_klasoru=veri_klasoru)

    if seed_gerekli_mi(vy):
        print("[Seed] Veritabanı boş, örnek veriler yükleniyor...")
        seed_uygula(vy)
        print(f"[Seed] {len(vy.tum_kitaplar())} kitap, "
              f"{len(vy.tum_uyeler())} üye, "
              f"{len(vy.tum_oduncler())} ödünç kaydı eklendi.")

    pencere = AnaPencere(vy, aktif_kullanici=aktif_kullanici)
    pencere.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
