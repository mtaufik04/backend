FROM python:3.11-slim

WORKDIR /app

# Install dependencies sistem yang dibutuhkan OpenCV
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements dan install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Jalankan uvicorn dengan port dinamis dari Render
CMD ["sh", "-c", "uvicorn app:app --host 0.0.0.0 --port $PORT"]
