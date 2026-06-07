import streamlit as st
import urllib.parse
import re

# --- Sayfa Yapılandırması ---
st.set_page_config(
    page_title="G-ENGINE // Hardware Search Engine", 
    page_icon="🔍", 
    layout="centered"
)

# --- Sarı Tonlarında Modern Arka Plan ---
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #FFD700, #FFA500, #FF8C00);
        background-size: 400% 400%;
        animation: gradient 10s ease infinite;
    }
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    h1, h2, h3, p, label {
        color: #2e2e2e !important;
        font-weight: 600;
    }
    .stTextInput > div > div > input {
        background-color: rgba(255, 255, 255, 0.8) !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Yan Menü ---
st.sidebar.title("👤 İletişim")
st.sidebar.info("G-ENGINE geliştiricisi ile iletişime geçmek için:")
st.sidebar.link_button("Discord Profilim", "https://discord.com/users/714481744295886990", use_container_width=True)
st.sidebar.write("---")
st.sidebar.caption("G-ENGINE v1.0 // Hardware Search")

# --- Ana Sayfa ---
st.title("🔍 G-ENGINE")
st.caption("Hardware Search Engine // Orijinal Arama Motoru")
st.write("---")

arama_turu = st.radio(
    "Arama Modu:", 
    ["Link Analizi", "Model İsmi ile Arama"], 
    horizontal=True
)

with st.form("arama_formu"):
    if arama_turu == "Link Analizi":
        girdi_alani = st.text_input("Ürün Linkini Girin:", placeholder="https://www.itopya.com/...")
    else:
        girdi_alani = st.text_input("Ürün Modelini Girin:", placeholder="Örn: PNY RTX 5070")
    arama_tetiklendi = st.form_submit_button("Motoru Çalıştır", type="primary", use_container_width=True)

# --- Fonksiyonlar ---
def link_temizle_ve_coz(url):
    try:
        url = url.strip().lower()
        if not url.startswith(("http://", "https://")): url = "https://" + url
        parsed_url = urllib.parse.urlparse(urllib.parse.unquote(url))
        ham = re.split(r'[/_\-+.]', parsed_url.path)
        engelli = ["html", "urun", "p", "detay", "ara", "geforce", "oc", "overclock", "v2", "gaming", "rgb", "white", "black", "mouse", "kulaklik"]
        filtrelenmis = [k for k in ham if k and k not in engelli and not (k.startswith('u') and any(c.isdigit() for c in k)) and not (k.isdigit() and len(k) <= 3)]
        return filtrelenmis[:4] if filtrelenmis else ["donanimi"]
    except: return ["donanimi"]

def guvenli_metin_onar(metin):
    return metin.lower().strip().replace("ı", "i").replace("ş", "s").replace("ç", "c").replace("ğ", "g").replace("ü", "u").replace("ö", "o")

# --- İşlem ---
if arama_tetiklendi and girdi_alani:
    if arama_turu == "Link Analizi": 
        kelimeler = link_temizle_ve_coz(girdi_alani)
    else: 
        kelimeler =
