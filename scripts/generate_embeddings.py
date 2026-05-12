import os
import json
import faiss
import numpy as np

from sentence_transformers import SentenceTransformer
from tqdm import tqdm

# LOAD ASSESSMENT DATA

with open("data/processed/shl_catalog.json", "r", encoding="utf-8") as f:
    assessments = json.load(f)

print(f"\nTOTAL ASSESSMENTS: {len(assessments)}")

# LOAD EMBEDDING MODEL

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# PREPARE TEXTS

texts = []

for item in assessments:
    text = f"""
    Assessment Name: {item.get('name', '')}
    Attributes: {' '.join(item.get('attributes', []))}
    Description: {item.get('description', '')}
    Job Levels: {' '.join(item.get('job_levels', []))}
    Languages: {' '.join(item.get('languages', []))}
    """

    texts.append(text.strip())

# GENERATE EMBEDDINGS

print("\nGENERATING EMBEDDINGS...\n")

embeddings = model.encode(
    texts,
    batch_size=32,
    show_progress_bar=True,
    convert_to_numpy=True
)

print("\nEMBEDDINGS GENERATED")

# CREATE FAISS INDEX
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(np.array(embeddings).astype("float32"))
print("\nFAISS INDEX CREATED")

# CREATE DIRECTORY

os.makedirs("data/embeddings", exist_ok=True)

# SAVE INDEX

faiss.write_index(
    index,
    "data/embeddings/shl_index.faiss"
)

# SAVE DOCUMENTS

with open(
    "data/embeddings/documents.json",
    "w",
    encoding="utf-8"
) as f:
    json.dump(assessments, f, indent=2)

print("\nINDEX + DOCUMENTS SAVED")
