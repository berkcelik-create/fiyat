import streamlit as st
import urllib.parse

# Sayfa Ayarları
st.set_page_config(
    page_title="G-ENGINE // Hardware Search Engine", 
    page_icon="🔍", 
    layout="centered"
)

# Başlık
st.title("🔍 G-ENGINE")
st.caption("Hardware Search Engine // Global Donanım Arama Motoru")
st.write("---")

# 1. KISIM: HIZLI ERİŞİM BUTONLARI
st.write("### ⚡ Hızlı Erişim")
col1, col2, col3, col4 = st.columns(4)

# Butona basıldığında session_state değerini güncelle
if col1.button("🖱️ Logitech"): st.session_state.girdi = "Logitech"
if col2.button("🖱️ Razer"): st.session_state.girdi = "Razer"
if col3.button("⌨️ SteelSeries"): st.session_state.girdi = "SteelSeries"
if col4.button("⚡ Ekran Kartı"): st.session_state.girdi = "Ekran Kartı"

# Arama Modu
arama_turu = st.radio("Arama Modu:", ["🔗 Link Analizi", "⌨️ Model İsmi ile Arama"], horizontal=True)

# 2. KISIM: ARAMA FORMU
with st.form("arama_formu"):
    # Hızlı erişimden gelen değeri 'value' kısmına atıyoruz
    val = st.session_state.get("girdi", "")
    
    if arama_turu == "🔗 Link Analizi":
        girdi_alani = st.text_input("Ürün Linkini Girin:", placeholder="https://www.itopya.com/...")
    else:
        girdi_alani = st.text_input("Ürün Modelini Girin:", value=val, placeholder="Örn: AMD Ryzen 7 7800X3D")
    
    arama_tetiklendi = st.form_submit_button("🔍 Motoru Çalıştır", type="primary", use_container_width=True)

# 3. KISIM: ARAMA İŞLEMLERİ VE UYARI
if arama_tetiklendi and girdi_alani:
    st.info("⚠️ **Not:** Fiyatlar ve stoklar mağazalarda anlık değişebilir. Lütfen linke tıkladıktan sonra güncel durumu kontrol edin.")
    
    arama_kelimesi = girdi_alani
    arama_kelimesi_upper = arama_kelimesi.upper()
    
    st.success(f"🎯 Hedef Model: **{arama_kelimesi_upper}**")
    st.code(arama_kelimesi_upper, language="text")
        
    safe_search = urllib.parse.quote(arama_kelimesi.lower())
    
    # Mağazalar
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
    sol_col, sag_col = st.columns(2)
    
    for i, m in enumerate(tum_magazalar):
        buton_metni = f"{m['logo']} {m['ad']}"
        if i % 2 == 0:
            sol_col.link_button(buton_metni, m['url'], use_container_width=True)
        else:
            sag_col.link_button(buton_metni, m['url'], use_container_width=True)
