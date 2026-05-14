Bu proje, kullanıcının çizdiği rakam veya harfi tahmin etmek için hazırlandı.

Programda `0-9` arasındaki rakamlar ile İngilizce alfabedeki büyük harfler kullanılır. Kullanıcı ekrandaki beyaz alana bir karakter çizer. Program bu çizimi küçük bir matrise dönüştürür ve daha önce eğitilmiş modele gönderir. Model de en yakın tahmini ekranda gösterir.

Projede bulunan dosyalar:

- `ayarlar.py`
  Ortak ayarlar burada bulunur. Matris boyutu, çizim alanı boyutu ve bazı yardımcı işlemler bu dosyada yer alır.
- `veri_seti_olustur.py`
  Eğitim için kullanılacak örnekleri üretir ve `veri_seti.csv` dosyasını oluşturur.
- `modeli_egit.py`
  Oluşturulan veri setini okuyup modeli eğitir ve sonucu `karakter_modeli.pkl` dosyasına kaydeder.
- `tahmin_et.py`
  Çizim ekranını açar ve kullanıcının çizdiği karakteri tahmin eder.

Programı çalıştırma sırası:

1. `python veri_seti_olustur.py`
2. `python modeli_egit.py`
3. `python tahmin_et.py`

Gerekli kütüphaneler:

- `pandas`
- `scikit-learn`
- `joblib`
- `Pillow`
