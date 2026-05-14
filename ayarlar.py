import os

from PIL import Image, ImageOps


PROJE_KLASORU = os.path.dirname(os.path.abspath(__file__))
VERI_SETI_YOLU = os.path.join(PROJE_KLASORU, "veri_seti.csv")
MODEL_YOLU = os.path.join(PROJE_KLASORU, "karakter_modeli.pkl")

MATRIS_BOYUTU = 18
CIZIM_ALANI_BOYUTU = 280
KARAKTERLER = list("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ")
PIKSEL_SUTUNLARI = [f"p{i}" for i in range(1, MATRIS_BOYUTU * MATRIS_BOYUTU + 1)]


def yazi_tipi_yollarini_al():
    font_klasoru = os.path.join(os.environ.get("WINDIR", "C:\\Windows"), "Fonts")
    dosya_adlari = [
        "arial.ttf",
        "arialbd.ttf",
        "calibri.ttf",
        "calibrib.ttf",
        "consola.ttf",
        "consolab.ttf",
        "comic.ttf",
        "comicbd.ttf",
        "corbel.ttf",
        "corbelb.ttf",
        "georgia.ttf",
        "georgiab.ttf",
        "inkfree.ttf",
        "segoepr.ttf",
        "segoeprb.ttf",
        "verdana.ttf",
        "verdanab.ttf",
    ]

    yazi_tipi_yollari = []

    for dosya_adi in dosya_adlari:
        yol = os.path.join(font_klasoru, dosya_adi)

        if os.path.exists(yol):
            yazi_tipi_yollari.append(yol)

    return yazi_tipi_yollari


def matrisi_listeye_cevir(matris):
    sayilar = []

    for satir in matris:
        for piksel in satir:
            sayilar.append(piksel)

    return sayilar


def resmi_matrise_cevir(resim):
    gri_resim = resim.convert("L")
    ters_resim = ImageOps.invert(gri_resim)
    sinirlar = ters_resim.getbbox()

    if sinirlar is None:
        return None

    kirpilmis_resim = gri_resim.crop(sinirlar)
    genislik, yukseklik = kirpilmis_resim.size
    kare_boyut = max(genislik, yukseklik) + 40
    kare_resim = Image.new("L", (kare_boyut, kare_boyut), 255)

    sol = (kare_boyut - genislik) // 2
    ust = (kare_boyut - yukseklik) // 2
    kare_resim.paste(kirpilmis_resim, (sol, ust))

    kucuk_resim = kare_resim.resize(
        (MATRIS_BOYUTU, MATRIS_BOYUTU),
        Image.Resampling.LANCZOS,
    )

    matris = []

    for y in range(MATRIS_BOYUTU):
        satir = []

        for x in range(MATRIS_BOYUTU):
            piksel = kucuk_resim.getpixel((x, y))
            satir.append(1 if piksel < 215 else 0)

        matris.append(satir)

    return matris
