FROM python:3.9-slim

WORKDIR /app
COPY . .

# Create and activate venv, install requirements, pre-download model
RUN python -m venv /app/venv && \
    /app/venv/bin/pip install --upgrade pip && \
    /app/venv/bin/pip install --no-cache-dir -r requirements.txt && \
    /app/venv/bin/python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')" && \
    apt-get remove -y gcc python3-dev wget && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/*

# Entrypoint for semantic analysis (can be overridden)
ENTRYPOINT ["/app/venv/bin/python", "semantic_analyzer.py"]