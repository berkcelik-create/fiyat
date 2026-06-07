import streamlit as st
import urllib.parse

# 1. Sayfa Ayarları (Görsel Temel)
st.set_page_config(page_title="G-ENGINE", page_icon="🔍", layout="centered")

# 2. CSS Animasyonları ve Stil (Görsel Şıklık)
st.markdown("""
    <style>
    /* Arka Plan ve Genel Font */
    .stApp { background-color: #0e1117; }
    
    /* Buton Animasyonları */
    div.stButton > button:hover {
        transform: scale(1.02);
        transition: 0.3s;
        border: 1px solid #ff4b4b;
    }
    
    /* Başlık Rengi */
    h1 { color: #ff4b4b !important; }
    
    /* Link Butonları Renklendirme */
    div.stLinkButton > a {
        background-color: #1f2329 !important;
        border-radius: 8px !important;
        transition: 0.3s !important;
    }
    div.stLinkButton > a:hover {
        background-color: #ff4b4b !important;
        color: white !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🔍 G-ENGINE")
st.write("---")

# Hızlı Erişim Butonları
col1, col2, col3, col4 = st.columns(4)
if col1.button("Logitech"): st.session_state.girdi = "Logitech"
if col2.button("Razer"): st.session_state.girdi = "Razer"
if col3.button("SteelSeries"): st.session_state.girdi = "SteelSeries"
if col4.button("Ekran Kartı"): st.session_state.girdi = "Ekran Kartı"

# Arama Kutusu
val = st.session_state.get("girdi", "")
girdi_alani = st.text_input("Ürün Modelini Girin:", value=val)

if st.button("Motoru Çalıştır", type="primary"):
    if girdi_alani:
        safe_search = urllib.parse.quote(girdi_alani.lower())
        
        # Mağazalar (Şık liste)
        magazalar = [
            ("🚀 Wraith Esports", f"https://wraithesports.com/search?q={safe_search}"),
            ("🔥 İncehesap", f"https://www.incehesap.com/arama/?s={safe_search}"),
            ("🦎 İtopya", f"https://www.itopya.com/Arama?q={safe_search}"),
            ("⚡ Sinerji", f"https://www.sinerji.gen.tr/arama?q={safe_search}"),
            ("🧡 Trendyol", f"https://www.trendyol.com/sr?q={safe_search}"),
            ("💙 Hepsiburada", f"https://www.hepsiburada.com/ara?q={safe_search}"),
            ("💛 Amazon TR", f"https://www.amazon.com.tr/s?k={safe_search}"),
            ("🔍 Akakçe", f"https://www.akakce.com/arama/?q={safe_search}")
        ]
        
        # Sonuçları sütunlara dağıtarak göster
        for i in range(0, len(magazalar), 2):
            col_a, col_b = st.columns(2)
            name1, url1 = magazalar[i]
            col_a.link_button(name1, url1, use_container_width=True)
            if i+1 < len(magazalar):
                name2, url2 = magazalar[i+1]
                col_b.link_button(name2, url2, use_container_width=True)
    else:
        st.warning("Lütfen bir ürün ismi girin.")
