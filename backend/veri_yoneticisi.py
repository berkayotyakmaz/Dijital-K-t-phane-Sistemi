"""
Kütüphane Veri Yöneticisi - Tüm modellerin merkezi yönetimi ve JSON kalıcılık.
"""
import json
import os
from datetime import datetime
from typing import Dict, List, Optional

from .kitap import Kitap
from .uye import Uye
from .odunc import Odunc


class VeriYoneticisi:
    """Kütüphane verilerini JSON dosyalarında yönetir."""

    def __init__(self, veri_klasoru: str = "data"):
        self.veri_klasoru = veri_klasoru
        os.makedirs(veri_klasoru, exist_ok=True)

        self.kitaplar_dosya = os.path.join(veri_klasoru, "kitaplar.json")
        self.uyeler_dosya = os.path.join(veri_klasoru, "uyeler.json")
        self.oduncler_dosya = os.path.join(veri_klasoru, "oduncler.json")

        self._kitaplar: Dict[int, Kitap] = {}
        self._uyeler: Dict[int, Uye] = {}
        self._oduncler: Dict[int, Odunc] = {}

        self._sonraki_kitap_id = 1
        self._sonraki_uye_id = 1
        self._sonraki_odunc_id = 1

        self._yukle()

    # ---------------- KALICILIK ----------------

    def _yukle(self) -> None:
        if os.path.exists(self.kitaplar_dosya):
            try:
                with open(self.kitaplar_dosya, "r", encoding="utf-8") as f:
                    for d in json.load(f):
                        k = Kitap.from_dict(d)
                        self._kitaplar[k.kitap_id] = k
                        self._sonraki_kitap_id = max(self._sonraki_kitap_id, k.kitap_id + 1)
            except (json.JSONDecodeError, KeyError):
                pass

        if os.path.exists(self.uyeler_dosya):
            try:
                with open(self.uyeler_dosya, "r", encoding="utf-8") as f:
                    for d in json.load(f):
                        u = Uye.from_dict(d)
                        self._uyeler[u.uye_id] = u
                        self._sonraki_uye_id = max(self._sonraki_uye_id, u.uye_id + 1)
            except (json.JSONDecodeError, KeyError):
                pass

        if os.path.exists(self.oduncler_dosya):
            try:
                with open(self.oduncler_dosya, "r", encoding="utf-8") as f:
                    for d in json.load(f):
                        o = Odunc.from_dict(d)
                        self._oduncler[o.odunc_id] = o
                        self._sonraki_odunc_id = max(self._sonraki_odunc_id, o.odunc_id + 1)
            except (json.JSONDecodeError, KeyError):
                pass

    def kaydet(self) -> None:
        with open(self.kitaplar_dosya, "w", encoding="utf-8") as f:
            json.dump([k.to_dict() for k in self._kitaplar.values()], f,
                      ensure_ascii=False, indent=2)
        with open(self.uyeler_dosya, "w", encoding="utf-8") as f:
            json.dump([u.to_dict() for u in self._uyeler.values()], f,
                      ensure_ascii=False, indent=2)
        with open(self.oduncler_dosya, "w", encoding="utf-8") as f:
            json.dump([o.to_dict() for o in self._oduncler.values()], f,
                      ensure_ascii=False, indent=2)

    # ---------------- KİTAP CRUD ----------------

    def kitap_ekle(self, ad: str, yazar: str, kategori: str = "Genel") -> Kitap:
        kitap = Kitap(
            kitap_id=self._sonraki_kitap_id,
            ad=ad, yazar=yazar, kategori=kategori,
        )
        self._kitaplar[kitap.kitap_id] = kitap
        self._sonraki_kitap_id += 1
        self.kaydet()
        return kitap

    def kitap_guncelle(self, kitap_id: int, ad: str, yazar: str,
                       kategori: str) -> Kitap:
        kitap = self._kitaplar.get(kitap_id)
        if not kitap:
            raise ValueError(f"Kitap bulunamadı (ID: {kitap_id}).")
        if not ad.strip():
            raise ValueError("Kitap adı boş olamaz.")
        if not yazar.strip():
            raise ValueError("Yazar boş olamaz.")
        kitap.ad = ad.strip()
        kitap.yazar = yazar.strip()
        kitap.kategori = (kategori or "Genel").strip()
        self.kaydet()
        return kitap

    def kitap_sil(self, kitap_id: int) -> bool:
        kitap = self._kitaplar.get(kitap_id)
        if not kitap:
            return False
        if kitap.durum == "odunc":
            raise ValueError("Ödünçteki kitap silinemez. Önce iade edilmeli.")
        del self._kitaplar[kitap_id]
        self.kaydet()
        return True

    def kitap_getir(self, kitap_id: int) -> Optional[Kitap]:
        return self._kitaplar.get(kitap_id)

    def tum_kitaplar(self) -> List[Kitap]:
        return sorted(self._kitaplar.values(), key=lambda k: k.ad.lower())

    def musait_kitaplar(self) -> List[Kitap]:
        return [k for k in self._kitaplar.values() if k.musait_mi()]

    # ---------------- ÜYE CRUD ----------------

    def uye_ekle(self, ad: str, email: str) -> Uye:
        email_lower = email.strip().lower()
        for u in self._uyeler.values():
            if u.email == email_lower:
                raise ValueError(f"Bu e-posta zaten kayıtlı: {email_lower}")

        uye = Uye(uye_id=self._sonraki_uye_id, ad=ad, email=email)
        self._uyeler[uye.uye_id] = uye
        self._sonraki_uye_id += 1
        self.kaydet()
        return uye

    def uye_guncelle(self, uye_id: int, ad: str, email: str) -> Uye:
        uye = self._uyeler.get(uye_id)
        if not uye:
            raise ValueError(f"Üye bulunamadı (ID: {uye_id}).")

        email_lower = email.strip().lower()
        for u in self._uyeler.values():
            if u.uye_id != uye_id and u.email == email_lower:
                raise ValueError(f"Bu e-posta başka üyeye ait: {email_lower}")
        if not Uye._email_gecerli_mi(email):
            raise ValueError(f"Geçersiz e-posta: {email}")

        uye.ad = ad.strip()
        uye.email = email_lower
        self.kaydet()
        return uye

    def uye_sil(self, uye_id: int) -> bool:
        uye = self._uyeler.get(uye_id)
        if not uye:
            return False
        # Aktif ödüncü var mı?
        for o in self._oduncler.values():
            if o.uye_id == uye_id and o.aktif_mi():
                raise ValueError("Üye üzerinde aktif ödünç var. Önce iade edilmeli.")
        del self._uyeler[uye_id]
        self.kaydet()
        return True

    def uye_getir(self, uye_id: int) -> Optional[Uye]:
        return self._uyeler.get(uye_id)

    def tum_uyeler(self) -> List[Uye]:
        return sorted(self._uyeler.values(), key=lambda u: u.ad.lower())

    # ---------------- ÖDÜNÇ İŞLEMLERİ ----------------

    def odunc_ver(self, kitap_id: int, uye_id: int) -> Odunc:
        kitap = self._kitaplar.get(kitap_id)
        uye = self._uyeler.get(uye_id)

        if not kitap:
            raise ValueError("Kitap bulunamadı.")
        if not uye:
            raise ValueError("Üye bulunamadı.")
        if kitap.durum == "odunc":
            raise ValueError(f"'{kitap.ad}' zaten ödünçte.")

        if not uye.kitap_odunc_al(kitap):
            raise ValueError("Ödünç verme başarısız.")

        odunc = Odunc(
            odunc_id=self._sonraki_odunc_id,
            kitap_id=kitap_id,
            uye_id=uye_id,
        )
        self._oduncler[odunc.odunc_id] = odunc
        self._sonraki_odunc_id += 1
        self.kaydet()
        return odunc

    def iade_et(self, odunc_id: int) -> Odunc:
        odunc = self._oduncler.get(odunc_id)
        if not odunc:
            raise ValueError("Ödünç kaydı bulunamadı.")
        if not odunc.aktif_mi():
            raise ValueError("Bu kitap zaten iade edilmiş.")

        kitap = self._kitaplar.get(odunc.kitap_id)
        uye = self._uyeler.get(odunc.uye_id)
        if kitap and uye:
            uye.kitap_iade_et(kitap)

        odunc.iade_et()
        self.kaydet()
        return odunc

    def odunc_getir(self, odunc_id: int) -> Optional[Odunc]:
        return self._oduncler.get(odunc_id)

    def tum_oduncler(self) -> List[Odunc]:
        return sorted(self._oduncler.values(),
                      key=lambda o: o.odunc_tarihi, reverse=True)

    def aktif_oduncler(self) -> List[Odunc]:
        return [o for o in self._oduncler.values() if o.aktif_mi()]

    def gecikmis_oduncler(self) -> List[Odunc]:
        return [o for o in self._oduncler.values() if o.gecikme_var_mi()]

    def uye_odunc_gecmisi(self, uye_id: int) -> List[Odunc]:
        return sorted(
            [o for o in self._oduncler.values() if o.uye_id == uye_id],
            key=lambda o: o.odunc_tarihi, reverse=True,
        )

    # ---------------- İSTATİSTİK ----------------

    def genel_istatistikler(self) -> dict:
        toplam_kitap = len(self._kitaplar)
        odunc_kitap = sum(1 for k in self._kitaplar.values() if not k.musait_mi())
        musait_kitap = toplam_kitap - odunc_kitap

        oran = (odunc_kitap / toplam_kitap * 100) if toplam_kitap else 0

        return {
            "toplam_kitap": toplam_kitap,
            "musait_kitap": musait_kitap,
            "odunc_kitap": odunc_kitap,
            "toplam_uye": len(self._uyeler),
            "aktif_odunc": len(self.aktif_oduncler()),
            "gecikmis_odunc": len(self.gecikmis_oduncler()),
            "toplam_islem": len(self._oduncler),
            "kullanim_orani": round(oran, 1),
        }

    def kategori_dagilim(self) -> dict:
        """Kitapların kategorilere göre dağılımı."""
        dagilim = {}
        for k in self._kitaplar.values():
            dagilim[k.kategori] = dagilim.get(k.kategori, 0) + 1
        return dagilim
