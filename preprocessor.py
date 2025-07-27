class DocumentPreprocessor:
    def process(self, document_json):
        chunks = []
        for section in document_json['outline']:
            chunks.append({
                'text': self._clean_text(section['text']),
                'page': section['page'],
                'doc_title': document_json['title']
            })
        return chunks
    
    def _clean_text(self, text):
        return text.replace('\u2013', '-').strip()