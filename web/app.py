from flask import Flask, render_template, request, send_file, jsonify
import os
import sys
import tempfile
import logging

# Donusum klasörünü import edebilmek için path'e ekle
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from donusum import (
    txt_to_pdf,
    word_to_pdf,
    pdf_to_word,
    pdf_to_txt,
    pdf_to_image,
    image_to_pdf,
    image_converter,
    excel_to_pdf,
    powerpoint_to_pdf,
    pdf_merge,
    pdf_split,
    pdf_compress,
    markdown_converter,
    html_to_pdf,
    csv_excel_converter
)

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50 MB limit

# Geçici dosyalar için klasör
UPLOAD_FOLDER = tempfile.mkdtemp()

# Dönüşüm türleri
DONUSUM_TURLERI = {
    'pdf-to-word': {
        'isim': 'PDF → Word',
        'aciklama': 'PDF dosyasını Word belgesine dönüştür',
        'uzanti': ['.pdf'],
        'cikti': '.docx',
        'fonksiyon': pdf_to_word.cevir
    },
    'word-to-pdf': {
        'isim': 'Word → PDF',
        'aciklama': 'Word belgesini PDF dosyasına dönüştür',
        'uzanti': ['.docx', '.doc'],
        'cikti': '.pdf',
        'fonksiyon': word_to_pdf.cevir
    },
    'pdf-to-txt': {
        'isim': 'PDF → TXT',
        'aciklama': 'PDF dosyasından metin çıkar',
        'uzanti': ['.pdf'],
        'cikti': '.txt',
        'fonksiyon': pdf_to_txt.cevir
    },
    'txt-to-pdf': {
        'isim': 'TXT → PDF',
        'aciklama': 'Metin dosyasını PDF\'e dönüştür',
        'uzanti': ['.txt'],
        'cikti': '.pdf',
        'fonksiyon': txt_to_pdf.cevir
    },
    'image-to-pdf': {
        'isim': 'Resim → PDF',
        'aciklama': 'Resim dosyasını PDF\'e dönüştür',
        'uzanti': ['.jpg', '.jpeg', '.png'],
        'cikti': '.pdf',
        'fonksiyon': image_to_pdf.cevir
    },
    'jpg-to-png': {
        'isim': 'JPG → PNG',
        'aciklama': 'JPG resmini PNG formatına dönüştür',
        'uzanti': ['.jpg', '.jpeg'],
        'cikti': '.png',
        'fonksiyon': image_converter.jpg_to_png
    },
    'png-to-jpg': {
        'isim': 'PNG → JPG',
        'aciklama': 'PNG resmini JPG formatına dönüştür',
        'uzanti': ['.png'],
        'cikti': '.jpg',
        'fonksiyon': image_converter.png_to_jpg
    },
    'excel-to-pdf': {
        'isim': 'Excel → PDF',
        'aciklama': 'Excel dosyasını PDF\'e dönüştür',
        'uzanti': ['.xlsx', '.xls'],
        'cikti': '.pdf',
        'fonksiyon': excel_to_pdf.cevir
    },
    'powerpoint-to-pdf': {
        'isim': 'PowerPoint → PDF',
        'aciklama': 'PowerPoint sunumunu PDF\'e dönüştür',
        'uzanti': ['.pptx', '.ppt'],
        'cikti': '.pdf',
        'fonksiyon': powerpoint_to_pdf.cevir
    },
    'pdf-merge': {
        'isim': 'PDF Birleştir',
        'aciklama': 'Birden fazla PDF dosyasını tek dosyada birleştir',
        'uzanti': ['.pdf'],
        'cikti': '.pdf',
        'fonksiyon': pdf_merge.cevir,
        'coklu': True  # Çoklu dosya kabul eder
    },
    'pdf-split': {
        'isim': 'PDF Böl',
        'aciklama': 'PDF dosyasını sayfa sayfa ayır (ZIP olarak indir)',
        'uzanti': ['.pdf'],
        'cikti': '.zip',
        'fonksiyon': pdf_split.cevir
    },
    'pdf-compress': {
        'isim': 'PDF Sıkıştır',
        'aciklama': 'PDF dosya boyutunu küçült',
        'uzanti': ['.pdf'],
        'cikti': '.pdf',
        'fonksiyon': pdf_compress.cevir
    },
    'markdown-to-html': {
        'isim': 'Markdown → HTML',
        'aciklama': 'Markdown dosyasını HTML\'e dönüştür',
        'uzanti': ['.md'],
        'cikti': '.html',
        'fonksiyon': markdown_converter.md_to_html
    },
    'markdown-to-pdf': {
        'isim': 'Markdown → PDF',
        'aciklama': 'Markdown dosyasını PDF\'e dönüştür',
        'uzanti': ['.md'],
        'cikti': '.pdf',
        'fonksiyon': markdown_converter.md_to_pdf
    },
    'html-to-pdf': {
        'isim': 'HTML → PDF',
        'aciklama': 'HTML dosyasını PDF\'e dönüştür',
        'uzanti': ['.html', '.htm'],
        'cikti': '.pdf',
        'fonksiyon': html_to_pdf.cevir
    },
    'csv-to-excel': {
        'isim': 'CSV → Excel',
        'aciklama': 'CSV dosyasını Excel formatına dönüştür',
        'uzanti': ['.csv'],
        'cikti': '.xlsx',
        'fonksiyon': csv_excel_converter.csv_to_excel
    },
    'excel-to-csv': {
        'isim': 'Excel → CSV',
        'aciklama': 'Excel dosyasını CSV formatına dönüştür',
        'uzanti': ['.xlsx', '.xls'],
        'cikti': '.csv',
        'fonksiyon': csv_excel_converter.excel_to_csv
    }
}


