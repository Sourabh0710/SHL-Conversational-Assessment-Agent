import json
import faiss
import numpy as np

from rank_bm25 import BM25Okapi
from sentence_transformers import SentenceTransformer


# ---------------------------------
# QUERY EXPANSION
# ---------------------------------

def expand_query(query):

    query_lower = query.lower()

    expanded_terms = [query]

    if "python" in query_lower:

        expanded_terms.extend([
            "backend development",
            "software engineering",
            "programming",
            "API development",
            "database"
        ])

    if "java" in query_lower:

        expanded_terms.extend([
            "spring",
            "backend engineering",
            "enterprise application",
            "object oriented programming"
        ])

    if "leadership" in query_lower:

        expanded_terms.extend([
            "managerial",
            "people management",
            "executive",
            "team leadership"
        ])

    if "sales" in query_lower:

        expanded_terms.extend([
            "customer service",
            "communication",
            "business development"
        ])

    return " ".join(expanded_terms)


# ---------------------------------
# LOAD MODEL
# ---------------------------------

model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)

# ---------------------------------
# LOAD FAISS INDEX
# ---------------------------------

index = faiss.read_index(
    "data/embeddings/shl_index.faiss"
)

# ---------------------------------
# LOAD DOCUMENTS
# ---------------------------------

with open(
    "data/embeddings/documents.json",
    "r",
    encoding="utf-8"
) as f:

    documents = json.load(f)

# ---------------------------------
# BM25 CORPUS
# ---------------------------------

bm25_corpus = []

for doc in documents:

    text = f"""
    {doc['name']}
    {' '.join(doc['attributes'])}
    {doc.get('page_text', '')}
    """

    tokens = text.lower().split()

    bm25_corpus.append(tokens)

bm25 = BM25Okapi(bm25_corpus)


# ---------------------------------
# MAIN RETRIEVAL
# ---------------------------------

def retrieve_assessments(query, top_k=10):

    # QUERY EXPANSION
    query = expand_query(query)

    # ---------------------------------
    # FAISS SEARCH
    # ---------------------------------

    query_embedding = model.encode(
        [query],
        convert_to_numpy=True
    )

    distances, faiss_indices = index.search(
        query_embedding,
        top_k * 2
    )

    # ---------------------------------
    # BM25 SEARCH
    # ---------------------------------

    tokenized_query = query.lower().split()

    bm25_scores = bm25.get_scores(tokenized_query)

    bm25_indices = np.argsort(
        bm25_scores
    )[::-1][:top_k * 2]

    # ---------------------------------
    # HYBRID MERGING
    # ---------------------------------

    combined_scores = {}

    # FAISS RESULTS
    for rank, idx in enumerate(faiss_indices[0]):

        combined_scores[idx] = (
            combined_scores.get(idx, 0)
            + (top_k * 2 - rank)
        )

    # BM25 RESULTS
    for rank, idx in enumerate(bm25_indices):

        combined_scores[idx] = (
            combined_scores.get(idx, 0)
            + (top_k * 2 - rank)
        )

    # SORT RESULTS
    sorted_results = sorted(
        combined_scores.items(),
        key=lambda x: x[1],
        reverse=True
    )

    results = []

    for idx, score in sorted_results[:top_k]:

        assessment = documents[idx]

        results.append({
            "name": assessment["name"],
            "url": assessment["url"],
            "attributes": assessment["attributes"]
        })

    return results