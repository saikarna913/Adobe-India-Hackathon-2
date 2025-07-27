from analyzer import SemanticAnalyzer
import json
import sys
from datetime import datetime

def load_input(input_path):
    with open(input_path) as f:
        return json.load(f)

def main():
    if len(sys.argv) != 4:
        print("Usage: python main.py <persona> <job> <document_json_path>")
        return
    
    persona = sys.argv[1]
    job = sys.argv[2]
    doc_path = sys.argv[3]
    
    document_json = load_input(doc_path)
    analyzer = SemanticAnalyzer()
    
    result = analyzer.analyze_documents(persona, job, document_json)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = f"output_{timestamp}.json"
    
    with open(output_path, 'w') as f:
        json.dump(result, f, indent=2)
    
    print(f"Analysis complete. Results saved to {output_path}")

if __name__ == "__main__":
    main()