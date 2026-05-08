"""
Auth modülü - Kullanıcı kimlik doğrulama.

Şifreler PBKDF2-HMAC-SHA256 ile hash'lenir; düz metin saklanmaz.
"""
import hashlib
import hmac
import json
import os
import secrets
from datetime import datetime
from typing import Optional


class Kullanici:
    """Sistem kullanıcısı."""

    def __init__(
        self,
        kullanici_adi: str,
        sifre_hash: str,
        salt: str,
        ad: str = "",
        rol: str = "yonetici",
        olusturma: str = None,
    ):
        self.kullanici_adi = kullanici_adi.strip().lower()
        self.sifre_hash = sifre_hash
        self.salt = salt
        self.ad = ad or kullanici_adi
        self.rol = rol
        self.olusturma = olusturma or datetime.now().isoformat()

    def to_dict(self) -> dict:
        return {
            "kullanici_adi": self.kullanici_adi,
            "sifre_hash": self.sifre_hash,
            "salt": self.salt,
            "ad": self.ad,
            "rol": self.rol,
            "olusturma": self.olusturma,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "Kullanici":
        return cls(**d)


class AuthYoneticisi:
    """Kullanıcı CRUD + login işlemleri."""

    PBKDF2_ITER = 200_000

    def __init__(self, dosya_yolu: str):
        self.dosya_yolu = dosya_yolu
        self._kullanicilar: dict[str, Kullanici] = {}
        self._yukle()

    # ---------- Kalıcılık ----------

    def _yukle(self) -> None:
        if not os.path.exists(self.dosya_yolu):
            return
        try:
            with open(self.dosya_yolu, "r", encoding="utf-8") as f:
                veri = json.load(f)
                for d in veri:
                    k = Kullanici.from_dict(d)
                    self._kullanicilar[k.kullanici_adi] = k
        except (json.JSONDecodeError, KeyError, TypeError):
            pass

    def kaydet(self) -> None:
        os.makedirs(os.path.dirname(self.dosya_yolu) or ".", exist_ok=True)
        veri = [k.to_dict() for k in self._kullanicilar.values()]
        with open(self.dosya_yolu, "w", encoding="utf-8") as f:
            json.dump(veri, f, ensure_ascii=False, indent=2)

    # ---------- Şifre işlemleri ----------

    @staticmethod
    def _hash_sifre(sifre: str, salt: str) -> str:
        """PBKDF2-HMAC-SHA256 ile şifre hash'le."""
        dk = hashlib.pbkdf2_hmac(
            "sha256",
            sifre.encode("utf-8"),
            salt.encode("utf-8"),
            AuthYoneticisi.PBKDF2_ITER,
        )
        return dk.hex()

    @staticmethod
    def _yeni_salt() -> str:
        return secrets.token_hex(16)

    # ---------- API ----------

    def kullanici_var_mi(self) -> bool:
        """Sistemde en az bir kullanıcı var mı?"""
        return len(self._kullanicilar) > 0

    def kullanici_ekle(
        self, kullanici_adi: str, sifre: str, ad: str = "", rol: str = "yonetici"
    ) -> Kullanici:
        kullanici_adi = kullanici_adi.strip().lower()

        if not kullanici_adi:
            raise ValueError("Kullanıcı adı boş olamaz.")
        if len(kullanici_adi) < 3:
            raise ValueError("Kullanıcı adı en az 3 karakter olmalı.")
        if " " in kullanici_adi:
            raise ValueError("Kullanıcı adı boşluk içeremez.")
        if not sifre or len(sifre) < 4:
            raise ValueError("Şifre en az 4 karakter olmalı.")
        if kullanici_adi in self._kullanicilar:
            raise ValueError(f"Bu kullanıcı adı zaten kayıtlı: {kullanici_adi}")

        salt = self._yeni_salt()
        sifre_hash = self._hash_sifre(sifre, salt)
        k = Kullanici(
            kullanici_adi=kullanici_adi,
            sifre_hash=sifre_hash,
            salt=salt,
            ad=ad.strip() or kullanici_adi,
            rol=rol,
        )
        self._kullanicilar[kullanici_adi] = k
        self.kaydet()
        return k

    def dogrula(self, kullanici_adi: str, sifre: str) -> Optional[Kullanici]:
        """Doğru ise Kullanici nesnesi, yanlış ise None döner."""
        kullanici_adi = kullanici_adi.strip().lower()
        k = self._kullanicilar.get(kullanici_adi)
        if not k:
            return None
        beklenen = self._hash_sifre(sifre, k.salt)
        # Sabit zamanlı karşılaştırma (timing attack koruması)
        if hmac.compare_digest(beklenen, k.sifre_hash):
            return k
        return None

    def sifre_degistir(self, kullanici_adi: str, eski_sifre: str, yeni_sifre: str) -> bool:
        k = self.dogrula(kullanici_adi, eski_sifre)
        if not k:
            return False
        if not yeni_sifre or len(yeni_sifre) < 4:
            raise ValueError("Yeni şifre en az 4 karakter olmalı.")
        k.salt = self._yeni_salt()
        k.sifre_hash = self._hash_sifre(yeni_sifre, k.salt)
        self.kaydet()
        return True

    def varsayilan_kullanici_olustur(self) -> Kullanici:
        """İlk açılışta varsayılan admin oluşturur."""
        return self.kullanici_ekle(
            kullanici_adi="admin",
            sifre="admin123",
            ad="Admin",
            rol="yonetici",
        )
