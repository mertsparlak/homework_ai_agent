# Ödev Analiz Aracı

Bu araç, verilen bir klasördeki PDF formatındaki öğrenci ödevlerini otomatik olarak analiz etmek ve değerlendirmek için geliştirilmiştir. Google Gemini API'sini kullanarak ödevlerin doğruluğunu ve uygunluğunu değerlendirir, puan verir ve kısa bir açıklama oluşturur. Sonuçlar, Excel dosyasına kaydedilir.

## Nasıl Çalışır?

Araç, aşağıdaki adımları izleyerek çalışır:

1.  **PDF'leri Okuma:** Belirtilen klasördeki tüm PDF dosyalarını okur ve metin içeriğini çıkarır.
2.  **Öğrenci Bilgilerini Çıkarma:** PDF içeriğinden öğrenci adını, soyadını ve ID'sini çıkarır. Bu işlem için "İSİM:", "SOYAD:" ve "İD:" ifadelerini arayan bir regex kullanılır. Bu ifadelerin PDF'lerde tutarlı bir şekilde bulunması gerekmektedir.
3.  **Gemini ile Değerlendirme:** Çıkarılan metni ve ödev açıklamasını Google Gemini API'sine göndererek ödevin doğruluğunu değerlendirmesini ister. Gemini'den bir puan (100 üzerinden) ve kısa bir açıklama beklenir.
4.  **Sonuçları Kaydetme:** Öğrenci bilgileri, verilen puan ve oluşturulan açıklama bir Excel dosyasına kaydedilir.

## Kurulum

Aracı kullanmak için aşağıdaki adımları izleyin:

1.  **Python Kurulumu:** Bilgisayarınızda Python'ın kurulu olduğundan emin olun (Python 3.7 veya üzeri önerilir).
2.  **Gerekli Kütüphaneleri Kurun:** Terminal veya komut istemcisini açın ve aşağıdaki komutları çalıştırın:

    ```bash
    pip install google-generativeai pymupdf pandas tkinter
    ```

3.  **API Anahtarı:** Bir Google Cloud projesi oluşturun ve Gemini API'sini etkinleştirin. Ardından, bir API anahtarı oluşturun.
4.  **`api_key.py` Dosyası Oluşturun:** Proje dizininizde `api_key.py` adında bir dosya oluşturun ve aşağıdaki satırı ekleyin (GERÇEK_API_ANAHTARINIZ yerine kendi API anahtarınızı girin):

    ```python
    your_api = "GERÇEK_API_ANAHTARINIZ"
    ```

5.  **Kodu İndirin:** Bu kodları içeren Python dosyasını (`main.py` gibi) indirin veya kopyalayın.

## Kullanım

1.  `main.py` dosyasını çalıştırın:

    ```bash
    python main.py
    ```

2.  Açılan arayüzde aşağıdaki bilgileri girin:
    *   **PDF Klasör Yolu:** Ödev PDF'lerinin bulunduğu klasörün yolunu seçin.
    *   **Ders Adı:** Dersin adını girin (örneğin, "Tarih").
    *   **Ödev Açıklaması:** Öğrencilerden ödevde ne istendiğini kısaca açıklayın (örneğin, "1. ve 2. Dünya Savaşları hakkında bilgi").
    *   **Kaydetme Konumu:** Excel dosyasının kaydedileceği konumu seçin.
3.  "Ödevleri Analiz Et" butonuna tıklayın.

## Dosya Formatı

Öğrenci bilgilerinin doğru şekilde çıkarılabilmesi için PDF dosyalarının aşağıdaki formatta olması gerekmektedir:

Elbette, projeniz için bir README dosyası hazırlayabilirim. Sohbet boyunca edindiğimiz bilgilere dayanarak, olabildiğince anlaşılır ve insancıl bir dil kullanacağım. İşte örnek bir README dosyası:

Markdown

# Ödev Analiz Aracı

