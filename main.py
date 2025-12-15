import os

from donusum import word_to_pdf, pdf_to_word

def yonetici(dosya_ismi):

    if not os.path.exists(dosya_ismi):
        print("Dosya bulunamadı!")
        return
    uzanti = dosya_ismi.split('.')[-1].lower()
    if uzanti in ['docx', 'doc']:
        word_to_pdf.cevir(dosya_ismi)
    
    elif uzanti == 'pdf':
        pdf_to_word.cevir(dosya_ismi)        
    else:
        print("⚠️ Bu dosya türünü tanıyan bir işçimiz yok.")

# --- TEST ---
print("--- SİSTEM BAŞLATILDI ---")

yonetici("deneme.docx")