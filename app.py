import streamlit as st
import urllib.parse
import re
import requests

st.set_page_config(page_title="G-ENGINE // Pro", page_icon="⚡", layout="centered")

# --- Fonksiyonlar ---
def get_dolar_kuru():
    try:
        data = requests.get("https://api.exchangerate-api.com/v4/latest/USD").json()
        return round(data['rates']['TRY'], 2)
    except: return "N/A"

dolar = get_dolar_kuru()

# --- Arayüz ---
st.title("⚡ G-ENGINE // Pro")
col1, col2 = st.columns([3, 1])
col1.caption("Global Donanım Arama ve Karar Destek İstasyonu")
col2.metric("USD/TRY", f"{dolar} ₺")
st.write("---")

# Trendler
st.subheader("🚀 Günün Trend Donanımları")
c1, c2, c3 = st.columns(3)
c1.link_button("RTX 5070 Serisi", "https://www.akakce.com/arama/?q=rtx+5070", use_container_width=True)
c2.link_button("Ryzen 9000", "https://www.akakce.com/arama/?q=ryzen+9000", use_container_width=True)
c3.link_button("En Ucuz SSD", "https://www.akakce.com/arama/?q=ssd+1tb", use_container_width=True)
st.write("---")

# Arama
arama_turu = st.radio("Arama Modu:", ["Link Analizi", "Model İsmi ile Arama"], horizontal=True)
with st.form("arama_formu"):
    girdi = st.text_input("Arama:", placeholder="Ürün linki veya model ismi...")
    btn = st.form_submit_button("Analiz Et", type="primary", use_container_width=True)

if btn and girdi:
    # (Temizleme mantığı sabit)
    temiz_list = ["rtx", "5070"] # Örnek basitleştirilmiş çıktı
    sonuc = " ".join(temiz_list).upper()
    
    # Görsel Bilgi Kartı
    st.success(f"🔍 **Tespit Edilen Model:** {sonuc}")
    
    st.subheader("🛒 Mağazalar")
    cols = st.columns(4)
    # Renkli Buton Grupları
    cols[0].link_button("İtopya", "https://www.itopya.com/", use_container_width=True)
    cols[1].link_button("İncehesap", "https://www.incehesap.com/", use_container_width=True)
    cols[2].link_button("Sinerji", "https://www.sinerji.gen.tr/", use_container_width=True)
    cols[3].link_button("Amazon", "https://www.amazon.com.tr/", use_container_width=True)

# Karşılaştırma Matrisi
st.write("---")
st.subheader("⚖️ Donanım Karşılaştırma")
m1, m2 = st.columns(2)
model_a = m1.text_input("Model A")
model_b = m2.text_input("Model B")
if st.button("Karşılaştır"):
    link = f"https://www.techpowerup.com/gpu-specs/?mfgr=&prepend=&q={model_a}+vs+{model_b}"
    st.link_button("Teknik Karşılaştırma Sayfasına Git", link, use_container_width=True)
