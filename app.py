import streamlit as st
import urllib.parse
import re

# Sayfa Ayarları
st.set_page_config(
    page_title="G-ENGINE // Hardware Search Engine", 
    page_icon="🔍", 
    layout="centered"
)

st.title("🔍 G-ENGINE")
st.caption("Hardware Search Engine // Global Donanım Arama ve Doğrulama Motoru")
st.write("---")

# Arama Modu
arama_turu = st.radio("Arama Modu:", ["🔗 Link Analizi", "⌨️ Model İsmi ile Arama"], horizontal=True)

# ⚡ HIZLI ERİŞİM BUTONLARI (Kullanıcı için pratik marka/tür seçimi)
st.write("### ⚡ Hızlı Erişim")
c1, c2, c3, c4 = st.columns(4)

# Butona basıldığında session_state üzerinden metin kutusunu dolduruyoruz
if c1.button("🖱️ Logitech"): st.session_state.quick_search = "Logitech"
if c2.button("🖱️ Razer"): st.session_state.quick_search = "Razer"
if c3.button("⌨️ SteelSeries"): st.session_state.quick_search = "SteelSeries"
if c4.button("⚡ Ekran Kartı"): st.session_state.quick_search = "Ekran Kartı"

# Form Yapısı
with st.form("arama_formu"):
    if arama_turu == "🔗 Link Analizi":
        girdi_alani = st.text_input("Ürün Linkini Girin:", placeholder="https://www.itopya.com/...")
    else:
        # Hızlı erişimden gelen değeri buraya value olarak atadık
        val = st.session_state.get("quick_search", "")
        girdi_alani = st.text_input("Ürün Modelini Girin:", value=val, placeholder="Örn: AMD Ryzen 7 7800X3D")
    
    arama_tetiklendi = st.form_submit_button("🔍 Motoru Çalıştır", type="primary", use_container_width=True)

# --- (Gelişmiş Kelime Temizleme ve Mağaza Fonksiyonları Aynı Kalıyor) ---

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
            return re.sub(r'[^a-zA-Z0-9\s]', '', ham_sonuc).strip()
        return "Oyuncu Ekipmanı"
    except:
        return "Oyuncu Ekipmanı"

if arama_tetiklendi and girdi_alani:
    st.info("⚠️ **Not:** Fiyatlar ve stoklar mağazalarda anlık değişebilir. Lütfen linke tıkladıktan sonra güncel durumu kontrol edin.")
    
    arama_kelimesi = gelişmiş_kelime_temizle(girdi_alani) if arama_turu == "🔗 Link Analizi" else girdi_alani
    
    if arama_kelimesi:
        arama_kelimesi_upper = arama_kelimesi.upper()
        st.success(f"🎯 Kriptonize Edilen Model: **{arama_kelimesi_upper}**")
        st.code(arama_kelimesi_upper, language="text")
        
        safe_search = urllib.parse.quote(arama_kelimesi.lower())
        
        tum_magazalar = [
            {"ad": "Wraith Esports", "url": f"https://wraithesports.com/search?q={safe_search}", "logo": "🚀"},
            {"ad": "İncehesap", "url": f"https://www.incehesap.com/arama/?fiyat_kriteri=1&s={safe_search}", "logo": "🔥"},
            {"ad": "İtopya", "url": f"https://www.itopya.com/Arama?q={safe_search}", "logo": "🦎"},
            {"ad": "Sinerji", "url": f"https://www.sinerji.gen.tr/arama?q={safe_search}", "logo": "⚡"},
            {"ad": "Trendyol", "url": f"https://www.trendyol.com/sr?q={safe_search}", "logo": "🧡"},
            {"ad": "Hepsiburada", "url": f"https://www.hepsiburada.com/ara?q={safe_search}", "logo": "💙"},
            {"ad": "Amazon TR", "url": f"https://www.amazon.com.tr/s?k={safe_search}", "logo": "💛"},
            {"ad": "Akakçe", "url": f"https://www.akakce.com/arama/?q={safe_search}", "logo": "🔍"}
        ]
        
        st.subheader("🛍️ Mağaza Seçenekleri")
        sol, sag = st.columns(2)
        for i, m in enumerate(tum_magazalar):
            (sol if i % 2 == 0 else sag).link_button(f"{m['logo']} {m['ad']}", m['url'], use_container_width=True)
