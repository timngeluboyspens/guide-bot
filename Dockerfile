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

# Jalankan file download_pandoc.py
RUN python download_pandoc.py

# Berikan permission untuk eksekusi script
RUN chmod +x /app/install_packages.sh

# Jalankan shell script untuk menginstall sistem packages
RUN /app/install_packages.sh

# Berikan permission untuk eksekusi script yang menjalankan aplikasi
RUN chmod +x /app/start.sh

# Eksekusi skrip yang menjalankan Flask dan Telegram bot
CMD ["/app/start.sh"]