from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel

load_dotenv()
client = OpenAI()

print("--- 1. ÖRNEK: ÜRÜN ÖZETİ (PDF ÖRNEĞİ) ---")
class UrunOzeti(BaseModel):
    urun_adi: str
    fiyat: float
    stokta_mi: bool

response = client.responses.parse(
    model="gpt-4o-mini",
    input="iPhone 15, 999 dolar, stokta mevcut.",
    text_format=UrunOzeti,
)

urun: UrunOzeti = response.output_parsed
print(f"Ürün Adı: {urun.urun_adi}")
print(f"Fiyat: {urun.fiyat}")
print(f"Stok Durumu: {urun.stokta_mi}\n")


print("--- ALIŞTIRMA 2: RESTORAN MENÜSÜ YEMEK DETAYI ---")
class YemekDetayi(BaseModel):
    isim: str
    fiyat: float
    vejetaryen_mi: bool
    kalori: int

menu_response = client.responses.parse(
    model="gpt-4o-mini",
    input="Mercimek Çorbası: 120 TL, tamamen bitkisel içerikli, porsiyonu yaklaşık 250 kalori.",
    text_format=YemekDetayi,
)

yemek: YemekDetayi = menu_response.output_parsed
print(f"Yemek İsim: {yemek.isim}")
print(f"Fiyat: {yemek.fiyat} TL")
print(f"Vejetaryen mi?: {yemek.vejetaryen_mi}")
print(f"Kalori: {yemek.kalori} kcal")