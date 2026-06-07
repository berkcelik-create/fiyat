import streamlit as st
import urllib.parse
import re
import time

# Sayfa Ayarları
st.set_page_config(page_title="GamerFinder Pro", page_icon="🎮", layout="centered")

# Modern Stil ve Animasyonlar
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; }
    div.stButton > button:hover { transform: scale(1.02); transition: 0.3s; border: 1px solid #ff4b4b; }
    div.stLinkButton > a:hover { background-color: #ff4b4b !important; color: white !important; }
    h1 { color: #ff4b4b !important; }
    </style>
""", unsafe_allow_html=True)

st.title("🎮 GamerFinder Pro")
st.caption("Gelişmiş Oyuncu Ekipmanı Arama Motoru v7.5")
st.write("---")

# Hızlı Erişim Butonları
c1, c2, c3, c4 = st.columns(4)
if c1.button("🖱️ Logitech"): st.session_state.girdi = "Logitech"
if c2.button("🖱️ Razer"): st.session_state.girdi = "Razer"
if c3.button("⌨️ SteelSeries"): st.session_state.girdi = "SteelSeries"
if c4.button("⚡ Ekran Kartı"): st.session_state.girdi = "Ekran Kartı"

arama_turu = st.radio("Arama Yöntemi:", ["🔗 Link Analizi", "⌨️ Ürün İsim Arama"], horizontal=True)

# Form Yapısı
with st.form("arama_formu"):
    val = st.session_state.get("girdi", "")
    if arama_turu == "🔗 Link Analizi":
        girdi_alani = st.text_input("Ürün Linkini Yapıştırın:", placeholder="https://www.itopya.com/...")
    else:
        girdi_alani = st.text_input("Ürün Modelini Yazın:", value=val, placeholder="Örn: Razer Deathadder V3 Pro")
    
    arama_tetiklendi = st.form_submit_button("🔍 Fiyatları Karşılaştır", type="primary", use_container_width=True)

# Fonksiyonlar
def gelişmiş_kelime_temizle(url):
    try:
        url_temiz = url.split("?")[0].split("#")[0]
        parcalar = url_temiz.split("/")[-1].split("-")
        yasakli = {"html", "urun", "p", "detay", "fiyat", "ozellikleri", "satinal", "gaming", "oyuncu", "store", "product", "com", "tr"}
        temiz = [k.replace(".html", "") for k in parcalar if len(k) > 2 and not k.isdigit() and k.lower() not in yasakli]
        return " ".join(temiz[:4]) if temiz else "Oyuncu Ekipmanı"
    except: return "Oyuncu Ekipmanı"

def akilli_metin_duzelt(metin):
    metin = " ".join(metin.split())
    donusum = {"İ": "I", "ı": "i", "Ş": "S", "ş": "s", "Ç": "C", "ç": "c", "Ğ": "G", "ğ": "g", "Ü": "U", "ü": "u", "Ö": "O", "ö": "o"}
    for k, h in donusum.items(): metin = metin.replace(k, h)
    return metin

# İşlem
if arama_tetiklendi and girdi_alani:
    with st.spinner("🔄 Analiz ediliyor..."):
        time.sleep(0.5)
        arama_kelimesi = gelişmiş_kelime_temizle(girdi_alani) if arama_turu == "🔗 Link Analizi" else girdi_alani
        arama_kelimesi = akilli_metin_duzelt(arama_kelimesi)

    if not arama_kelimesi or len(arama_kelimesi) < 2:
        st.error("❌ Geçersiz Girdi!")
    else:
        st.info("⚠️ **Not:** Fiyatlar ve stoklar anlık değişebilir. Lütfen mağaza sayfasını kontrol edin.")
        arama_kelimesi_upper = arama_kelimesi.upper()
        st.success(f"🎯 Hedef: **{arama_kelimesi_upper}**")
        st.code(arama_kelimesi_upper, language="text")
            
        safe_search = urllib.parse.quote(arama_kelimesi.lower())
        is_donanim = any(x in arama_kelimesi.lower() for x in ["ekran karti", "islemci", "anakart", "ram", "ssd", "gpu", "cpu"])
        
        tum_magazalar = [
            {"ad": "Wraith Esports", "url": f"https://wraithesports.com/search?q={safe_search}", "logo": "🚀", "tip": "ekipman"},
            {"ad": "İncehesap", "url": f"https://www.incehesap.com/arama/?s={safe_search}", "logo": "🔥", "tip": "hepsi"},
            {"ad": "İtopya", "url": f"https://www.itopya.com/Arama?q={safe_search}", "logo": "🦎", "tip": "hepsi"},
            {"ad": "Sinerji", "url": f"https://www.sinerji.gen.tr/arama?q={safe_search}", "logo": "⚡", "tip": "hepsi"},
            {"ad": "Trendyol", "url": f"https://www.trendyol.com/sr?q={safe_search}", "logo": "🧡", "tip": "hepsi"},
            {"ad": "Amazon TR", "url": f"https://www.amazon.com.tr/s?k={safe_search}", "logo": "💛", "tip": "hepsi"},
            {"ad": "Akakçe", "url": f"https://www.akakce.com/arama/?q={safe_search}", "logo": "🔍", "tip": "hepsi"}
        ]
        
        st.subheader("🛍️ Mağaza Seçenekleri")
        aktif = [m for m in tum_magazalar if not (is_donanim and m["tip"] == "ekipman")]
        sol, sag = st.columns(2)
        for i, m in enumerate(aktif):
            (sol if i % 2 == 0 else sag).link_button(f"{m['logo']} {m['ad']}", m['url'], use_container_width=True)
