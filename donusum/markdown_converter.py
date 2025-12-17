"""
Markdown Dönüştürücü Modülü
Markdown dosyalarını PDF veya HTML formatına dönüştürür.
"""

import os
import markdown


def md_to_html(dosya_yolu):
    """Markdown dosyasını HTML'e dönüştürür."""
    try:
        if not dosya_yolu.lower().endswith('.md') or not os.path.exists(dosya_yolu):
            return False
        
        with open(dosya_yolu, 'r', encoding='utf-8') as f:
            md_icerik = f.read()
        
        html_icerik = markdown.markdown(
            md_icerik,
            extensions=['tables', 'fenced_code', 'codehilite', 'toc']
        )
        
        # Tam HTML belgesi oluştur
        html_sablon = f"""<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{os.path.basename(dosya_yolu)}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            max-width: 800px;
            margin: 40px auto;
            padding: 20px;
            line-height: 1.6;
            color: #333;
        }}
        h1, h2, h3, h4, h5, h6 {{
            color: #2c3e50;
            margin-top: 24px;
        }}
        code {{
            background-color: #f4f4f4;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Consolas', 'Monaco', monospace;
        }}
        pre {{
            background-color: #f4f4f4;
            padding: 16px;
            border-radius: 6px;
            overflow-x: auto;
        }}
        pre code {{
            padding: 0;
            background: none;
        }}
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 16px 0;
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 8px 12px;
            text-align: left;
        }}
        th {{
            background-color: #f4f4f4;
        }}
        blockquote {{
            border-left: 4px solid #3498db;
            margin: 16px 0;
            padding-left: 16px;
            color: #666;
        }}
        a {{
            color: #3498db;
        }}
        img {{
            max-width: 100%;
            height: auto;
        }}
    </style>
</head>
<body>
{html_icerik}
</body>
</html>"""
        
        dizin = os.path.dirname(dosya_yolu)
        dosya_adi = os.path.splitext(os.path.basename(dosya_yolu))[0]
        cikti_yolu = os.path.join(dizin, f"{dosya_adi}.html") if dizin else f"{dosya_adi}.html"
        
        with open(cikti_yolu, 'w', encoding='utf-8') as f:
            f.write(html_sablon)
        
        return True
        
    except Exception:
        return False


def md_to_pdf(dosya_yolu):
    """Markdown dosyasını PDF'e dönüştürür."""
    try:
        if not dosya_yolu.lower().endswith('.md') or not os.path.exists(dosya_yolu):
            return False
        
        with open(dosya_yolu, 'r', encoding='utf-8') as f:
            md_icerik = f.read()
        
        html_icerik = markdown.markdown(
            md_icerik,
            extensions=['tables', 'fenced_code', 'codehilite', 'toc']
        )
        
        html_sablon = f"""<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <style>
        @page {{
            size: A4;
            margin: 2cm;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            font-size: 12pt;
            line-height: 1.6;
            color: #333;
        }}
        h1 {{ font-size: 24pt; color: #2c3e50; }}
        h2 {{ font-size: 18pt; color: #2c3e50; }}
        h3 {{ font-size: 14pt; color: #2c3e50; }}
        code {{
            background-color: #f4f4f4;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Consolas', monospace;
            font-size: 10pt;
        }}
        pre {{
            background-color: #f4f4f4;
            padding: 12px;
            border-radius: 6px;
            overflow-x: auto;
        }}
        table {{
            border-collapse: collapse;
            width: 100%;
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 8px;
        }}
        th {{
            background-color: #f4f4f4;
        }}
    </style>
</head>
<body>
{html_icerik}
</body>
</html>"""
        
        dizin = os.path.dirname(dosya_yolu)
        dosya_adi = os.path.splitext(os.path.basename(dosya_yolu))[0]
        cikti_yolu = os.path.join(dizin, f"{dosya_adi}.pdf") if dizin else f"{dosya_adi}.pdf"
        
        try:
            from weasyprint import HTML
            HTML(string=html_sablon).write_pdf(cikti_yolu)
        except ImportError:
            return False
        
        return True
        
    except Exception:
        return False


def cevir(dosya_yolu):
    """Markdown dosyasını HTML'e dönüştürür."""
    return md_to_html(dosya_yolu)


def cevir_pdf(dosya_yolu):
    """Markdown dosyasını PDF'e dönüştürür."""
    return md_to_pdf(dosya_yolu)


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        dosya = sys.argv[1]
        format = sys.argv[2] if len(sys.argv) > 2 else 'html'
        
        if format.lower() == 'pdf':
            md_to_pdf(dosya)
        else:
            md_to_html(dosya)
    else:
        print("Kullanım: python markdown_converter.py dosya.md [html|pdf]")
