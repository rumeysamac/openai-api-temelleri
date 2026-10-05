from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()

print("--- RESPONSES API İLE ÇAĞRI ---")
response = client.responses.create(
    model="gpt-4o-mini",
    input="Fotosentez nedir?"
)

# Responses API'de çıktı doğrudan output_text üzerinden alınır
print(response.output_text)