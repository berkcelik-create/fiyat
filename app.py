import streamlit as st
import urllib.parse
import re

# Sayfa Ayarları ve Sekme Emojisi
st.set_page_config(
    page_title="G-ENGINE // Hardware Search Engine", 
    page_icon="🔍", 
    layout="centered"
)

# Arama Motoru Başlık Düzeni
st.title("🔍 G-ENGINE")
st.caption("Hardware Search Engine // Global Donanım Arama ve Doğrulama Motoru")
st.write("---")

# Üçüncü bir mod olarak Yapay Zeka Modu eklendi
arama_turu = st.radio(
    "Arama Modu:", 
    ["🔗 Link Analizi", "⌨️ Model İsmi ile Arama", "🤖 AI Açıklama ile Arama"], 
    horizontal=True
)

# Form Yapısı
with st.form("arama_formu"):
    if arama_turu == "🔗 Link Analizi":
        girdi_alani = st.text_input("Ürün Linkini Girin:", placeholder="https://www.itopya.com/...")
    elif arama_turu == "⌨️ Model İsmi ile Arama":
        girdi_alani = st.text_input("Ürün Modelini Girin:", placeholder="Örn: AMD Ryzen 7 7800X3D")
    else:
        girdi_alani = st.text_input("Aradığınız Ekipmanı Tarif Edin:", placeholder="Örn: siyah hafif kablosuz oyuncu mouse rgb")
    
    arama_tetiklendi = st.form_submit_button("🔍 Motoru Çalıştır", type="primary", use_container_width=True)

# Gelişmiş Kelime Temizleme Fonksiyonu
def gelişmiş_kelime_temizle(url):
    try:
        if not url.startswith("http://") and not url.startswith("https://") and "." not in url:
            return None
        url_temiz = url.split("?")[0].split("#")[0]
        parcalar = url_temiz.split("/")[-1].split("-")
        yasakli = {"html", "urun", "p", "detay", "fiyat", "ozellikleri", "satinal", "gaming", "oyuncu", "store", "product", "com", "tr"}
        temiz = [k.replace(".html", "") for k in parcalar if len(k) > 2 and not k.isdigit() and k.lower() not in yasakli]
        if temiz:
            ham_sonuc = " ".join(temiz[:4])
            temiz_sonuc = re.sub(r'[^a-zA-Z0-9\s]', '', ham_sonuc)
            return temiz_sonuc.strip()
        return "Oyuncu Ekipmanı"
    except:
        return "Oyuncu Ekipmanı"

# Akıllı Boşluk Toleransı
def akilli_metin_duzelt(metin):
    metin = " ".join(metin.split())
    donusum = {"İ": "I", "ı": "i", "Ş": "S", "ş": "s", "Ç": "C", "ç": "c", "Ğ": "G", "ğ": "g", "Ü": "U", "ü": "u", "Ö": "O", "ö": "o"}
    for kaynak, placeholder in donusum.items():
        metin = metin.replace(kaynak, placeholder)
    return metin

# Arka Planda Çalışan Doğal Dil İşleme / AI Filtreleme Fonksiyonu
def ai_kelime_süzgeci(tarif):
    tarif = tarif.lower()
    gereksizler = [
        "bana", "bul", "getir", "ara", "arat", "tarzı", "gibi", "en", "iyi", "güzel", 
        "kaliteli", "ucuz", "fiyatlı", "bir", "tane", "istiyorum", "lazım", "olan", "ve", "veya"
    ]
    kelimeler = tarif.split()
    temiz_kelimeler = [k for k in kelimeler if k not in gereksizler]
    return " ".join(temiz_kelimeler[:4]) if temiz_kelimeler else "Oyuncu Ekipmanı"

# --- 🤖 YAPAY ZEKA ÖZELLİK ANALİZ MOTORU (Kural Tabanlı AI Alanı) ---
def ai_ozellik_yorumlama(tarif):
    tarif = tarif.lower()
    analiz_notlari = []
    
    if "mouse" in tarif or "fare" in tarif:
        analiz_notlari.append("🎯 **Ekipman Türü:** Oyuncu Mouse'u")
        if "hafif" in tarif:
            analiz_notlari.append("⚡ **AI Yorumu:** Hafif tasarımlar (flick atmak) ve FPS oyunlarında (Valorant, CS2) refleks hızını doğrudan artırır.")
        if "kablosuz" in tarif or "wireless" in tarif:
            analiz_notlari.append("📶 **AI Yorumu:** Kablosuz bağlantı masa üstündeki sürtünmeyi sıfırlayarak hareket özgürlüğü sağlar.")
            
    elif "klavye" in tarif or "keyboard" in tarif:
        analiz_notlari.append("⌨️ **Ekipman Türü:** Oyuncu Klavyesi")
        if "mekanik" in tarif:
            analiz_notlari.append("🕹️ **AI Yorumu:** Mekanik switchler daha düşük tepki süresi (ms) ve daha yüksek tuş ömrü sunar.")
            
    elif any(x in tarif for x in ["islemci", "cpu", "ekran karti", "gpu", "ram", "anakart"]):
