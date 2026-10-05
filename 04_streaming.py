from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()

print("--- STREAMING (CEVABI PARÇA PARÇA ALMA) ---")
stream = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Kısa bir hikaye anlat."}],
    stream=True
)

for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="", flush=True)

print() # Alt satıra geçiş