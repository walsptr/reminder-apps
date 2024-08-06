# Gunakan base image resmi Python
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Buat direktori untuk aplikasi
WORKDIR /app

# Salin file requirements.txt ke dalam image
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Salin semua file aplikasi ke dalam image
COPY . /app/

# Set environment variable untuk Flask
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Jalankan perintah untuk memulai aplikasi Flask
CMD ["flask", "run"]

