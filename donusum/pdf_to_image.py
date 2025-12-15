import fitz  # PyMuPDF
import os

def cevir(dosya_yolu, format="png", dpi=200):
    print(f"🖼️ [Modül: PDF -> Resim] {dosya_yolu} işleniyor...")
    
    try:
        pdf_document = fitz.open(dosya_yolu)
        dosya_adi = os.path.splitext(os.path.basename(dosya_yolu))[0]
        toplam_sayfa = len(pdf_document)
        
        for sayfa_num in range(toplam_sayfa):
            sayfa = pdf_document[sayfa_num]
            
            # DPI ayarı için zoom faktörü
            zoom = dpi / 72
            mat = fitz.Matrix(zoom, zoom)
            
            # Sayfayı resme çevir
            pix = sayfa.get_pixmap(matrix=mat)
            
            # Çıktı dosya adı
            cikti_dosya = f"{dosya_adi}_sayfa_{sayfa_num + 1}.{format}"
            pix.save(cikti_dosya)
            print(f"   📄 Sayfa {sayfa_num + 1} kaydedildi: {cikti_dosya}")
        
        pdf_document.close()
        print(f"✅ PDF'ten resme dönüşüm başarılı. Toplam {toplam_sayfa} sayfa.")
        return True
    except Exception as e:
        print(f"❌ Hata: {e}")
        return False
