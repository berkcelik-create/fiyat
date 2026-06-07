import streamlit as st
import urllib.parse
import re

st.set_page_config(page_title="G-ENGINE // Pro", page_icon="⚡", layout="centered")

st.title("⚡ G-ENGINE // Pro")
st.caption("Donanım Arama & Karşılaştırma İstasyonu")
st.write("---")

# 1. Arama Bölümü
with st.form("arama_formu"):
    girdi = st.text_input("Model ismi girin:", placeholder="Örn: RTX 5070")
    arama = st.form_submit_button("Analiz Et", type="primary", use_container_width=True)

if arama and girdi:
    temiz = urllib.parse.quote(girdi)
    st.success(f"Analiz edilen: {girdi.upper()}")
    
    # 2. Teknik Özellik ve Karşılaştırma Alanı (Pro Özellik)
    st.subheader("🔍 Teknik Hızlı Erişim")
    col1, col2 = st.columns(2)
    col1.link_button("Teknik Detaylar", f"https://www.techpowerup.com/gpu-specs/?q={temiz}", use_container_width=True)
    col2.link_button("FPS Karşılaştırma", f"https://www.youtube.com/results?search_query={temiz}+fps+benchmark", use_container_width=True)
    
    # 3. Mağaza Listesi
    st.subheader("🛒 Mağaza Arama")
    magazalar = [
        ("İtopya", f"https://www.itopya.com/ara?bul={temiz}"),
        ("İncehesap", f"https://www.incehesap.com/arama/?s={temiz.replace('+', '%20')}"),
        ("Sinerji", f"https://www.sinerji.gen.tr/arama?q={temiz}"),
        ("Akakçe", f"https://www.akakce.com/arama/?q={temiz}")
    ]
    for ad, url in magazalar:
        st.link_button(ad, url, use_container_width=True)

# 4. Profesyonel Karşılaştırma Matrisi
st.write("---")
st.subheader("⚖️ İkili Karşılaştırma Matrisi")
m1, m2 = st.columns(2)
a = m1.text_input("Model 1")
b = m2.text_input("Model 2")
if st.button("Performans Farkını Göster"):
    st.link_button("Karşılaştırmayı Başlat", f"https://versus.com/tr/{a}-vs-{b}", use_container_width=True)
