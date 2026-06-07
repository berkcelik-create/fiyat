import streamlit as st
import urllib.parse

# Sayfa Ayarları
st.set_page_config(page_title="G-ENGINE", page_icon="🔍", layout="centered")

st.title("🔍 G-ENGINE")
st.write("---")

# 1. Hızlı Erişim Butonları
col1, col2, col3, col4 = st.columns(4)
if col1.button("Logitech"): st.session_state.girdi = "Logitech"
if col2.button("Razer"): st.session_state.girdi = "Razer"
if col3.button("SteelSeries"): st.session_state.girdi = "SteelSeries"
if col4.button("Ekran Kartı"): st.session_state.girdi = "Ekran Kartı"

# 2. Arama Kutusu
# session_state ile buton değerini kutuya aktarıyoruz
val = st.session_state.get("girdi", "")
girdi_alani = st.text_input("Ürün Modelini Girin:", value=val)

# 3. Arama Motoru Çalıştırma
if st.button("Motoru Çalıştır", type="primary"):
    if girdi_alani:
        # Linkleri güvenli formata çevir
        safe_search = urllib.parse.quote(girdi_alani.lower())
        
        # Mağaza Listesi
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
        
        # Sonuçları yan yana ikişerli butonlar halinde listele
        for i in range(0, len(magazalar), 2):
            col_a, col_b = st.columns(2)
            name1, url1 = magazalar[i]
            col_a.link_button(name1, url1, use_container_width=True)
            if i + 1 < len(magazalar):
                name2, url2 = magazalar[i+1]
                col_b.link_button(name2, url2, use_container_width=True)
    else:
        st.warning("Lütfen bir ürün ismi girin.")
