import os
import json
from dotenv import load_dotenv
from openai import OpenAI




client = OpenAI(api_key="apı key gir.")

# ---------------------------------------------------------
# 1. PYTHON FONKSİYONLARI (Tek Berfin Kaydı)
# ---------------------------------------------------------

def kitap_veya_film_oner(kategori: str) -> str:
    """Belirtilen kategoriye göre öneri döner."""
    veri = {
        "bilimkurgu": "Film: Interstellar (2014) - Kitap: Mülksüzler (Ursula K. Le Guin)",
        "yazilim": "Kitap: Pragmatic Programmer - Film: The Social Network",
        "psikoloji": "Kitap: İnsanın Anlam Arayışı (Viktor Frankl)"
    }
    kat_clean = kategori.lower().strip()
    return veri.get(kat_clean, f"{kategori} kategorisinde popüler bir içerik: Matrix (Film)")

def kullanici_profil_getir(kullanici_adi: str) -> str:
    """Sistemde kayıtlı kullanıcının bilgilerini döner."""
    profiller = {
        "rumeysamac": "Kullanıcı: Rümeysa | Rol: Yapay Zeka Operatörü | Aktif Proje: PyTorch & RAG Chatbot",
        "esraarataş": "Kullanıcı: Esra | Rol: Arka Yüz Geliştirici | Aktif Proje: Streamlit UI",
        "berfintoprak": "Kullanıcı: Berfin | Rol: Bilgisayar programcılığı | Aktif Proje: Otomasyon pipeline geliştirme"
    }
    user_clean = kullanici_adi.lower().strip()
    return profiller.get(user_clean, "Kullanıcı bulunamadı.")

def skincare_icerik_analiz(icerik_adi: str) -> str:
    """Cilt bakımındaki aktif maddelerin ne işe yaradığını döner."""
    icerikler = {
        "niacinamide": "Niacinamide (B3 Vitamini): Gözenekleri sıkılaştırır, cilt tonunu eşitler ve leke karşıtıdır.",
        "salisilik asit": "Salisilik Asit (BHA): Yağda çözünür, tıkalı gözenekleri ve siyah noktaları temizler.",
        "hyaluronik asit": "Hyaluronik Asit: Cilde yoğun nem sağlar, dolgunlaştırır."
    }
    icerik_clean = icerik_adi.lower().strip()
    return icerikler.get(icerik_clean, f"{icerik_adi}: Genel nemlendirici veya yatıştırıcı içerik.")

# ---------------------------------------------------------
# 2. TOOL TANIMLARI (JSON Schema)
# ---------------------------------------------------------

tools = [
    {
        "type": "function",
        "function": {
            "name": "kitap_veya_film_oner",
            "description": "Kullanıcıya belirli bir kategoride (bilimkurgu, yazılım, psikoloji vb.) kitap veya film önerisi sunar.",
            "parameters": {
                "type": "object",
                "properties": {
                    "kategori": {"type": "string", "description": "Öneri istenen kategori adı"}
                },
                "required": ["kategori"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "kullanici_profil_getir",
            "description": "Sistemde kayıtlı kullanıcıların profil bilgilerini getirir. Sistemdeki kullanıcı adları: rumeysamac, esraarataş, berfintoprak. Kullanıcı sadece isim söylese bile (örn: 'Berfin' veya 'Esra') bunu uygun kullanıcı adına (örn: 'berfintoprak', 'esraarataş') dönüştürerek çağır.", 
            "parameters": {
                "type": "object",
                "properties": {
                    "kullanici_adi": {
                        "type": "string", 
                        "description": "Sorgulanacak tam kullanıcı adı: rumeysamac, esraarataş veya berfintoprak"
                    }
                },
                "required": ["kullanici_adi"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "skincare_icerik_analiz",
            "description": "Cilt bakımı ürünlerinde geçen aktif maddelerin ne işe yaradığını açıklar.",
            "parameters": {
                "type": "object",
                "properties": {
                    "icerik_adi": {"type": "string", "description": "Analiz edilecek içeriğin veya asidin adı"}
                },
                "required": ["icerik_adi"],
            },
        },
    }    
]

# ---------------------------------------------------------
# 3. MANUEL ÇAĞRI TESTİ
# ---------------------------------------------------------

soru = "Berfin kullanıcısının profil bilgilerini getir ve bana bilimkurgu kategorisinde bir öneri yap."

messages = [{"role": "user", "content": soru}]
print(f"Kullanıcı Sorusu: {soru}\n")

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages,
    tools=tools,
    temperature=0.0
)

assistant_msg = response.choices[0].message

if assistant_msg.tool_calls:
    print(">>> Model Araç Çağırma Kararı Aldı!")
    messages.append(assistant_msg)

    for tool_call in assistant_msg.tool_calls:
        fn_name = tool_call.function.name
        fn_args = json.loads(tool_call.function.arguments)
        print(f"-> Çalıştırılacak Araç: {fn_name}({fn_args})")

        if fn_name == "kitap_veya_film_oner":
            sonuc = kitap_veya_film_oner(**fn_args)
        elif fn_name == "kullanici_profil_getir":
            sonuc = kullanici_profil_getir(**fn_args)
        elif fn_name == "skincare_icerik_analiz":
            sonuc = skincare_icerik_analiz(**fn_args)
        else:
            sonuc = "Fonksiyon bulunamadı."

        print(f"   [Araç Çıktısı]: {sonuc}")

        messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": sonuc,
        })

    final_response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        tools=tools
    )

    print("\n--- NİHAİ MODEL CEVABI ---")
    print(final_response.choices[0].message.content)