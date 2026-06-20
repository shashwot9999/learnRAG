relevant_docs = []

for doc, distance in zip(documents, distances):

    if distance < 0.7:
        relevant_docs.append(doc)

context = "\n".join(relevant_docs)