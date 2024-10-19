# Gunakan unstructured Docker image sebagai base image
FROM downloads.unstructured.io/unstructured-io/unstructured:latest

# Setel direktori kerja di dalam container
WORKDIR /app

# Copy seluruh kode aplikasi ke dalam container
COPY . .

# Install dependencies dari linux-requirements.txt
RUN pip install --no-cache-dir -r linux-requirements.txt

# Berikan permission untuk eksekusi script
RUN chmod +x /app/install_packages.sh

# Jalankan shell script untuk menginstall sistem packages
RUN /app/install_packages.sh

# Berikan permission untuk eksekusi script yang menjalankan aplikasi
RUN chmod +x /app/start.sh

# Eksekusi skrip yang menjalankan Flask dan Telegram bot
CMD ["/app/start.sh"]
