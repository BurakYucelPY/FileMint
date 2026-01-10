# FileMint Production Dockerfile
# Python 3.11 slim image - üretim için optimize edilmiş

FROM python:3.11-slim

# Ortam değişkenleri
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Çalışma dizini
WORKDIR /app

# pdf2docx ve weasyprint için gerekli sistem bağımlılıkları
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libcairo2 \
    libgdk-pixbuf-2.0-0 \
    libffi-dev \
    shared-mime-info \
    && rm -rf /var/lib/apt/lists/*

# Python bağımlılıklarını kopyala ve yükle
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Uygulama dosyalarını kopyala
COPY . .

# Çalışma dizinini web klasörüne ayarla
WORKDIR /app/web

# Render.com PORT ortam değişkenini dinle (varsayılan 10000)
EXPOSE 10000

# Gunicorn ile uygulamayı başlat
# - workers: CPU sayısına göre ayarlanır, Render free tier için 2 yeterli
# - bind: 0.0.0.0:$PORT ile tüm arayüzleri dinler
# - timeout: uzun süren dönüşümler için 120 saniye
CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:${PORT:-10000} --workers 2 --timeout 120 app:app"]
