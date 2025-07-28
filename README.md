# Intelligent Document Analyst - Docker Setup

This project extracts and prioritizes the most relevant sections from a collection of documents based on a specific persona and job-to-be-done, using semantic embeddings and cosine similarity.

## Prerequisites

- [Docker](https://www.docker.com/products/docker-desktop) installed on your machine
- Place your PDF files in the `pdf/` directory

## Project Structure

```
.
├── Dockerfile
├── requirements.txt
├── main.py
├── src/
│   ├── outline.py
│   └── semantic_analyzer.py
├── pdfs/
│   └── (your PDF files)
└── test/
    └── (generated JSON outlines)
```
## Clone the repo
```sh
git clone https://github.com/saikarna913/Adobe-India-Hackathon-2.git
```

## Build the Docker Image

```sh
docker build -t intelligent-document-analyst .
```

## Run the Pipeline

Replace the **persona** and **job description** as needed.

```sh
docker run --rm -v "$PWD/pdf:/app/pdf" -v "$PWD/test:/app/test" -v "$PWD/output:/app/output" intelligent-document-analyst --persona "Travel Planner" --job "Plan a trip of 4 days for a group of 10 college friends." --output output/output.json
```

- This will:
  1. Extract outlines from all PDFs in `pdfs/` into `test/` as JSON files.
  2. Run semantic analysis on the outlines.
  3. Produce `output.json` in output folder with the results.

## Notes

- The model is pre-downloaded in the Docker image for offline use.
- All processing is CPU-only and fits within 1GB model size.
- No internet access is required at runtime.

## Troubleshooting

- Ensure your `pdfs/` folder contains valid PDF files.
- If you encounter JSON errors, check that the `test/` folder is cleared or contains only valid outline JSONs.

---

**For any issues, please open an issue in this repository.**
