from openai import OpenAI
from sentence_transformers import SentenceTransformer
import chromadb

# ----------------------------
# INITIALIZATION
# ----------------------------

client = OpenAI(
    api_key="YOUR_API_KEY"
)

embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

chroma_client = chromadb.PersistentClient(
    path="./vector_db"
)

collection = chroma_client.get_collection(
    "course_materials"
)

# ----------------------------
# RETRIEVAL
# ----------------------------

def retrieve_context(question, top_k=5):

    query_embedding = embedding_model.encode(
        question
    ).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    documents = results["documents"][0]

    context = "\n\n".join(documents)

    return context


# ----------------------------
# PROMPT CONSTRUCTION
# ----------------------------

def build_prompt(question, context):

    prompt = f"""
You are an intelligent course assistant.

Use ONLY the provided course material.

Course Material:
{context}

Student Question:
{question}

Provide:
1. Clear explanation
2. Examples if available
3. Simple language

Answer:
"""

    return prompt


# ----------------------------
# LLM GENERATION
# ----------------------------

def generate_answer(question):

    context = retrieve_context(question)

    prompt = build_prompt(
        question,
        context
    )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3
    )

    return response.choices[0].message.content


# ----------------------------
# MAIN LOOP
# ----------------------------

while True:

    question = input("\nAsk a question: ")

    if question.lower() == "exit":
        break

    answer = generate_answer(question)

    print("\nAnswer:")
    print(answer)