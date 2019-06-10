# Sosyal Medyada Duygu Analizi

[![OMÜ CEng](https://img.shields.io/badge/OM%C3%9C-CEng-blue.svg)](http://bil.muhendislik.omu.edu.tr)

## İçerik

**Ondokuz Mayıs Üniversitesi** (OMÜ) **Bilgisayar Mühendisliği** lisans programı **Seminer** dersi ve **Proje** kapsamında 
Güz ve Bahar dönemleri boyunca yapılan projenin kaynak kodları ve raporu yer almaktadır.


## Repo'nun Dizin Yapısı

* **data** içerisinde **htmlwords.txt** , **slang.txt** , **text_emotion.csv** ve **clean_tweet.csv** belgeleri yer almaktadır.
  * **text_emotion.csv** belgesi içerisinde 40.000 adet tweet bulunmaktadır. Yapay Sinir Ağının eğitimi için kullanılacak veri setinin ham halidir.
  * **slang.txt** belgesi içerisinde tarafımdan hazırlanmış gündelik hayatta çok sık kullanılan kısaltmalar yer almaktadır.
  * **htmlwords.txt** belgesi içerisinde tarafımdan hazırlanmış html kelimeleri yer almaktadır.
  * **clean_tweet.csv** belgesi içerisinde elimizdeki veri setinin **data_helpers.py** ile temizlendikten sonraki hali yer almaktadır. Yapay Sinir Ağının eğitimi için kullanılacak veri setinin temizlenmiş halidir.

* **main** içerisinde proje kapsamında gerçekleştirilen kodlar yer almaktadır.

## Projenin Dizin Yapısı
* **.py** uzantılı dosyalar yer almtakdır. Proje **Python** programlama dili ve kütüphaneleri kullanılarak gerçekleştirilmiştir.
* **data_helpers.py** içerisinde Preprocessing aşamasında kullanılacak metodlar yer almaktadır. Elimizdeki veri seti veya Twitterdan gelen veriler bu kod sayesinde temizlenir.
* **lstm.py** içerisinde Yapay Sinir Ağı modelimizi oluşturduğumuz ve bu model ile ilgili metodların yer aldığı kaynak kod bulunmaktadır.
* **main.py** içerisinde **Python** kütüphanesi olan **dash ve plotly** ile gerçekleştirilmiş uygulama arayüzünün kodları yer almaktadır.
  * Bu kodlara ek olarak Twitter API kod bloğu da bu kaynak kodun içerisinde yer almaktadır.

## Katkıda Bulunanlar

* [@tunahanyetimoglu](https://github.com/tunahanyetimoglu) - Tunahan YETİMOĞLU
* [@erdemsahin](https://github.com/erdemsahin) - Erdem ŞAHİN
* [@usalman](https://github.com/usalman) - Umit SALMAN
