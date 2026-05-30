Bu proje, ekrana çizilen harfleri ve kelimeleri tahmin etmek için hazırlandı.

Programda harfler yan yana yazılarak kelime oluşturulabilir. Program çizilen şeyi harf harf parçalara böler, her harfi ayrı tahmin eder ve sonra bu harfleri birleştirip sözlükten en yakın kelimeyi bulur.

Projede bulunan dosyalar:

- `ayarlar.py`
  Ekran boyutu ve matris ayarları gibi ortak ayarlar burada bulunur.
- `kelime_araclari.py`
  Kelimeleri harflere bölme ve sözlükten kelime bulma işlemlerini yapar.
- `veri_seti_olustur.py`
  Eğitim için harf örnekleri üretir ve `veri_seti.csv` dosyasını oluşturur.
- `modeli_egit.py`
  Veri setini okuyup modeli eğitir ve sonucu `karakter_modeli.pkl` dosyasına kaydeder.
- `tahmin_et.py`
  Çizim ekranını açar ve yazılan kelimeyi tahmin eder.

Programı çalıştırma sırası:

1. `python veri_seti_olustur.py`
2. `python modeli_egit.py`
3. `python tahmin_et.py`

Gerekli kütüphaneler:

- `pandas`
- `scikit-learn`
- `joblib`
- `Pillow`
