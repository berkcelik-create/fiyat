import streamlit as st
import urllib.parse

# Sayfa Ayarları
st.set_page_config(
    page_title="G-ENGINE", 
    page_icon="🔍", 
    layout="centered"
)

st.title("🔍 G-ENGINE")
st.write("---")

# 1. Hızlı Erişim Butonları
col1, col2, col3, col4 = st.columns(4)
if col1.button("Logitech"): st.session_state.girdi = "Logitech"
if col2.button("Razer"): st.session_state.girdi = "Razer"
if col3.button("SteelSeries"): st.session_state.girdi = "SteelSeries"
if col4.button("Ekran Kartı"): st.session_state.girdi = "Ekran Kartı"

# 2. Arama Kutusu
val = st.session_state.get("girdi", "")
girdi_alani = st.text_input("Ürün Modelini Girin:", value=val)

if st.button("Motoru Çalıştır", type="primary"):
    if girdi_alani:
        safe_search = urllib.parse.quote(girdi_alani.lower())
        
        # Mağazalar
        magazalar = [
            ("Wraith Esports", f"https://wraithesports.com/search?q={safe_search}"),
            ("İncehesap", f"https://www.incehesap.com/arama/?s={safe_search}"),
            ("İtopya", f"https://www.itopya.com/Arama?q={safe_search}"),
            ("Sinerji", f"https://www.sinerji.gen.tr/arama?q={safe_search}"),
            ("Trendyol", f"https://www.trendyol.com/sr?q={safe_search}"),
            ("Hepsiburada", f"https://www.hepsiburada.com/ara?q={safe_search}"),
            ("Amazon TR", f"https://www.amazon.com.tr/s?k={safe_search}"),
            ("Akakçe", f"https://www.akakce.com/arama/?q={safe_search}")
        ]
        
        # 3. Sonuçlar
        for ad, url in magazalar:
            st.link_button(ad, url, use_container_width=True)
    else:
        st.warning("Lütfen bir ürün ismi girin.")
