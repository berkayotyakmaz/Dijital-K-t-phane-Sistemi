"""
Otomatik seed - Boş veritabanını örnek kitap, üye ve ödünç ile doldurur.
"""
from datetime import datetime, timedelta

from .veri_yoneticisi import VeriYoneticisi


def seed_gerekli_mi(vy: VeriYoneticisi) -> bool:
    return (
        len(vy.tum_kitaplar()) == 0
        and len(vy.tum_uyeler()) == 0
        and len(vy.tum_oduncler()) == 0
    )


def seed_uygula(vy: VeriYoneticisi) -> None:
    """Boş bir VeriYoneticisi'ye örnek kütüphane verileri yükler."""

    # KİTAPLAR
    kitaplar = [
        ("Suç ve Ceza", "Fyodor Dostoyevski", "Roman"),
        ("1984", "George Orwell", "Distopya"),
        ("Sapiens: İnsanlığın Kısa Tarihi", "Yuval Noah Harari", "Tarih"),
        ("Dune", "Frank Herbert", "Bilim Kurgu"),
        ("Şeker Portakalı", "José Mauro de Vasconcelos", "Roman"),
        ("Cosmos", "Carl Sagan", "Bilim"),
        ("Küçük Prens", "Antoine de Saint-Exupéry", "Çocuk"),
        ("Yüzüklerin Efendisi", "J. R. R. Tolkien", "Fantastik"),
        ("Tutunamayanlar", "Oğuz Atay", "Roman"),
        ("Kürk Mantolu Madonna", "Sabahattin Ali", "Roman"),
        ("Bir Bilim Adamının Romanı", "Oğuz Atay", "Biyografi"),
        ("Hayvan Çiftliği", "George Orwell", "Distopya"),
        ("Yabancı", "Albert Camus", "Felsefe"),
        ("Beyaz Diş", "Jack London", "Roman"),
        ("Kısa Hikayeler", "Anton Çehov", "Hikaye"),
        ("Zaman Makinesi", "H. G. Wells", "Bilim Kurgu"),
        ("Drakula", "Bram Stoker", "Korku"),
        ("Bir Ömür Nasıl Yaşanır", "İlber Ortaylı", "Tarih"),
        ("Ahir Zaman Çocukları", "İskender Pala", "Roman"),
        ("Olağanüstü Bir Gece", "Stefan Zweig", "Roman"),
        ("Beyaz Geceler", "Fyodor Dostoyevski", "Roman"),
        ("Anna Karenina", "Lev Tolstoy", "Roman"),
        ("Sefiller", "Victor Hugo", "Roman"),
        ("Don Kişot", "Miguel de Cervantes", "Roman"),
        ("Madame Bovary", "Gustave Flaubert", "Roman"),
        ("Bilinçli Tasarım", "Stephen Hawking", "Bilim"),
        ("Tao Te Ching", "Lao Tzu", "Felsefe"),
        ("Otostopçunun Galaksi Rehberi", "Douglas Adams", "Bilim Kurgu"),
        ("Cesur Yeni Dünya", "Aldous Huxley", "Distopya"),
        ("Fareler ve İnsanlar", "John Steinbeck", "Roman"),
    ]
    kitap_objs = [vy.kitap_ekle(ad, yazar, kategori) for ad, yazar, kategori in kitaplar]

    # ÜYELER
    uyeler = [
        ("Beko Yılmaz", "beko.yilmaz@gmail.com"),
        ("Ali Demir", "ali.demir@hotmail.com"),
        ("Ayşe Kaya", "ayse.kaya@outlook.com"),
        ("Mehmet Şahin", "mehmet.sahin@gmail.com"),
        ("Zeynep Arslan", "zeynep.arslan@yahoo.com"),
        ("Can Öztürk", "can.ozturk@protonmail.com"),
        ("Selin Yıldız", "selin.yildiz@gmail.com"),
        ("Murat Koç", "murat.koc@outlook.com"),
        ("Elif Çelik", "elif.celik@gmail.com"),
        ("Burak Aydın", "burak.aydin@hotmail.com"),
        ("Deniz Kara", "deniz.kara@gmail.com"),
        ("Ece Yıldırım", "ece.yildirim@outlook.com"),
        ("Kerem Aksoy", "kerem.aksoy@gmail.com"),
        ("Pınar Doğan", "pinar.dogan@yahoo.com"),
        ("Tolga Erdem", "tolga.erdem@gmail.com"),
    ]
    uye_objs = [vy.uye_ekle(ad, email) for ad, email in uyeler]

    # ÖDÜNÇ İŞLEMLERİ - bazıları aktif, bazıları iade edilmiş, bazıları gecikmiş
    odunc_planlari = [
        # (kitap_idx, uye_idx, kac_gun_once_alindi, iade_edildi_mi, kac_gun_sonra_iade)
        (0, 0, 5, False, None),     # Suç ve Ceza - Beko, 5 gün önce, aktif
        (1, 1, 3, False, None),     # 1984 - Ali, aktif
        (2, 2, 8, False, None),     # Sapiens - Ayşe, aktif
        (3, 0, 2, False, None),     # Dune - Beko, aktif (Beko 2 kitap)
        (5, 4, 18, False, None),    # Cosmos - Zeynep, GECİKMİŞ (>14 gün)
        (7, 3, 20, False, None),    # Yüzüklerin Efendisi - Mehmet, GECİKMİŞ
        (8, 5, 6, False, None),     # Tutunamayanlar - Can, aktif

        # İade edilmiş geçmiş kayıtlar
        (4, 1, 30, True, 25),       # Şeker Portakalı - Ali, iade edildi
        (6, 6, 25, True, 18),       # Küçük Prens - Selin, iade edildi
        (9, 7, 40, True, 28),       # Kürk Mantolu Madonna - Murat, iade edildi
        (10, 8, 35, True, 23),      # Bir Bilim Adamı - Elif
        (11, 9, 45, True, 35),      # Hayvan Çiftliği - Burak
        (12, 0, 60, True, 50),      # Yabancı - Beko (geçmiş)
        (13, 10, 22, True, 14),     # Beyaz Diş - Deniz
        (14, 11, 50, True, 40),     # Kısa Hikayeler - Ece
        (1, 2, 80, True, 65),       # 1984 - Ayşe (geçmiş)
        (2, 5, 75, True, 60),       # Sapiens - Can (geçmiş)
        (15, 12, 33, True, 26),     # Zaman Makinesi - Kerem
        (16, 13, 28, True, 19),     # Drakula - Pınar
    ]

    simdi = datetime.now()

    for plan in odunc_planlari:
        kitap_idx, uye_idx, kac_gun_once, iade_edildi, kac_gun_sonra = plan
        kitap = kitap_objs[kitap_idx]
        uye = uye_objs[uye_idx]

        # Kitap aktif olarak başka birinde mi kontrol et
        if not kitap.musait_mi():
            continue

        try:
            odunc = vy.odunc_ver(kitap.kitap_id, uye.uye_id)
        except ValueError:
            continue

        # Tarihleri geriye al
        odunc.odunc_tarihi = simdi - timedelta(days=kac_gun_once)
        odunc.son_teslim_tarihi = odunc.odunc_tarihi + timedelta(days=14)

        if iade_edildi and kac_gun_sonra is not None:
            # İade işlemini geriye doğru yap
            odunc.iade_tarihi = odunc.odunc_tarihi + timedelta(days=kac_gun_sonra)
            # Kitap durumunu model metodu üzerinden güncelle (validation korunur)
            kitap.kitap_durumu_degistir("musait")

    vy.kaydet()
