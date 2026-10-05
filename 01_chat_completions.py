from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()

print("--- 1. BÖLÜM: TEMEL CHAT COMPLETIONS ÇAĞRISI ---")
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "Sen kısa ve net cevaplar veren bir asistansın."},
        {"role": "user", "content": "Fotosentez nedir?"}
    ],
    temperature=0.3
)
print(response.choices[0].message.content)

print("\n--- ALIŞTIRMA 1: 3 TURLUK MANUEL KONUŞMA GEÇMİŞİ ---")
# API stateless olduğu için tüm geçmişi elle dizide saklıyoruz
messages = [
    {"role": "system", "content": "Sen samimi ve yardımsever bir asistansın."}
]

# 1. Tur
messages.append({"role": "user", "content": "Selam, ben Rümeysa. Yapay zeka üzerine çalışıyorum."})
res1 = client.chat.completions.create(model="gpt-4o-mini", messages=messages)
ans1 = res1.choices[0].message.content
messages.append({"role": "assistant", "content": ans1})
print(f"Kullanıcı: Selam, ben Rümeysa...")
print(f"Asistan: {ans1}\n")

# 2. Tur
messages.append({"role": "user", "content": "Şu an Python ile OpenAI API öğreniyorum."})
res2 = client.chat.completions.create(model="gpt-4o-mini", messages=messages)
ans2 = res2.choices[0].message.content
messages.append({"role": "assistant", "content": ans2})
print(f"Kullanıcı: Şu an Python ile OpenAI API öğreniyorum.")
print(f"Asistan: {ans2}\n")

# 3. Tur (Geçmişi hatırlama testi)
messages.append({"role": "user", "content": "Benim adım neydi ve hangi alanda çalışıyordum?"})
res3 = client.chat.completions.create(model="gpt-4o-mini", messages=messages)
print(f"Kullanıcı: Benim adım neydi...")
print(f"Asistan: {res3.choices[0].message.content}")

print("\n--- ALIŞTIRMA 3: TEMPERATURE MANTIĞI TESTİ ---")
# temperature=0 vs 1.5 karşılaştırması
temp_query = "Bana yaratıcı tek cümlelik bir uzay sloganı yaz."

print("Temperature = 0 (Tutarlı & Deterministik):")
for i in range(2):
    r = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": temp_query}],
        temperature=0.0
    )
    print(f"Deneme {i+1}: {r.choices[0].message.content}")

print("\nTemperature = 1.5 (Yaratıcı & Rastgele):")
for i in range(2):
    r = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": temp_query}],
        temperature=1.5
    )
    print(f"Deneme {i+1}: {r.choices[0].message.content}")