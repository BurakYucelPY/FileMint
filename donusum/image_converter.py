from PIL import Image
import os

def jpg_to_png(dosya_yolu):
    """JPG dosyasını PNG'ye dönüştürür."""
    print(f"🔄 [Modül: JPG -> PNG] {dosya_yolu} işleniyor...")
    
    try:
        img = Image.open(dosya_yolu)
        
        # Çıktı dosya adı
        cikti_dosya = os.path.splitext(dosya_yolu)[0] + ".png"
        
        img.save(cikti_dosya, "PNG")
        print(f"✅ JPG'den PNG'ye dönüşüm başarılı: {cikti_dosya}")
        return True
    except Exception as e:
        print(f"❌ Hata: {e}")
        return False


def png_to_jpg(dosya_yolu, kalite=95):
    """PNG dosyasını JPG'ye dönüştürür."""
    print(f"🔄 [Modül: PNG -> JPG] {dosya_yolu} işleniyor...")
    
    try:
        img = Image.open(dosya_yolu)
        
        # RGBA ise RGB'ye çevir (JPG transparanlık desteklemez)
        if img.mode == 'RGBA':
            # Beyaz arka plan oluştur
            background = Image.new('RGB', img.size, (255, 255, 255))
            background.paste(img, mask=img.split()[3])
            img = background
        elif img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Çıktı dosya adı
        cikti_dosya = os.path.splitext(dosya_yolu)[0] + ".jpg"
        
        img.save(cikti_dosya, "JPEG", quality=kalite)
        print(f"✅ PNG'den JPG'ye dönüşüm başarılı: {cikti_dosya}")
        return True
    except Exception as e:
        print(f"❌ Hata: {e}")
        return False


def cevir(dosya_yolu):
    """Dosya uzantısına göre otomatik dönüşüm yapar."""
    uzanti = os.path.splitext(dosya_yolu)[1].lower()
    
    if uzanti in ['.jpg', '.jpeg']:
        return jpg_to_png(dosya_yolu)
    elif uzanti == '.png':
        return png_to_jpg(dosya_yolu)
    else:
        print(f"❌ Desteklenmeyen format: {uzanti}")
        return False
