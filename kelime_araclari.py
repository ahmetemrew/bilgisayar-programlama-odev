import os
import urllib.request
import difflib
from PIL import ImageOps

from ayarlar import SOZLUK_YOLU


def sozluk_hazirla():
    if os.path.exists(SOZLUK_YOLU):
        return

    turkce_url = "https://raw.githubusercontent.com/CanNuhlar/Turkce-Kelime-Listesi/master/turkce_kelime_listesi.txt"
    ingilizce_url = "https://raw.githubusercontent.com/first20hours/google-10000-english/master/google-10000-english-no-swears.txt"

    kelimeler = set()

    for url in [turkce_url, ingilizce_url]:
        try:
            yanit = urllib.request.urlopen(url)
            icerik = yanit.read().decode("utf-8")
            for kelime in icerik.splitlines():
                temiz_kelime = kelime.strip().upper()
                if len(temiz_kelime) > 1:
                    kelimeler.add(temiz_kelime)
        except:
            continue

    with open(SOZLUK_YOLU, "w", encoding="utf-8") as dosya:
        for kelime in sorted(list(kelimeler)):
            dosya.write(kelime + "\n")


def sozluk_yukle():
    sozluk_hazirla()
    with open(SOZLUK_YOLU, "r", encoding="utf-8") as dosya:
        return [satir.strip() for satir in dosya]


def resmi_parcalara_bol(resim):
    gri_resim = resim.convert("L")
    ters_resim = ImageOps.invert(gri_resim)
    
    genislik, yukseklik = ters_resim.size
    pikseller = ters_resim.load()
    
    harf_sinirlari = []
    harf_basladi = False
    baslangic_x = 0
    
    for x in range(genislik):
        sutun_dolu = False
        for y in range(yukseklik):
            if pikseller[x, y] > 0:
                sutun_dolu = True
                break
        
        if sutun_dolu and not harf_basladi:
            harf_basladi = True
            baslangic_x = x
        elif not sutun_dolu and harf_basladi:
            harf_basladi = False
            if x - baslangic_x > 5:
                harf_sinirlari.append((baslangic_x, x))
    
    parcalar = []
    for sol, sag in harf_sinirlari:
        parca = resim.crop((sol - 5, 0, sag + 5, yukseklik))
        parcalar.append(parca)
        
    return parcalar


def en_yakin_kelimeyi_bul(tahmin_dizisi, kelime_listesi):
    eslesmeler = difflib.get_close_matches(tahmin_dizisi, kelime_listesi, n=1, cutoff=0.3)
    if eslesmeler:
        return eslesmeler[0]
    return tahmin_dizisi
