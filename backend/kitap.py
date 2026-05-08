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

    def __init__(self, kitap_id: int, ad: str, yazar: str, kategori: str,
                 durum: str = "musait"):
        if not ad or not ad.strip():
            raise ValueError("Kitap adı boş olamaz.")
        if not yazar or not yazar.strip():
            raise ValueError("Yazar boş olamaz.")
        if durum not in self.GECERLI_DURUMLAR:
            raise ValueError(f"Geçersiz durum: {durum}")

        self.kitap_id = kitap_id
        self.ad = ad.strip()
        self.yazar = yazar.strip()
        self.kategori = (kategori or "Genel").strip()
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
