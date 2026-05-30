import os

import joblib
import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier

from ayarlar import MODEL_YOLU, VERI_SETI_YOLU


def veri_setini_yukle():
    if not os.path.exists(VERI_SETI_YOLU):
        raise FileNotFoundError(
            "Önce veri_seti_olustur.py dosyasını çalıştırmanız gerekiyor."
        )

    return pd.read_csv(VERI_SETI_YOLU, dtype={"label": str})


def modeli_egit(veriler):
    X = veriler.drop("label", axis=1)
    y = veriler["label"]

    X_egitim, X_test, y_egitim, y_test = train_test_split(
        X,
        y,
        test_size=0.25,
        random_state=42,
        stratify=y,
    )

    model = MLPClassifier(
        hidden_layer_sizes=(180,),
        max_iter=600,
        random_state=42,
    )

    model.fit(X_egitim, y_egitim)

    tahminler = model.predict(X_test)
    basari = accuracy_score(y_test, tahminler)

    joblib.dump(model, MODEL_YOLU)

    print("Model eğitildi.")
    print(f"Toplam veri sayısı: {len(veriler)}")
    print(f"Eğitim verisi sayısı: {len(X_egitim)}")
    print(f"Test verisi sayısı: {len(X_test)}")
    print(f"Başarı oranı: {basari * 100:.2f}%")
    print("Model kaydedildi.")


def ana_program():
    try:
        veriler = veri_setini_yukle()
        modeli_egit(veriler)
    except Exception as hata:
        print(f"Hata: {hata}")


if __name__ == "__main__":
    ana_program()
