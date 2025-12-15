import subprocess
import os

libreoffice_path = r"C:\Program Files\LibreOffice\program\soffice.exe"

def cevir(dosya_yolu):
    print(f"[Modül: Word -> PDF] {dosya_yolu} işleniyor...")
    
    komut = [
        libreoffice_path,
        '--headless',
        '--convert-to', 'pdf',
        '--outdir', os.getcwd(), # Ana klasöre kaydet
        dosya_yolu
    ]

    try:
        subprocess.run(komut, check=True)
        print("Word'den PDF'e dönüşüm başarılı.")
        return True
    except Exception as e:
        print(f"Hata: {e}")
        return False