from groq import Groq
from app.config import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)

def generate_answer(prompt):
    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    return response.choices[0].message.content