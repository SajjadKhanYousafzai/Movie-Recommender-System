import json
import os

# Clean the notebook for better GitHub rendering
notebook_path = "movie_recommend_system.ipynb"

# Check file size
file_size = os.path.getsize(notebook_path) / (1024 * 1024)  # MB
print(f"Notebook size: {file_size:.2f} MB")

# Load and clean notebook
with open(notebook_path, 'r', encoding='utf-8') as f:
    notebook = json.load(f)

# Clean problematic characters and optimize outputs
cells_cleaned = 0
for cell in notebook.get('cells', []):
    # Clean source text
    if 'source' in cell and isinstance(cell['source'], list):
        cleaned_source = []
        for line in cell['source']:
            # Remove problematic Unicode surrogates
            clean_line = ''.join(c for c in line if ord(c) < 0xD800 or ord(c) > 0xDFFF)
            cleaned_source.append(clean_line)
        cell['source'] = cleaned_source
        cells_cleaned += 1
    
    # Limit large outputs that might break rendering
    if 'outputs' in cell:
        for output in cell['outputs']:
            if 'text' in output and isinstance(output['text'], list):
                if len(output['text']) > 1000:  # Limit very long outputs
                    output['text'] = output['text'][:500] + ['\\n... (output truncated for GitHub display) ...\\n']

print(f"Cleaned {cells_cleaned} cells")

# Save cleaned notebook
with open(notebook_path, 'w', encoding='utf-8') as f:
    json.dump(notebook, f, ensure_ascii=False, indent=1)

print("Notebook cleaned and optimized for GitHub!")
