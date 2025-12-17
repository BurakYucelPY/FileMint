"""
PDF Birleştirme Modülü
Birden fazla PDF dosyasını tek bir PDF'de birleştirir.
"""

import os
from PyPDF2 import PdfMerger


def cevir(dosya_yollari):
    """Birden fazla PDF dosyasını birleştirir."""
    try:
        if isinstance(dosya_yollari, str):
            dosya_yollari = [dosya_yollari]
        
        if len(dosya_yollari) < 2:
            return False
        
        for dosya in dosya_yollari:
            if not dosya.lower().endswith('.pdf') or not os.path.exists(dosya):
                return False
        
        merger = PdfMerger()
        for dosya in dosya_yollari:
            merger.append(dosya)
        
        ilk_dosya = dosya_yollari[0]
        dizin = os.path.dirname(ilk_dosya)
        cikti_yolu = os.path.join(dizin, "birlestirilmis.pdf") if dizin else "birlestirilmis.pdf"
        
        merger.write(cikti_yolu)
        merger.close()
        return True
        
    except Exception:
        return False


if __name__ == "__main__":
    # Test
    import sys
    if len(sys.argv) > 2:
        cevir(sys.argv[1:])
    else:
        print("Kullanım: python pdf_merge.py dosya1.pdf dosya2.pdf ...")
