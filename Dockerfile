# Gunakan image dasar Python
FROM python:3.10-slim

# Setel direktori kerja di dalam container
WORKDIR /app

# Copy file requirements.txt ke dalam container
COPY requirements.txt requirements.txt

# Install dependencies dari requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy seluruh kode aplikasi ke dalam container
COPY . .

# Berikan permission untuk eksekusi script
RUN chmod +x /app/install_packages.sh

# Jalankan shell script untuk menginstall sistem packages
RUN /app/install_packages.sh

# Eksekusi aplikasi Flask dengan Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--log-level", "info", "wsgi:app"]
