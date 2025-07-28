FROM python:3.10-slim

WORKDIR /app
COPY . .

# Install dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc python3-dev wget && \
    pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    apt-get remove -y gcc python3-dev wget && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/*

# Entrypoint for full pipeline (outline extraction + semantic analysis)
ENTRYPOINT ["python", "main.py"]
