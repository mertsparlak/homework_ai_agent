import os
import google.generativeai as genai
import re
import pandas as pd
import fitz  
from api_key import your_api

# API Anahtarını ve modeli tanımlayın
api_key = your_api
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

# PDF dosyalarını ve klasörü belirtin
folder_path = input("Lütfen ödev PDF'lerinin bulunduğu klasörün yolunu girin: ")
course_name = input("Lütfen dersin adını girin: ")
assignment_desc = input("Lütfen ödevde öğrencilerden ne istediğinizi kısaca belirtin: ")

# Klasördeki PDF dosyalarını listele
pdf_files = [f for f in os.listdir(folder_path) if f.endswith(".pdf")]

# Sonuçları saklamak için bir liste oluştur
results = []

# Öğrencilerin isim, soyad, ID'lerini ve yanıtları çıkaran regexler
name_pattern = re.compile(r"([A-Za-z]+)\s+([A-Za-z]+)\s*ID:? (\d+)")

# PDF dosyalarını işle
for pdf_file in pdf_files:
    file_path = os.path.join(folder_path, pdf_file)
    print(f"Dosya işleniyor: {file_path}")

    try:
        doc = fitz.open(file_path)
        pdf_text = ""
        for page in doc:
            pdf_text += page.get_text()
        doc.close()
    except Exception as e:
        print(f"PDF okuma hatası: {e}")
        results.append({ # Hata durumunda sonuçları kaydet
            "Öğrenci Adı": "Bilinmiyor",
            "Öğrenci Soyadı": "Bilinmiyor",
            "Öğrenci ID": "Bilinmiyor",
            "Puan": "PDF Okuma Hatası",
            "Açıklama": str(e)
        })
        continue

    prompt = f"Ödevde istenen: {assignment_desc}. Bu ödevin doğruluğu nedir? Puan ver (10 üzerinden) ve açıklama yap. PDF içeriği aşağıdadır:\n\n{pdf_text}"

    try:
        response = model.generate_content(prompt)
        response_text = response.text
        print(f"Gemini yanıtı: {response_text}")

        try:
            score_match = re.search(r"Puan:\s*(\d+)/10", response_text, re.IGNORECASE)
            explanation_match = re.search(r"(Açıklama:|Explanation:)\s*(.+)", response_text, re.IGNORECASE)

            score = int(score_match.group(1)) if score_match else "Puan alınamadı"
            explanation = explanation_match.group(2).strip() if explanation_match else "Açıklama alınamadı"
        except Exception as e:
            score = "Açıklama ayrıştırma hatası"
            explanation = str(e)

    except Exception as e:
        print(f"Gemini API hatası: {e}")
        score = "API Hatası"
        explanation = str(e)

    student_match = name_pattern.search(pdf_file)
    if student_match:
        first_name = student_match.group(1)
        last_name = student_match.group(2)
        student_id = student_match.group(3)
    else:
        first_name = "Bilinmiyor"
        last_name = "Bilinmiyor"
        student_id = "Bilinmiyor"

    results.append({
        "Öğrenci Adı": first_name,
        "Öğrenci Soyadı": last_name,
        "Öğrenci ID": student_id,
        "Puan": score,
        "Açıklama": explanation
    })

# Sonuçları bir DataFrame'e dönüştür ve kaydet
df = pd.DataFrame(results)
output_file = os.path.join(folder_path, f"{course_name}_odev_analizi.xlsx")
df.to_excel(output_file, index=False)
print(f"Sonuçlar {output_file} adresine kaydedildi.")