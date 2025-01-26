import os
import google.generativeai as genai
import re
import pandas as pd
import fitz
import tkinter as tk
from tkinter import filedialog, messagebox
from api_key import your_api

# api anahtarı ve modeli tanımlama
api_key = your_api
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

def analyze_assignments():
    folder_path = folder_path_entry.get()
    course_name = course_name_entry.get()
    assignment_desc = assignment_desc_entry.get()
    save_path = save_path_entry.get()

    if not all([folder_path, course_name, assignment_desc, save_path]):
        messagebox.showerror("Hata", "Lütfen tüm alanları doldurun.")
        return

    pdf_files = [f for f in os.listdir(folder_path) if f.endswith(".pdf")]
    results = []
    info_pattern = re.compile(r"İSİM:\s*([A-Za-zÇŞĞÜÖİçşğüöı]+)\s*SOYAD:\s*([A-Za-zÇŞĞÜÖİçşğüöı]+)\s*İD:\s*(\d+)", re.IGNORECASE)

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

    try:
        df = pd.DataFrame(results)
        output_file = os.path.join(save_path, f"{course_name}_odev_analizi.xlsx")
        df.to_excel(output_file, index=False)
        messagebox.showinfo("Başarılı", f"Sonuçlar {output_file} adresine kaydedildi.")
    except Exception as e:
        messagebox.showerror("Kaydetme Hatası", str(e))

def browse_folder():
    filename = filedialog.askdirectory()
    folder_path_entry.delete(0, tk.END)
    folder_path_entry.insert(0, filename)

def browse_save_path():
    filename = filedialog.askdirectory()
    save_path_entry.delete(0, tk.END)
    save_path_entry.insert(0, filename)

# Arayüz oluştur
window = tk.Tk()
window.title("Ödev Analiz Aracı")

# Etiketler ve giriş alanları
tk.Label(window, text="PDF Klasör Yolu:").grid(row=0, column=0, sticky="w")
folder_path_entry = tk.Entry(window, width=50)
folder_path_entry.grid(row=0, column=1, sticky="ew")
tk.Button(window, text="Gözat", command=browse_folder).grid(row=0, column=2)

tk.Label(window, text="Ders Adı:").grid(row=1, column=0, sticky="w")
course_name_entry = tk.Entry(window, width=50)
course_name_entry.grid(row=1, column=1, sticky="ew")

tk.Label(window, text="Ödev Açıklaması:").grid(row=2, column=0, sticky="w")
assignment_desc_entry = tk.Entry(window, width=50)
assignment_desc_entry.grid(row=2, column=1, sticky="ew")

tk.Label(window, text="Kaydetme Konumu").grid(row=3, column=0, sticky="w")
save_path_entry = tk.Entry(window, width=50)
save_path_entry.grid(row=3, column=1, sticky="ew")
tk.Button(window, text="Gözat", command=browse_save_path).grid(row=3, column=2)

# Analiz butonu
analyze_button = tk.Button(window, text="Ödevleri Analiz Et", command=analyze_assignments)
analyze_button.grid(row=4, column=0, columnspan=3, pady=10)

window.mainloop()