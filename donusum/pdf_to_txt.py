import PyPDF2
import os

def cevir(dosya_yolu):
    print(f"📄 [Modül: PDF -> Metin] {dosya_yolu} işleniyor...")
    
    # Çıktı dosyasının ismini ayarla
    txt_dosyasi = dosya_yolu.replace('.pdf', '.txt')
    
    try:
        with open(dosya_yolu, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            
            tum_metin = ""
            
            for sayfa_num in range(len(pdf_reader.pages)):
                sayfa = pdf_reader.pages[sayfa_num]
                metin = sayfa.extract_text()
                tum_metin += f"--- Sayfa {sayfa_num + 1} ---\n"
                tum_metin += metin + "\n\n"
            
            # Metin dosyasına kaydet
            with open(txt_dosyasi, 'w', encoding='utf-8') as txt_file:
                txt_file.write(tum_metin)
        
        print(f"✅ PDF'ten metin çıkarma başarılı: {txt_dosyasi}")
        return True
    except Exception as e:
        print(f"❌ Hata: {e}")
        return False
