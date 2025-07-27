# run.ps1
Write-Host "Setting up Python environment..."

# Create and activate virtual environment
python -m venv venv
.\venv\Scripts\activate

# Install requirements
pip install -r requirements.txt

# Run the analysis
python main.py `
    "PhD Researcher in Computational Biology" `
    "Prepare literature review on Graph Neural Networks" `
    "test/test_input.json"

Write-Host "Analysis complete!"