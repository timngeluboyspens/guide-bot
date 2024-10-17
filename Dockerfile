# Gunakan image dasar Python
FROM python:3.10-slim

# Setel direktori kerja di dalam container
WORKDIR /app

# Copy seluruh kode aplikasi ke dalam container
COPY . .

# Install dependencies dari linux-requirements.txt
RUN pip install --no-cache-dir -r linux-requirements.txt

# Berikan permission untuk eksekusi script
RUN chmod +x /app/install_packages.sh

# Jalankan shell script untuk menginstall sistem packages
RUN ./app/install_packages.sh

# Eksekusi aplikasi Flask dengan Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--log-level", "info", "wsgi:app"]
