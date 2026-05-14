import os
import tkinter as tk
from tkinter import messagebox

import joblib
import pandas as pd
from PIL import Image, ImageDraw

from ayarlar import (
    CIZIM_ALANI_BOYUTU,
    MODEL_YOLU,
    PIKSEL_SUTUNLARI,
    matrisi_listeye_cevir,
    resmi_matrise_cevir,
)


model = None
canvas = None
sonuc_yazisi = None
cizim_resmi = None
cizim_nesnesi = None
son_x = None
son_y = None


def modeli_yukle():
    if not os.path.exists(MODEL_YOLU):
        raise FileNotFoundError("Önce veri_seti_olustur.py ve modeli_egit.py dosyalarını çalıştırın.")

    return joblib.load(MODEL_YOLU)


def bos_resim_olustur():
    global cizim_resmi, cizim_nesnesi

    cizim_resmi = Image.new("L", (CIZIM_ALANI_BOYUTU, CIZIM_ALANI_BOYUTU), 255)
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

    canvas.create_oval(
        event.x - 8,
        event.y - 8,
        event.x + 8,
        event.y + 8,
        fill="black",
        outline="black",
    )

    cizim_nesnesi.ellipse(
        (
            event.x - 8,
            event.y - 8,
            event.x + 8,
            event.y + 8,
        ),
        fill=0,
    )


def ciz(event):
    global son_x, son_y

    if son_x is None or son_y is None:
        son_x = event.x
        son_y = event.y
        return

    canvas.create_line(
        son_x,
        son_y,
        event.x,
        event.y,
        fill="black",
        width=18,
        capstyle=tk.ROUND,
        smooth=True,
    )

    cizim_nesnesi.line(
        (
            son_x,
            son_y,
            event.x,
            event.y,
        ),
        fill=0,
        width=18,
    )

    son_x = event.x
    son_y = event.y


def cizimi_bitir(event):
    global son_x, son_y

    son_x = None
    son_y = None


def tahmin_et():
    matris = resmi_matrise_cevir(cizim_resmi)

    if matris is None:
        sonuc_yazisi.set("Önce bir karakter çizin.")
        return

    pikseller = matrisi_listeye_cevir(matris)
    veri = pd.DataFrame([pikseller], columns=PIKSEL_SUTUNLARI)
    tahmin = model.predict(veri)[0]
    sonuc_yazisi.set(f"Tahmin edilen karakter: {tahmin}")


def arayuzu_baslat():
    global model, canvas, sonuc_yazisi

    model = modeli_yukle()

    pencere = tk.Tk()
    pencere.title("Karakter Tahmin Programı")
    pencere.resizable(False, False)

    canvas = tk.Canvas(
        pencere,
        width=CIZIM_ALANI_BOYUTU,
        height=CIZIM_ALANI_BOYUTU,
        bg="white",
        highlightthickness=0,
        bd=0,
    )
    canvas.pack(pady=(15, 0))

    canvas.bind("<Button-1>", cizime_basla)
    canvas.bind("<B1-Motion>", ciz)
    canvas.bind("<ButtonRelease-1>", cizimi_bitir)

    buton_cercevesi = tk.Frame(pencere)
    buton_cercevesi.pack(pady=12)

    tahmin_butonu = tk.Button(
        buton_cercevesi,
        text="Tahmin Et",
        width=14,
        command=tahmin_et,
    )
    tahmin_butonu.pack(side="left", padx=6)

    temizle_butonu = tk.Button(
        buton_cercevesi,
        text="Temizle",
        width=14,
        command=temizle,
    )
    temizle_butonu.pack(side="left", padx=6)

    sonuc_yazisi = tk.StringVar()
    sonuc_yazisi.set("Henüz tahmin yapılmadı.")

    sonuc_etiketi = tk.Label(
        pencere,
        textvariable=sonuc_yazisi,
        font=("Arial", 13),
    )
    sonuc_etiketi.pack(pady=(0, 15))

    bos_resim_olustur()
    pencere.mainloop()


def ana_program():
    try:
        arayuzu_baslat()
    except FileNotFoundError as hata:
        messagebox.showerror("Hata", str(hata))
    except Exception as hata:
        messagebox.showerror("Hata", str(hata))


if __name__ == "__main__":
    ana_program()
