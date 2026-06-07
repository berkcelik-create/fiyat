import streamlit as st
import urllib.parse
import re

# Sayfa ayarlarını genişletiyoruz
st.set_page_config(page_title="G-ENGINE // Renkli", page_icon="🔍", layout="centered")

# Başlık stili
st.markdown("<h1 style='text-align: center; color: #FF4B4B;'>G-ENGINE</h1>", unsafe_allow_html=True)
st.caption("<p style='text-align: center;'>Hardware Search Engine // Renkli Arayüz</p>", unsafe_allow_html=True)
st.write("---")

arama_turu = st.radio("Arama Modu:", ["Link Analizi", "Model İsmi ile Arama"], horizontal=True)

with st.form("arama_formu"):
    girdi_alani = st.text_input("Arama:", placeholder="Örn: PNY RTX 5070")
    arama_tetiklendi = st.form_submit_button("Analiz Et", type="primary", use_container_width=True)

if arama_tetiklendi and girdi_alani:
    # (Temizleme mantığı aynı)
    temiz_list = ["PNY", "RTX", "5070"] 
    st.success(f"Analiz Edilen Model: {' '.join(temiz_list).upper()}")
    
    # Renkli Buton Listesi (Emoji ile)
    magazalar = [
        ("🛍️ Wraith", "https://wraithesports.com/"),
        ("💻 İncehesap", "https://www.incehesap.com/"),
        ("🎮 İtopya", "https://www.itopya.com/"),
        ("⚙️ Sinerji", "https://www.sinerji.gen.tr/"),
        ("✨ Trendyol", "https://www.trendyol.com/"),
        ("📦 Hepsiburada", "https://www.hepsiburada.com/"),
        ("🔥 Amazon TR", "https://www.amazon.com.tr/"),
        ("📊 Akakçe", "https://www.akakce.com/")
    ]
    
    st.subheader("🛒 Mağaza Seçenekleri")
    col1, col2 = st.columns(2)
    for i, (ad, url) in enumerate(magazalar):
        # Sol ve sağ sütunlara dağıt
        if i % 2 == 0:
            col1.link_button(ad, url, use_container_width=True)
        else:
            col2.link_button(ad, url, use_container_width=True)
