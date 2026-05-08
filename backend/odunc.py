"""
Ödünç işlemi sınıfı.
"""
from datetime import datetime, timedelta


class Odunc:
    """
    Bir ödünç işlemi kaydını temsil eder.

    Attributes:
        odunc_id (int)
        kitap_id (int)
        uye_id (int)
        odunc_tarihi (datetime)
        iade_tarihi (datetime | None)
        son_teslim_tarihi (datetime)
    """

    ODUNC_SURESI_GUN = 14

    def __init__(self, odunc_id: int, kitap_id: int, uye_id: int,
                 odunc_tarihi: datetime = None,
                 iade_tarihi: datetime = None,
                 son_teslim_tarihi: datetime = None):
        self.odunc_id = odunc_id
        self.kitap_id = kitap_id
        self.uye_id = uye_id
        self.odunc_tarihi = odunc_tarihi or datetime.now()
        self.iade_tarihi = iade_tarihi
        self.son_teslim_tarihi = son_teslim_tarihi or (
            self.odunc_tarihi + timedelta(days=self.ODUNC_SURESI_GUN)
        )

    def iade_et(self) -> None:
        """Ödüncü iade et - iade_tarihi atar."""
        if self.iade_tarihi is not None:
            raise ValueError("Bu kitap zaten iade edilmiş.")
        self.iade_tarihi = datetime.now()

    def aktif_mi(self) -> bool:
        """Henüz iade edilmemiş mi?"""
        return self.iade_tarihi is None

    def gecikme_var_mi(self) -> bool:
        if not self.aktif_mi():
            return False
        return datetime.now() > self.son_teslim_tarihi

    def kalan_gun(self) -> int:
        """Pozitif: kalan gün, Negatif: gecikmiş gün."""
        if not self.aktif_mi():
            return 0
        delta = self.son_teslim_tarihi - datetime.now()
        return delta.days

    def to_dict(self) -> dict:
        return {
            "odunc_id": self.odunc_id,
            "kitap_id": self.kitap_id,
            "uye_id": self.uye_id,
            "odunc_tarihi": self.odunc_tarihi.isoformat(),
            "iade_tarihi": self.iade_tarihi.isoformat() if self.iade_tarihi else None,
            "son_teslim_tarihi": self.son_teslim_tarihi.isoformat(),
        }

    @classmethod
    def from_dict(cls, d: dict) -> "Odunc":
        return cls(
            odunc_id=d["odunc_id"],
            kitap_id=d["kitap_id"],
            uye_id=d["uye_id"],
            odunc_tarihi=datetime.fromisoformat(d["odunc_tarihi"]),
            iade_tarihi=(datetime.fromisoformat(d["iade_tarihi"])
                         if d.get("iade_tarihi") else None),
            son_teslim_tarihi=datetime.fromisoformat(d["son_teslim_tarihi"]),
        )

    def __repr__(self) -> str:
        durum = "aktif" if self.aktif_mi() else "iade edildi"
        return f"Odunc(id={self.odunc_id}, kitap={self.kitap_id}, uye={self.uye_id}, {durum})"
