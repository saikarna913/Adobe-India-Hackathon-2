# Approach Explanation

## Overview
This system is designed to act as an intelligent document analyst, extracting and prioritizing the most relevant sections from a collection of documents based on a specific persona and their job-to-be-done. The solution is generic and can handle diverse document types, personas, and tasks.

## Methodology
1. **Document Parsing**: The system accepts 3-10 PDF documents. Each document is parsed to extract its outline, including titles and subheadings, along with their page numbers.
2. **Metadata Extraction**: The input includes the document collection, persona definition (role and expertise), and a concrete job-to-be-done. These are stored as metadata for traceability and reproducibility.
3. **Semantic Embedding**: For each outline element (title/subheading), as well as the persona and job description, semantic embeddings are generated using a compact transformer-based model (e.g., MiniLM or DistilBERT) that fits within the 1GB model size constraint and runs efficiently on CPU.
4. **Cosine Similarity Analysis**: The system computes cosine similarity between each outline element and the persona/job description embeddings. This quantifies relevance.
5. **Section Prioritization**: Sections are ranked by similarity scores. The most relevant sections are selected and assigned an importance rank.
6. **Sub-section Analysis**: For each selected section, the system refines the text, checks page number constraints, and outputs the most relevant sub-sections.
7. **Output Generation**: The final output includes metadata, extracted sections (with document, page number, section title, and importance rank), and sub-section analysis (with refined text and page constraints).

## Constraints & Optimization
- **Model Selection**: Only models ≤1GB are used (e.g., sentence-transformers/all-MiniLM-L6-v2 or distilbert-base-uncased), ensuring CPU-only inference and fast processing.
- **No Internet Access**: All models and dependencies are pre-installed in the Docker image; no downloads at runtime.
- **Performance**: The pipeline is optimized to process 3-5 documents in ≤60 seconds on CPU.

## Execution
- The system is containerized using Docker. All dependencies are installed offline.
- Execution instructions are provided in the README and Dockerfile.

## Extensibility
- The approach is domain-agnostic and can be extended to other document types, personas, and tasks.

---

This methodology ensures robust, efficient, and interpretable document analysis tailored to user-defined personas and tasks.
