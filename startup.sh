#!/bin/bash

python scripts/generate_embeddings.py

uvicorn app.main:app --host 0.0.0.0 --port $PORT