@app.route('/')
def anasayfa():
    return render_template('index.html', donusumler=DONUSUM_TURLERI)


@app.route('/donustur/<tur>')
def donustur_sayfa(tur):
    if tur not in DONUSUM_TURLERI:
        return "Geçersiz dönüşüm türü", 404
    
    bilgi = DONUSUM_TURLERI[tur]
    return render_template('convert.html', tur=tur, bilgi=bilgi)


@app.route('/yukle/<tur>', methods=['POST'])
def dosya_yukle(tur):
    if tur not in DONUSUM_TURLERI:
        return jsonify({'hata': 'Geçersiz dönüşüm türü'}), 400
    
    bilgi = DONUSUM_TURLERI[tur]
    coklu_dosya = bilgi.get('coklu', False)
    
    # Çoklu dosya desteği (PDF birleştirme için)
    if coklu_dosya:
        if 'dosya' not in request.files:
            return jsonify({'hata': 'Dosya bulunamadı'}), 400
        
        dosyalar = request.files.getlist('dosya')
        if len(dosyalar) < 2:
            return jsonify({'hata': 'En az 2 dosya gerekli'}), 400
        
        try:
            gecici_klasor = tempfile.mkdtemp()
            dosya_yollari = []
            
            for dosya in dosyalar:
                if dosya.filename == '':
                    continue
                    
                dosya_uzanti = os.path.splitext(dosya.filename)[1].lower()
                if dosya_uzanti not in bilgi['uzanti']:
                    return jsonify({'hata': f'Geçersiz dosya türü: {dosya.filename}'}), 400
                
                girdi_yolu = os.path.join(gecici_klasor, dosya.filename)
                dosya.save(girdi_yolu)
                dosya_yollari.append(girdi_yolu)
            
            eski_cwd = os.getcwd()
            os.chdir(gecici_klasor)
            
            sonuc = bilgi['fonksiyon'](dosya_yollari)
            
            os.chdir(eski_cwd)
            
            if sonuc:
                beklenen_uzanti = bilgi['cikti']
                for f in os.listdir(gecici_klasor):
                    if f.lower().endswith(beklenen_uzanti) and f not in [os.path.basename(d) for d in dosya_yollari]:
                        cikti_yolu = os.path.join(gecici_klasor, f)
                        return send_file(
                            cikti_yolu,
                            as_attachment=True,
                            download_name=f,
                            mimetype='application/octet-stream'
                        )
                return jsonify({'hata': 'Çıktı dosyası oluşturulamadı'}), 500
            else:
                return jsonify({'hata': 'Dönüşüm başarısız oldu'}), 500
                
        except Exception as e:
            return jsonify({'hata': str(e)}), 500
    
    # Tekli dosya işleme (mevcut kod)
    if 'dosya' not in request.files:
        return jsonify({'hata': 'Dosya bulunamadı'}), 400
    
    dosya = request.files['dosya']
    if dosya.filename == '':
        return jsonify({'hata': 'Dosya seçilmedi'}), 400
    
    # Uzantı kontrolü
    dosya_uzanti = os.path.splitext(dosya.filename)[1].lower()
    if dosya_uzanti not in bilgi['uzanti']:
        return jsonify({'hata': f'Geçersiz dosya türü. Kabul edilen: {", ".join(bilgi["uzanti"])}'}), 400
    
    try:
        # Geçici klasör oluştur
        gecici_klasor = tempfile.mkdtemp()
        
        # Dosyayı kaydet
        girdi_yolu = os.path.join(gecici_klasor, dosya.filename)
        dosya.save(girdi_yolu)
        
        # Çalışma dizinini geçici klasöre değiştir
        eski_cwd = os.getcwd()
        os.chdir(gecici_klasor)
        
        # Dönüşümü yap
        sonuc = bilgi['fonksiyon'](girdi_yolu)
        
        # Çalışma dizinini geri al
        os.chdir(eski_cwd)
        
        if sonuc:
            # Çıktı dosyasını bul
            dosya_adi = os.path.splitext(dosya.filename)[0]
            beklenen_uzanti = bilgi['cikti']
            
            # Klasördeki dosyaları tara ve çıktıyı bul
            cikti_yolu = None
            cikti_dosya = None
            
            for f in os.listdir(gecici_klasor):
                # Orijinal dosyayı atla
                if f == dosya.filename:
                    continue
                    
                # Beklenen uzantıyla biten dosyayı bul
                if f.lower().endswith(beklenen_uzanti):
                    cikti_yolu = os.path.join(gecici_klasor, f)
                    # İndirme için temiz dosya adı oluştur
                    cikti_dosya = dosya_adi + beklenen_uzanti
                    break
            
            if cikti_yolu and os.path.exists(cikti_yolu):
                return send_file(
                    cikti_yolu,
                    as_attachment=True,
                    download_name=cikti_dosya,
                    mimetype='application/octet-stream'
                )
            else:
                return jsonify({'hata': 'Çıktı dosyası oluşturulamadı'}), 500
        else:
            return jsonify({'hata': 'Dönüşüm başarısız oldu'}), 500
            
    except Exception as e:
        return jsonify({'hata': str(e)}), 500


if __name__ == '__main__':
    # Render.com ve diğer bulut platformları için PORT ortam değişkenini kullan
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
