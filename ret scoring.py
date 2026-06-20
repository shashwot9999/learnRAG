results = collection.query(
    query_embeddings=[query_embedding],
    n_results=5
)

documents = results["documents"][0]
distances = results["distances"][0]

for doc, score in zip(documents, distances):
    print(score)