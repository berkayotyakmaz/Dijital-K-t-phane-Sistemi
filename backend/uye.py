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

    def __init__(self, uye_id: int, ad: str, email: str):
        if not ad or not ad.strip():
            raise ValueError("Üye adı boş olamaz.")
        if not self._email_gecerli_mi(email):
            raise ValueError(f"Geçersiz e-posta formatı: {email}")

        self.uye_id = uye_id
        self.ad = ad.strip()
        self.email = email.strip().lower()

    @staticmethod
    def _email_gecerli_mi(email: str) -> bool:
        if not email or not isinstance(email, str):
            return False
        return bool(Uye.EMAIL_REGEX.match(email.strip()))

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
