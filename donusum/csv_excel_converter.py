"""
CSV ↔ Excel Dönüştürücü Modülü
CSV ve Excel dosyaları arasında çift yönlü dönüşüm yapar.
"""

import os
import csv
import pandas as pd


def csv_to_excel(dosya_yolu):
    """CSV dosyasını Excel formatına dönüştürür."""
    try:
        if not dosya_yolu.lower().endswith('.csv') or not os.path.exists(dosya_yolu):
            return False
        
        encodings = ['utf-8', 'latin-1', 'iso-8859-9', 'cp1254']
        df = None
        
        # Otomatik delimiter tespiti
        delimiter = ','
        try:
            with open(dosya_yolu, 'r', encoding='utf-8') as f:
                sample = f.read(4096)
                sniffer = csv.Sniffer()
                dialect = sniffer.sniff(sample, delimiters=',;\t|')
                delimiter = dialect.delimiter
        except:
            delimiter = ','
        
        for encoding in encodings:
            try:
                df = pd.read_csv(dosya_yolu, encoding=encoding, sep=delimiter)
                break
            except UnicodeDecodeError:
                continue
        
        if df is None:
            return False
        
        dizin = os.path.dirname(dosya_yolu)
        dosya_adi = os.path.splitext(os.path.basename(dosya_yolu))[0]
        cikti_yolu = os.path.join(dizin, f"{dosya_adi}.xlsx") if dizin else f"{dosya_adi}.xlsx"
        
        df.to_excel(cikti_yolu, index=False, engine='openpyxl')
        return True
        
    except Exception:
        return False


def excel_to_csv(dosya_yolu):
    """Excel dosyasını CSV formatına dönüştürür."""
    try:
        if not dosya_yolu.lower().endswith(('.xlsx', '.xls')) or not os.path.exists(dosya_yolu):
            return False
        
        if dosya_yolu.lower().endswith('.xlsx'):
            df = pd.read_excel(dosya_yolu, engine='openpyxl')
        else:
            df = pd.read_excel(dosya_yolu, engine='xlrd')
        
        dizin = os.path.dirname(dosya_yolu)
        dosya_adi = os.path.splitext(os.path.basename(dosya_yolu))[0]
        cikti_yolu = os.path.join(dizin, f"{dosya_adi}.csv") if dizin else f"{dosya_adi}.csv"
        
        df.to_csv(cikti_yolu, index=False, encoding='utf-8')
        return True
        
    except Exception:
        return False


def cevir(dosya_yolu):
    """Dosya uzantısına göre otomatik dönüşüm yapar."""
    uzanti = os.path.splitext(dosya_yolu)[1].lower()
    
    if uzanti == '.csv':
        return csv_to_excel(dosya_yolu)
    elif uzanti in ['.xlsx', '.xls']:
        return excel_to_csv(dosya_yolu)
    return False


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        cevir(sys.argv[1])
    else:
        print("Kullanım: python csv_excel_converter.py dosya.csv")
        print("         python csv_excel_converter.py dosya.xlsx")
