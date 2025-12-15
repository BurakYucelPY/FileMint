import subprocess

komut = [
    r"C:\Program Files\LibreOffice\program\soffice.exe", 
    '--headless',       
    '--convert-to', 'pdf', 
    'deneme.txt'        
]

print("Dönüştürme başladı")
subprocess.run(komut)
print("BİTTİ")