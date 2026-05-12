import json
import numpy as np
import faiss

from sentence_transformers import SentenceTransformer

# LOAD ENRICHED DATASET
with open(
    "data/processed/shl_catalog_enriched.json",
    "r",
    encoding="utf-8"
) as f:

    assessments = json.load(f)

print(f"\nTOTAL ASSESSMENTS: {len(assessments)}")

# LOAD EMBEDDING MODEL
model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)

documents = []

for assessment in assessments:

    text = f"""
    Assessment Name: {assessment['name']}

    Attributes:
    {' '.join(assessment['attributes'])}

    Content:
    {assessment['page_text']}
    """

    documents.append(text)

print("\nGENERATING EMBEDDINGS...")

embeddings = model.encode(
    documents,
    convert_to_numpy=True,
    show_progress_bar=True
)

print("\nEMBEDDINGS GENERATED")

# CREATE FAISS INDEX
dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(dimension)

index.add(embeddings)

print("\nFAISS INDEX CREATED")

# SAVE INDEX
faiss.write_index(
    index,
    "data/embeddings/shl_index.faiss"
)

# SAVE METADATA
with open(
    "data/embeddings/documents.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(assessments, f, indent=2)

print("\nINDEX + DOCUMENTS SAVED")