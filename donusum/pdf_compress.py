"""
PDF Sıkıştırma Modülü
PDF dosyasının boyutunu küçültür.
"""

import os
import fitz  # PyMuPDF


def cevir(dosya_yolu, kalite=50):
    """PDF dosyasını sıkıştırır."""
    try:
        if not dosya_yolu.lower().endswith('.pdf') or not os.path.exists(dosya_yolu):
            return False
        
        doc = fitz.open(dosya_yolu)
        
        dizin = os.path.dirname(dosya_yolu)
        dosya_adi = os.path.splitext(os.path.basename(dosya_yolu))[0]
        cikti_yolu = os.path.join(dizin, f"{dosya_adi}_sikistirilmis.pdf") if dizin else f"{dosya_adi}_sikistirilmis.pdf"
        
        for sayfa_no in range(len(doc)):
            sayfa = doc[sayfa_no]
            gorseller = sayfa.get_images(full=True)
            
            for gorsel in gorseller:
                xref = gorsel[0]
                try:
                    base_image = doc.extract_image(xref)
                    if base_image:
                        image_bytes = base_image["image"]
                        from PIL import Image
                        import io
                        
                        img = Image.open(io.BytesIO(image_bytes))
                        if img.mode in ('RGBA', 'P'):
                            img = img.convert('RGB')
                        
                        output = io.BytesIO()
                        img.save(output, format='JPEG', quality=kalite, optimize=True)
                        compressed_bytes = output.getvalue()
                        
                        if len(compressed_bytes) < len(image_bytes):
                            doc.update_stream(xref, compressed_bytes)
                except Exception:
                    continue
        
        doc.save(cikti_yolu, garbage=4, deflate=True, clean=True)
        doc.close()
        return True
        
    except Exception:
        return False


if __name__ == "__main__":
    # Test
    import sys
    if len(sys.argv) > 1:
        kalite = int(sys.argv[2]) if len(sys.argv) > 2 else 50
        cevir(sys.argv[1], kalite)
    else:
        print("Kullanım: python pdf_compress.py dosya.pdf [kalite]")
