import os
import google.generativeai as genai
import re
import pandas as pd
import fitz

# API anahtarını ve modeli tanımla
from api_key import your_api
api_key = your_api
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

# Klasör yolu, ders adı ve ödev açıklamasını al
folder_path = input("Lütfen ödev PDF'lerinin bulunduğu klasörün yolunu girin: ")
course_name = input("Lütfen dersin adını girin: ")
assignment_desc = input("Lütfen ödevde öğrencilerden ne istediğinizi kısaca belirtin: ")

# PDF dosyalarını listele
pdf_files = [f for f in os.listdir(folder_path) if f.endswith(".pdf")]

# Sonuçları saklamak için liste oluştur
results = []

# Öğrenci bilgilerini PDF içeriğinden çıkaran regex
info_pattern = re.compile(r"İSİM:\s*([A-Za-zÇŞĞÜÖİçşğüöı]+)\s*SOYAD:\s*([A-Za-zÇŞĞÜÖİçşğüöı]+)\s*İD:\s*(\d+)", re.IGNORECASE)

# Her PDF dosyasını işle
for pdf_file in pdf_files:
    file_path = os.path.join(folder_path, pdf_file)
    print(f"\nDosya işleniyor: {file_path}")

    first_name = "Bulunamadı"
    last_name = "Bulunamadı"
    student_id = "Bulunamadı"
    score = "Değerlendirilemedi"
    explanation = "Değerlendirilemedi"

    try:
        doc = fitz.open(file_path)
        pdf_text = ""
        for page in doc:
            pdf_text += page.get_text()
        doc.close()

        info_match = info_pattern.search(pdf_text)
        if info_match:
            first_name = info_match.group(1).strip()
            last_name = info_match.group(2).strip()
            student_id = info_match.group(3).strip()
            print(f"Öğrenci bilgileri PDF'den bulundu: Ad: {first_name}, Soyad: {last_name}, ID: {student_id}")
        else:
            print(f"!!! Öğrenci bilgileri PDF'de BULUNAMADI: {pdf_file}")

        prompt = f"Ödevde istenen: {assignment_desc}. Bu ödev istenilene ne kadar uygun ve doğrudur? Puan ver (100 üzerinden ve yazarken Puan: diye belirt) ve en fazla iki cümlelik kısa ve öz bir açıklama yap (Açıklama: diye belirt). PDF içeriği aşağıdadır:\n\n{pdf_text}"
        try:
            response = model.generate_content(prompt)
            response_text = response.text
            print(f"Gemini yanıtı: {response_text}")

            score_match = re.search(r"(Puan:|Score:)\s*(\d+)", response_text, re.IGNORECASE)
            explanation_match = re.search(r"(Açıklama:|Explanation:|Özet:|Summary:)\s*(.+)", response_text, re.IGNORECASE | re.DOTALL)

            if score_match:
                score = int(score_match.group(2))
            else:
                print(f"!!! Puan regex ile bulunamadı. Tam yanıt: {response_text}")

            if explanation_match:
                explanation = explanation_match.group(2).strip()
                sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', explanation)
                explanation = " ".join(sentences[:2]) if len(sentences) >= 2 else (explanation[:100] + "...") if len(explanation)>100 else explanation
            else:
                print(f"!!! Açıklama regex ile bulunamadı. Tam yanıt: {response_text}")

        except Exception as e:
            print(f"!!! Gemini API hatası: {e}")

    except Exception as e:
        print(f"!!! Genel Hata: {e}")
        
    results.append({
        "Öğrenci Adı": first_name,
        "Öğrenci Soyadı": last_name,
        "Öğrenci ID": student_id,
        "Puan": score,
        "Açıklama": explanation
    })

# Sonuçları DataFrame'e dönüştür ve Excel'e kaydet
df = pd.DataFrame(results)
output_file = os.path.join(folder_path, f"{course_name}_odev_analizi.xlsx")
df.to_excel(output_file, index=False)
print(f"\nSonuçlar {output_file} adresine kaydedildi.")