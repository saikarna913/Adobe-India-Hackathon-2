from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from .preprocessor import DocumentPreprocessor
import numpy as np

class SemanticAnalyzer:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.preprocessor = DocumentPreprocessor()
    
    def calculate_relevance(self, query, chunks):
        query_embedding = self.model.encode(query)
        chunk_texts = [chunk['text'] for chunk in chunks]
        chunk_embeddings = self.model.encode(chunk_texts)
        
        similarities = cosine_similarity(
            [query_embedding],
            chunk_embeddings
        )[0]
        
        for i, chunk in enumerate(chunks):
            chunk['relevance_score'] = float(similarities[i])
        
        return sorted(chunks, key=lambda x: -x['relevance_score'])
    
    def analyze_documents(self, persona, job, document_json):
        chunks = self.preprocessor.process(document_json)
        query = f"Persona: {persona}. Job: {job}"
        scored_chunks = self.calculate_relevance(query, chunks)
        relevant_chunks = [c for c in scored_chunks if c['relevance_score'] > 0.3]
        
        return {
            "metadata": {
                "persona": persona,
                "job": job,
                "documents": list(set([c['doc_title'] for c in relevant_chunks])),
                "analysis_method": "embedding_semantic_similarity"
            },
            "results": [{
                "text": chunk['text'],
                "page": chunk['page'],
                "score": chunk['relevance_score'],
                "document": chunk['doc_title']
            } for chunk in relevant_chunks[:10]]  # Top 10 results
        }