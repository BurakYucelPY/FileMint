import subprocess
import os
import shutil

def get_libreoffice_path():
    """LibreOffice yolunu dinamik olarak tespit eder."""
    # Önce PATH'te ara
    soffice = shutil.which("soffice")
    if soffice:
        return soffice
    
    # Windows için bilinen yolları kontrol et
    windows_paths = [
        r"C:\Program Files\LibreOffice\program\soffice.exe",
        r"C:\Program Files (x86)\LibreOffice\program\soffice.exe",
    ]
    for path in windows_paths:
        if os.path.exists(path):
            return path
    
    return None

def cevir(dosya_yolu):
    print(f"[Modül: Word -> PDF] {dosya_yolu} işleniyor...")
    
    libreoffice_path = get_libreoffice_path()
    if not libreoffice_path:
        print("❌ LibreOffice bulunamadı. Lütfen LibreOffice'i yükleyin.")
        return False
    
    komut = [
        libreoffice_path,
        '--headless',
        '--convert-to', 'pdf',
        '--outdir', os.getcwd(),
        dosya_yolu
    ]

    try:
        subprocess.run(komut, check=True, capture_output=True)
        print("✅ Word'den PDF'e dönüşüm başarılı.")
        return True
    except Exception as e:
        print(f"❌ Hata: {e}")
        return False