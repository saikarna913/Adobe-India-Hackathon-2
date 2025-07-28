import os
import json
import glob
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from datetime import datetime

MODEL_NAME = "all-MiniLM-L6-v2"  # ~80MB, fits constraints

class DocumentSection:
    def __init__(self, document, page_num, title, text):
        self.document = document
        self.page_num = page_num
        self.title = title
        self.text = text
        self.importance_rank = None

class SubSectionAnalysis:
    def __init__(self, document, refined_text, page_num):
        self.document = document
        self.refined_text = refined_text
        self.page_num = page_num

class DocumentAnalyzer:
    def __init__(self, persona, job, json_folder):
        self.persona = persona
        self.job = job
        self.json_folder = json_folder
        self.model = SentenceTransformer(MODEL_NAME)
        self.sections = []
        self.sub_sections = []
        self.input_documents = []
        self.metadata = {
            "input_documents": [],
            "persona": persona,
            "job_to_be_done": job,
            "processing_timestamp": datetime.now().isoformat()
        }

    def extract_outline_from_json(self, json_path):
        with open(json_path, "r", encoding="utf-8") as f:
            doc = json.load(f)
        title = doc.get("title", os.path.basename(json_path))
        outlines = []
        for entry in doc.get("outline", []):
            outlines.append({
                "title": entry["text"],
                "page_num": entry["page"],
                "text": entry["text"]
            })
        return title, outlines

    def analyze(self):
        persona_job_text = f"{self.persona} {self.job}"
        persona_job_emb = self.model.encode([persona_job_text])[0]
        all_sections = []
        json_files = glob.glob(os.path.join(self.json_folder, "*.json"))
        self.input_documents = [os.path.basename(f) for f in json_files]
        self.metadata["input_documents"] = self.input_documents
        for json_path in json_files:
            doc_title, outlines = self.extract_outline_from_json(json_path)
            for outline in outlines:
                section_text = outline["title"]
                emb = self.model.encode([section_text])[0]
                score = cosine_similarity([emb], [persona_job_emb])[0][0]
                section = DocumentSection(
                    document=os.path.basename(json_path),
                    page_num=outline["page_num"],
                    title=outline["title"],
                    text=outline["text"]
                )
                section.importance_rank = score
                all_sections.append(section)
        # Sort and select top N
        all_sections.sort(key=lambda x: x.importance_rank, reverse=True)
        self.sections = all_sections[:10]  # Top 10 relevant sections
        # Sub-section analysis (refined text)
        for section in self.sections:
            refined_text = self.refine_text(section.text, persona_job_emb)
            self.sub_sections.append(SubSectionAnalysis(
                document=section.document,
                refined_text=refined_text,
                page_num=section.page_num
            ))

    def refine_text(self, text, persona_job_emb):
        # Split into sentences, rank by similarity
        sentences = [s.strip() for s in text.split(". ") if s.strip()]
        if not sentences:
            return ""
        sent_embs = self.model.encode(sentences)
        scores = cosine_similarity(sent_embs, [persona_job_emb]).flatten()
        top_idx = np.argmax(scores)
        return sentences[top_idx]

    def output_results(self, output_path):
        output = {
            "metadata": self.metadata,
            "extracted_sections": [
                {
                    "document": s.document,
                    "page_number": s.page_num,
                    "section_title": s.title,
                    "importance_rank": float(s.importance_rank)
                } for s in self.sections
            ],
            "sub_section_analysis": [
                {
                    "document": ss.document,
                    "refined_text": ss.refined_text,
                    "page_number": ss.page_num
                } for ss in self.sub_sections
            ]
        }
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(output, f, indent=2)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--json_folder", required=True, help="Folder containing outline JSON files")
    parser.add_argument("--persona", required=True, help="Persona description")
    parser.add_argument("--job", required=True, help="Job to be done")
    parser.add_argument("--output", default="output.json", help="Output file")
    args = parser.parse_args()
    analyzer = DocumentAnalyzer(args.persona, args.job, args.json_folder)
    analyzer.analyze()
    analyzer.output_results(args.output)
