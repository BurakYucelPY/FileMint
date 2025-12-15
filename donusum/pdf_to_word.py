from docx import Document
import PyPDF2
import os

def cevir(dosya_yolu):
    print(f"📑 [Modül: PDF -> Word] {dosya_yolu} işleniyor...")
    
    # Çıktı dosyasının ismini ayarla (deneme.pdf -> deneme.docx)
    word_dosyasi = dosya_yolu.replace('.pdf', '.docx')

    try:
        # PDF'den metin çıkar
        with open(dosya_yolu, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            
            # Yeni Word belgesi oluştur
            doc = Document()
            
            # Her sayfayı oku ve Word'e ekle
            for sayfa_num in range(len(pdf_reader.pages)):
                sayfa = pdf_reader.pages[sayfa_num]
                metin = sayfa.extract_text()
                
                # Metni Word belgesine ekle
                doc.add_paragraph(metin)
                
                # Sayfa arası boşluk
                if sayfa_num < len(pdf_reader.pages) - 1:
                    doc.add_page_break()
            
            # Word belgesini kaydet
            doc.save(word_dosyasi)
            
        print(f"✅ PDF'ten Word'e dönüşüm başarılı: {word_dosyasi}")
        return True
    except Exception as e:
        print(f"❌ Hata: {e}")
        return False