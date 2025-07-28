import os
import subprocess
import sys

def run_outline_extraction():
    # Run outline.py to generate test/*.json from pdfs/
    outline_script = os.path.join("src", "outline.py")
    print("[INFO] Extracting outlines from PDFs...")
    result = subprocess.run([sys.executable, outline_script], check=True)
    print("[INFO] Outline extraction complete.")

def run_semantic_analysis(persona, job, output="output.json"):
    # Run semantic_analyzer.py on test/*.json
    semantic_script = os.path.join("src", "semantic_analyzer.py")
    test_folder = "test"
    print("[INFO] Running semantic analysis...")
    result = subprocess.run([
        sys.executable, semantic_script,
        "--json_folder", test_folder,
        "--persona", persona,
        "--job", job,
        "--output", output
    ], check=True)
    print(f"[INFO] Semantic analysis complete. Output written to {output}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--persona", required=True, help="Persona description")
    parser.add_argument("--job", required=True, help="Job to be done")
    parser.add_argument("--output", default="output.json", help="Output JSON file")
    args = parser.parse_args()

    run_outline_extraction()
    run_semantic_analysis(args.persona, args.job, args.output)
