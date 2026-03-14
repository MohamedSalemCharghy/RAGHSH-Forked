import torch
from qdrant_client import QdrantClient
from qdrant_client.http import models
from fastembed import TextEmbedding

# Konfiguration
COLLECTION_NAME = "hsh_knowledge"
QUERY_TEXT = "Hanno Homann" 
# 1. Verbindung & Modell-Initialisierung (Explizit)
client = QdrantClient(host="localhost", port=6333)
# Wir nutzen exakt das Modell vom HPC
embedder = TextEmbedding(model_name="jinaai/jina-embeddings-v3")

def debug_manual():
    print(f"--- Suche nach: {QUERY_TEXT} ---")

    # --- TEIL 1: Vektor erzeugen ---
    # Wichtig: Task 'retrieval.query' für die Suche nutzen!
    print("Vektorisiere...")
    vector = list(embedder.embed([QUERY_TEXT], task="retrieval.query"))[0]

    # --- TEIL 2: Die Suche ---
    print("Suche in Qdrant...")
    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=vector.tolist(),
        limit=50,
        with_payload=True,
    ).points

    if not results:
        print("Keine Ergebnisse gefunden.")
    else:
        for i, res in enumerate(results):
            print(f"\n[{i+1}] Score: {res.score:.4f}")
            print(f"URL: {res.payload.get('source_url')}")
            print(f"Text: {res.payload.get('text')[:2000]}...")

if __name__ == "__main__":
    debug_manual()