Bu araç, verilen bir klasördeki PDF formatındaki öğrenci ödevlerini otomatik olarak analiz etmek ve değerlendirmek için geliştirilmiştir. Google Gemini API'sini kullanarak ödevlerin doğruluğunu ve uygunluğunu değerlendirir, puan verir ve kısa bir açıklama oluşturur. Sonuçlar, Excel dosyasına kaydedilir.

## Nasıl Çalışır?

Araç, aşağıdaki adımları izleyerek çalışır:

1.  **PDF'leri Okuma:** Belirtilen klasördeki tüm PDF dosyalarını okur ve metin içeriğini çıkarır.
2.  **Öğrenci Bilgilerini Çıkarma:** PDF içeriğinden öğrenci adını, soyadını ve ID'sini çıkarır. Bu işlem için "İSİM:", "SOYAD:" ve "İD:" ifadelerini arayan bir regex kullanılır. Bu ifadelerin PDF'lerde tutarlı bir şekilde bulunması gerekmektedir.
3.  **Gemini ile Değerlendirme:** Çıkarılan metni ve ödev açıklamasını Google Gemini API'sine göndererek ödevin doğruluğunu değerlendirmesini ister. Gemini'den bir puan (100 üzerinden) ve kısa bir açıklama beklenir.
4.  **Sonuçları Kaydetme:** Öğrenci bilgileri, verilen puan ve oluşturulan açıklama bir Excel dosyasına kaydedilir.

## Kurulum

Aracı kullanmak için aşağıdaki adımları izleyin:

1.  **Python Kurulumu:** Bilgisayarınızda Python'ın kurulu olduğundan emin olun (Python 3.7 veya üzeri önerilir).
2.  **Gerekli Kütüphaneleri Kurun:** Terminal veya komut istemcisini açın ve aşağıdaki komutları çalıştırın:

    ```bash
    pip install google-generativeai pymupdf pandas tkinter
    ```

3.  **API Anahtarı:** Bir Google Cloud projesi oluşturun ve Gemini API'sini etkinleştirin. Ardından, bir API anahtarı oluşturun.
4.  **`api_key.py` Dosyası Oluşturun:** Proje dizininizde `api_key.py` adında bir dosya oluşturun ve aşağıdaki satırı ekleyin (GERÇEK_API_ANAHTARINIZ yerine kendi API anahtarınızı girin):

    ```python
    your_api = "GERÇEK_API_ANAHTARINIZ"
    ```

5.  **Kodu İndirin:** Bu kodları içeren Python dosyasını (`main.py` gibi) indirin veya kopyalayın.

## Kullanım

1.  `main.py` dosyasını çalıştırın:

    ```bash
    python main.py
    ```

2.  Açılan arayüzde aşağıdaki bilgileri girin:
    *   **PDF Klasör Yolu:** Ödev PDF'lerinin bulunduğu klasörün yolunu seçin.
    *   **Ders Adı:** Dersin adını girin (örneğin, "Tarih").
    *   **Ödev Açıklaması:** Öğrencilerden ödevde ne istendiğini kısaca açıklayın (örneğin, "1. ve 2. Dünya Savaşları hakkında bilgi").
    *   **Kaydetme Konumu:** Excel dosyasının kaydedileceği konumu seçin.
3.  "Ödevleri Analiz Et" butonuna tıklayın.

## Dosya Formatı

Öğrenci bilgilerinin doğru şekilde çıkarılabilmesi için PDF dosyalarının aşağıdaki formatta olması gerekmektedir:

İSİM: Öğrenci Adı
SOYAD: Öğrenci Soyadı
İD: Öğrenci ID

Bu ifadelerin PDF'lerde tutarlı bir şekilde bulunması önemlidir.

## Hata Yönetimi

Araç, olası hataları tespit etmek ve kullanıcıya bilgilendirici mesajlar vermek için kapsamlı hata yönetimi içerir. Karşılaştığınız hatalarla ilgili detaylı bilgi için terminal çıktısını inceleyin.

## Katkıda Bulunma

Bu projeye katkıda bulunmak isterseniz, lütfen bir "pull request" gönderin.

## Lisans

Bu proje MIT Lisansı altında lisanslanmıştır.