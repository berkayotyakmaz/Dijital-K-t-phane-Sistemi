"""
Üye sınıfı.
"""
import re


class Uye:
    """
    Kütüphane üyesini temsil eder.

    Attributes:
        uye_id (int)
        ad (str)
        email (str)
    """

    EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")

    # Karakter sınırları
    MAX_AD = 80
    MAX_EMAIL = 120  # RFC 5321 local-part 64 + domain 255 ama pratikte 120 yeter

    def __init__(self, uye_id: int, ad: str, email: str):
        ad = (ad or "").strip()
        email = (email or "").strip()

        if not ad:
            raise ValueError("Üye adı boş olamaz.")
        if len(ad) > self.MAX_AD:
            raise ValueError(f"Üye adı en fazla {self.MAX_AD} karakter olabilir.")
        if len(email) > self.MAX_EMAIL:
            raise ValueError(f"E-posta en fazla {self.MAX_EMAIL} karakter olabilir.")
        if not self._email_gecerli_mi(email):
            raise ValueError(f"Geçersiz e-posta formatı: {email}")

        self.uye_id = uye_id
        self.ad = ad
        self.email = email.lower()

    @staticmethod
    def email_gecerli_mi(email: str) -> bool:
        """Public validator - dışarıdan da çağrılabilir."""
        if not email or not isinstance(email, str):
            return False
        return bool(Uye.EMAIL_REGEX.match(email.strip()))

    # Geriye uyumluluk
    _email_gecerli_mi = email_gecerli_mi

    def kitap_odunc_al(self, kitap) -> bool:
        """Kitap müsaitse üzerine alır."""
        if kitap.durum != "musait":
            return False
        kitap.kitap_durumu_degistir("odunc")
        return True

    def kitap_iade_et(self, kitap) -> bool:
        """Üye üzerindeki kitabı iade eder."""
        if kitap.durum != "odunc":
            return False
        kitap.kitap_durumu_degistir("musait")
        return True

    def to_dict(self) -> dict:
        return {
            "uye_id": self.uye_id,
            "ad": self.ad,
            "email": self.email,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "Uye":
        return cls(
            uye_id=d["uye_id"],
            ad=d["ad"],
            email=d["email"],
        )

    def __repr__(self) -> str:
        return f"Uye(id={self.uye_id}, ad='{self.ad}')"
