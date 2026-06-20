conversation_history = []

def generate_answer(question):

    context = retrieve_context(question)

    history_text = "\n".join(
        conversation_history[-5:]
    )

    prompt = f"""
Previous Conversation:
{history_text}

Relevant Course Material:
{context}

Question:
{question}

Answer:
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    answer = response.choices[0].message.content

    conversation_history.append(
        f"Q: {question}"
    )

    conversation_history.append(
        f"A: {answer}"
    )

    return answer