# Gunakan image dasar Python
FROM python:3.10-slim

# Setel direktori kerja di dalam container
WORKDIR /app

# Copy seluruh kode aplikasi ke dalam container
COPY . .

# Install dependencies dari linux-requirements.txt
RUN pip install --no-cache-dir -r linux-requirements.txt

# Install unstructured
RUN pip install "unstructured[all-docs]"

# Install pandoc
RUN dpkg -i /app/pandoc-3.5-1-amd64.deb

# Set path pandoc
ENV PATH="/usr/local/bin/pandoc:${PATH}"

# Install "poppler-utils" "libreoffice" "tesseract-ocr" "libtesseract-dev" "libmagic1" "libmagic-dev"
RUN apt-get update && apt-get install -y poppler-utils libreoffice tesseract-ocr libtesseract-dev libmagic1 libmagic-dev

# Berikan permission untuk eksekusi script yang menjalankan aplikasi
RUN chmod +x /app/start.sh

# Eksekusi skrip yang menjalankan Flask dan Telegram bot
CMD ["/app/start.sh"]