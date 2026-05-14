import csv
import random

from PIL import Image, ImageDraw, ImageFilter, ImageFont

from ayarlar import (
    CIZIM_ALANI_BOYUTU,
    KARAKTERLER,
    PIKSEL_SUTUNLARI,
    VERI_SETI_YOLU,
    matrisi_listeye_cevir,
    resmi_matrise_cevir,
    yazi_tipi_yollarini_al,
)


def karakter_resmi_olustur(
    karakter,
    yazi_tipi_yolu,
    yazi_boyutu,
    x_kayma,
    y_kayma,
    donus_acisi,
    egiklik,
    kalinlastir,
    dis_cizgi_kalinligi,
):
    resim = Image.new("L", (CIZIM_ALANI_BOYUTU, CIZIM_ALANI_BOYUTU), 255)
    cizim = ImageDraw.Draw(resim)
    yazi_tipi = ImageFont.truetype(yazi_tipi_yolu, yazi_boyutu)

    sol, ust, sag, alt = cizim.textbbox((0, 0), karakter, font=yazi_tipi)
    metin_genisligi = sag - sol
    metin_yuksekligi = alt - ust

    x = (CIZIM_ALANI_BOYUTU - metin_genisligi) // 2 - sol + x_kayma
    y = (CIZIM_ALANI_BOYUTU - metin_yuksekligi) // 2 - ust + y_kayma

    if dis_cizgi_kalinligi == 0:
        cizim.text((x, y), karakter, fill=0, font=yazi_tipi)
    else:
        cizim.text(
            (x, y),
            karakter,
            fill=255,
            font=yazi_tipi,
            stroke_width=dis_cizgi_kalinligi,
            stroke_fill=0,
        )

    resim = resim.rotate(donus_acisi, fillcolor=255)

    if egiklik != 0:
        kayma = int(abs(egiklik) * CIZIM_ALANI_BOYUTU)

        if egiklik > 0:
            veri = (1, egiklik, -kayma, 0, 1, 0)
        else:
            veri = (1, egiklik, 0, 0, 1, 0)

        resim = resim.transform(
            (CIZIM_ALANI_BOYUTU, CIZIM_ALANI_BOYUTU),
            Image.Transform.AFFINE,
            veri,
            fillcolor=255,
        )

    if kalinlastir:
        resim = resim.filter(ImageFilter.MaxFilter(3))

    return resim


def varyantlari_olustur(karakter, yazi_tipi_yollari):
    varyantlar = []
    gorulenler = set()
    uretici = random.Random(karakter)
    hedef_varyant_sayisi = 420
    maksimum_deneme_sayisi = 1600
    egiklikler = [-0.18, -0.12, -0.06, 0, 0.06, 0.12, 0.18]
    dis_cizgi_kalinliklari = [0, 0, 10, 14]

    for _ in range(maksimum_deneme_sayisi):
        if len(varyantlar) >= hedef_varyant_sayisi:
            break

        resim = karakter_resmi_olustur(
            karakter,
            uretici.choice(yazi_tipi_yollari),
            uretici.randint(145, 185),
            uretici.randint(-18, 18),
            uretici.randint(-18, 18),
            uretici.randint(-14, 14),
            uretici.choice(egiklikler),
            uretici.choice([False, True]),
            uretici.choice(dis_cizgi_kalinliklari),
        )

        matris = resmi_matrise_cevir(resim)

        if matris is None:
            continue

        anahtar = "".join(str(sayi) for sayi in matrisi_listeye_cevir(matris))

        if anahtar not in gorulenler:
            varyantlar.append(matris)
            gorulenler.add(anahtar)

    return varyantlar


def veri_seti_olustur():
    yazi_tipi_yollari = yazi_tipi_yollarini_al()

    if not yazi_tipi_yollari:
        raise FileNotFoundError("Uygun yazı tipi bulunamadı.")

    satirlar = []

    for karakter in KARAKTERLER:
        varyantlar = varyantlari_olustur(karakter, yazi_tipi_yollari)

        for matris in varyantlar:
            satir = matrisi_listeye_cevir(matris)
            satirlar.append(satir + [karakter])

    with open(VERI_SETI_YOLU, "w", newline="", encoding="utf-8") as dosya:
        yazici = csv.writer(dosya)
        yazici.writerow(PIKSEL_SUTUNLARI + ["label"])
        yazici.writerows(satirlar)

    print("Veri seti oluşturuldu.")
    print(f"Toplam örnek sayısı: {len(satirlar)}")


def ana_program():
    try:
        veri_seti_olustur()
    except Exception as hata:
        print(f"Hata: {hata}")


if __name__ == "__main__":
    ana_program()
