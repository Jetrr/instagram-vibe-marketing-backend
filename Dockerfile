# syntax=docker/dockerfile:1

FROM python:3.11-slim

# Install system dependencies (for Pillow, cryptography, etc.)
RUN apt-get update && apt-get install -y \
    build-essential \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Create the working dir
WORKDIR /app

# Copy requirements first for build caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy your application files
COPY . .

# (Optional) expose port 80 for uvicorn
EXPOSE 80

# Default command:
# -host 0.0.0.0 (allow external access)
# -port 80
# --reload only in dev! Remove in prod!
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]