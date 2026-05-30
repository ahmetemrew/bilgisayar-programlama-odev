import os
import tkinter as tk
from tkinter import messagebox

import joblib
import pandas as pd
from PIL import Image, ImageDraw

from ayarlar import (
    YUKSEKLIK,
    GENISLIK,
    MODEL_YOLU,
    PIKSEL_SUTUNLARI,
    matrisi_listeye_cevir,
    resmi_matrise_cevir,
)
from kelime_araclari import (
    sozluk_yukle,
    resmi_parcalara_bol,
    en_yakin_kelimeyi_bul,
)


model = None
canvas = None
sonuc_yazisi = None
cizim_resmi = None
cizim_nesnesi = None
son_x = None
son_y = None
kelime_listesi = []


def modeli_yukle():
    if not os.path.exists(MODEL_YOLU):
        raise FileNotFoundError("Önce modeli eğitin.")
    return joblib.load(MODEL_YOLU)


def bos_resim_olustur():
    global cizim_resmi, cizim_nesnesi
    cizim_resmi = Image.new("L", (GENISLIK, YUKSEKLIK), 255)
    cizim_nesnesi = ImageDraw.Draw(cizim_resmi)


def temizle():
    global son_x, son_y
    canvas.delete("all")
    bos_resim_olustur()
    sonuc_yazisi.set("Henüz tahmin yapılmadı.")
    son_x = None
    son_y = None


def cizime_basla(event):
    global son_x, son_y
    son_x = event.x
    son_y = event.y
    canvas.create_oval(event.x - 8, event.y - 8, event.x + 8, event.y + 8, fill="black", outline="black")
    cizim_nesnesi.ellipse((event.x - 8, event.y - 8, event.x + 8, event.y + 8), fill=0)


def ciz(event):
    global son_x, son_y
    if son_x is None or son_y is None:
        son_x = event.x
        son_y = event.y
        return

    canvas.create_line(son_x, son_y, event.x, event.y, fill="black", width=18, capstyle=tk.ROUND, smooth=True)
    cizim_nesnesi.line((son_x, son_y, event.x, event.y), fill=0, width=18)
    son_x = event.x
    son_y = event.y


def cizimi_bitir(event):
    global son_x, son_y
    son_x = None
    son_y = None


def tahmin_et():
    harf_resimleri = resmi_parcalara_bol(cizim_resmi)

    if not harf_resimleri:
        sonuc_yazisi.set("Önce bir kelime çizin.")
        return

    tahmin_dizisi = ""
    for parca in harf_resimleri:
        matris = resmi_matrise_cevir(parca)
        if matris:
            pikseller = matrisi_listeye_cevir(matris)
            veri = pd.DataFrame([pikseller], columns=PIKSEL_SUTUNLARI)
            harf = model.predict(veri)[0]
            tahmin_dizisi += str(harf)

    if tahmin_dizisi:
        sonuc = en_yakin_kelimeyi_bul(tahmin_dizisi, kelime_listesi)
        sonuc_yazisi.set(f"Tahmin: {sonuc} (Ham: {tahmin_dizisi})")


def arayuzu_baslat():
    global model, canvas, sonuc_yazisi, kelime_listesi

    model = modeli_yukle()
    kelime_listesi = sozluk_yukle()

    pencere = tk.Tk()
    pencere.title("Kelime Tahmin Programı")
    pencere.resizable(False, False)

    canvas = tk.Canvas(pencere, width=GENISLIK, height=YUKSEKLIK, bg="white", highlightthickness=0, bd=0)
    canvas.pack(pady=(15, 0))

    canvas.bind("<Button-1>", cizime_basla)
    canvas.bind("<B1-Motion>", ciz)
    canvas.bind("<ButtonRelease-1>", cizimi_bitir)

    buton_cercevesi = tk.Frame(pencere)
    buton_cercevesi.pack(pady=12)

    tk.Button(buton_cercevesi, text="Tahmin Et", width=14, command=tahmin_et).pack(side="left", padx=6)
    tk.Button(buton_cercevesi, text="Temizle", width=14, command=temizle).pack(side="left", padx=6)

    sonuc_yazisi = tk.StringVar()
    sonuc_yazisi.set("Henüz tahmin yapılmadı.")
    tk.Label(pencere, textvariable=sonuc_yazisi, font=("Arial", 13)).pack(pady=(0, 15))

    bos_resim_olustur()
    pencere.mainloop()


if __name__ == "__main__":
    try:
        arayuzu_baslat()
    except Exception as hata:
        print(f"Hata: {hata}")
