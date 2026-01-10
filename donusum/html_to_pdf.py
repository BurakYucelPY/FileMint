"""
HTML → PDF Dönüştürücü Modülü
HTML dosyalarını PDF formatına dönüştürür.
"""

import os


def cevir(dosya_yolu):
    """HTML dosyasını PDF'e dönüştürür."""
    try:
        if not dosya_yolu.lower().endswith(('.html', '.htm')) or not os.path.exists(dosya_yolu):
            return False
        
        dizin = os.path.dirname(dosya_yolu)
        dosya_adi = os.path.splitext(os.path.basename(dosya_yolu))[0]
        cikti_yolu = os.path.join(dizin, f"{dosya_adi}.pdf") if dizin else f"{dosya_adi}.pdf"
        
        from weasyprint import HTML
        HTML(filename=dosya_yolu).write_pdf(cikti_yolu)
        
        return True
        
    except Exception:
        return False


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        cevir(sys.argv[1])
    else:
        print("Kullanım: python html_to_pdf.py dosya.html")
