from PIL import Image
import os

def cevir(dosya_yollari, cikti_dosya="birlesik.pdf"):
    """
    Bir veya birden fazla resmi tek bir PDF'e birleştirir.
    
    Args:
        dosya_yollari: Tek dosya yolu (str) veya dosya yolları listesi (list)
        cikti_dosya: Çıktı PDF dosyasının adı
    """
    print(f"🖼️ [Modül: Resim -> PDF] işleniyor...")
    
    # Tek dosya ise listeye çevir
    if isinstance(dosya_yollari, str):
        dosya_yollari = [dosya_yollari]
    
    try:
        resimler = []
        
        for dosya_yolu in dosya_yollari:
            img = Image.open(dosya_yolu)
            # RGB'ye çevir (PNG'deki RGBA için gerekli)
            if img.mode == 'RGBA':
                img = img.convert('RGB')
            elif img.mode != 'RGB':
                img = img.convert('RGB')
            resimler.append(img)
            print(f"   📷 Eklendi: {dosya_yolu}")
        
        if resimler:
            # İlk resmi kaydet, diğerlerini ekle
            ilk_resim = resimler[0]
            diger_resimler = resimler[1:] if len(resimler) > 1 else []
            
            ilk_resim.save(cikti_dosya, "PDF", save_all=True, append_images=diger_resimler)
            print(f"✅ Resimler PDF'e dönüştürüldü: {cikti_dosya}")
            return True
        else:
            print("❌ Hiç resim bulunamadı.")
            return False
            
    except Exception as e:
        print(f"❌ Hata: {e}")
        return False
