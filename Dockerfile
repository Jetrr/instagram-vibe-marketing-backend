FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /app

COPY requirements.txt .

RUN python -m pip install "pip<24.1"
RUN pip install --no-cache-dir -r requirements.txt


COPY . .

ENV GOOGLE_APPLICATION_CREDENTIALS="/app/jetrr-ai-agent-5b34f6931fbf.json"

EXPOSE 8080

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]