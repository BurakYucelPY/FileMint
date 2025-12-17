"""
PDF Bölme Modülü
Tek bir PDF dosyasını sayfa sayfa ayırır ve ZIP olarak paketler.
"""

import os
import zipfile
from PyPDF2 import PdfReader, PdfWriter


def cevir(dosya_yolu):
    """PDF dosyasını sayfa sayfa ayırır ve ZIP olarak paketler."""
    try:
        if not dosya_yolu.lower().endswith('.pdf') or not os.path.exists(dosya_yolu):
            return False
        
        reader = PdfReader(dosya_yolu)
        toplam_sayfa = len(reader.pages)
        
        if toplam_sayfa < 1:
            return False
        
        dizin = os.path.dirname(dosya_yolu)
        dosya_adi = os.path.splitext(os.path.basename(dosya_yolu))[0]
        zip_adi = f"{dosya_adi}_sayfalar.zip"
        zip_yolu = os.path.join(dizin, zip_adi) if dizin else zip_adi
        
        with zipfile.ZipFile(zip_yolu, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for sayfa_no in range(toplam_sayfa):
                writer = PdfWriter()
                writer.add_page(reader.pages[sayfa_no])
                
                sayfa_adi = f"{dosya_adi}_sayfa_{sayfa_no + 1}.pdf"
                gecici_yol = os.path.join(dizin, sayfa_adi) if dizin else sayfa_adi
                
                with open(gecici_yol, 'wb') as f:
                    writer.write(f)
                
                zipf.write(gecici_yol, sayfa_adi)
                os.remove(gecici_yol)
        
        return True
        
    except Exception:
        return False


if __name__ == "__main__":
    # Test
    import sys
    if len(sys.argv) > 1:
        cevir(sys.argv[1])
    else:
        print("Kullanım: python pdf_split.py dosya.pdf")
