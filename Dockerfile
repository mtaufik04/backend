FROM python:3.11-slim

WORKDIR /app

# Copy requirements dan install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy semua source code
COPY . .

# Gunakan sh -c agar $PORT dieksekusi
CMD ["sh", "-c", "uvicorn app:app --host 0.0.0.0 --port $PORT"]
