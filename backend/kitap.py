"""
Kitap sınıfı.
"""


class Kitap:
    """
    Kütüphanedeki bir kitabı temsil eder.

    Attributes:
        kitap_id (int)
        ad (str)
        yazar (str)
        kategori (str)
        durum (str): "musait" | "odunc"
    """

    GECERLI_DURUMLAR = ("musait", "odunc")

    # Karakter sınırları - JSON şişmesini ve UI taşmasını engeller
    MAX_AD = 120
    MAX_YAZAR = 80
    MAX_KATEGORI = 40

    def __init__(self, kitap_id: int, ad: str, yazar: str, kategori: str,
                 durum: str = "musait"):
        ad = (ad or "").strip()
        yazar = (yazar or "").strip()
        kategori = (kategori or "Genel").strip() or "Genel"

        if not ad:
            raise ValueError("Kitap adı boş olamaz.")
        if len(ad) > self.MAX_AD:
            raise ValueError(f"Kitap adı en fazla {self.MAX_AD} karakter olabilir.")
        if not yazar:
            raise ValueError("Yazar boş olamaz.")
        if len(yazar) > self.MAX_YAZAR:
            raise ValueError(f"Yazar en fazla {self.MAX_YAZAR} karakter olabilir.")
        if len(kategori) > self.MAX_KATEGORI:
            raise ValueError(f"Kategori en fazla {self.MAX_KATEGORI} karakter olabilir.")
        if durum not in self.GECERLI_DURUMLAR:
            raise ValueError(f"Geçersiz durum: {durum}")

        self.kitap_id = kitap_id
        self.ad = ad
        self.yazar = yazar
        self.kategori = kategori
        self.durum = durum

    def kitap_durumu_degistir(self, yeni_durum: str) -> None:
        if yeni_durum not in self.GECERLI_DURUMLAR:
            raise ValueError(f"Geçersiz durum: {yeni_durum}")
        self.durum = yeni_durum

    def musait_mi(self) -> bool:
        return self.durum == "musait"

    def to_dict(self) -> dict:
        return {
            "kitap_id": self.kitap_id,
            "ad": self.ad,
            "yazar": self.yazar,
            "kategori": self.kategori,
            "durum": self.durum,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "Kitap":
        return cls(
            kitap_id=d["kitap_id"],
            ad=d["ad"],
            yazar=d["yazar"],
            kategori=d.get("kategori", "Genel"),
            durum=d.get("durum", "musait"),
        )

    def __repr__(self) -> str:
        return f"Kitap(id={self.kitap_id}, ad='{self.ad}', durum='{self.durum}')"
