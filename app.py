import streamlit as st
import urllib.parse
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
st.metric("USD/TRY", f"{dolar} ₺")
st.write("---")

# 1. Trendler
st.subheader("🚀 Hızlı Erişim")
c1, c2 = st.columns(2)
c1.link_button("Donanım Fırsatları", "https://www.akakce.com/bilgisayar-bilesenleri.html", use_container_width=True)
c2.link_button("Teknik Spesifikasyonlar", "https://www.techpowerup.com/gpu-specs/", use_container_width=True)

st.write("---")

# 2. Karşılaştırma Matrisi (Yenilendi)
st.subheader("⚖️ Profesyonel Karşılaştırma")
st.caption("İki modeli yazın, doğrudan karşılaştırma sayfasına gidin.")
m1, m2 = st.columns(2)
model_a = m1.text_input("1. Model (Örn: RTX 5070)")
model_b = m2.text_input("2. Model (Örn: RTX 4070 Ti)")

if st.button("Hızlı Karşılaştır", type="primary", use_container_width=True):
    if model_a and model_b:
        # TechPowerUp GPU Karşılaştırma Linki (En doğru sonucu verir)
        tpu_link = f"https://www.techpowerup.com/gpu-specs/?mfgr=&prepend=&q={model_a}+vs+{model_b}"
        # Akakçe Fiyat Karşılaştırma Linki
        akakce_link = f"https://www.akakce.com/karsilastir/?q={model_a}+{model_b}"
        
        st.link_button("Teknik Verileri Karşılaştır (TechPowerUp)", tpu_link, use_container_width=True)
        st.link_button("Fiyatları Karşılaştır (Akakçe)", akakce_link, use_container_width=True)
    else:
        st.warning("Lütfen karşılaştırmak için iki model ismi de girin.")

st.write("---")

# 3. Mağaza Arama (Önceki başarılı mantık)
st.subheader("🛒 Mağaza Arama")
girdi = st.text_input("Arama:", placeholder="Model ismi girin...")
if st.button("Mağazalarda Ara"):
    if girdi:
        normal = urllib.parse.quote(girdi)
        st.link_button("İtopya'da Ara", f"https://www.itopya.com/ara?bul={normal}", use_container_width=True)
        st.link_button("İncehesap'ta Ara", f"https://www.incehesap.com/arama/?s={normal.replace(' ', '%20')}", use_container_width=True)
        st.link_button("Akakçe'de Ara", f"https://www.akakce.com/arama/?q={normal}", use_container_width=True)
