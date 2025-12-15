import subprocess
import os

libreoffice_path = r"C:\Program Files\LibreOffice\program\soffice.exe"

def cevir(dosya_yolu):
    print(f"📽️ [Modül: PowerPoint -> PDF] {dosya_yolu} işleniyor...")
    
    komut = [
        libreoffice_path,
        '--headless',
        '--convert-to', 'pdf',
        '--outdir', os.getcwd(),
        dosya_yolu
    ]

    try:
        subprocess.run(komut, check=True)
        print(f"✅ PowerPoint'ten PDF'e dönüşüm başarılı.")
        return True
    except Exception as e:
        print(f"❌ Hata: {e}")
        return False
