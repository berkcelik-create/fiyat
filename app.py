import streamlit as st
import urllib.parse
import re

# Sayfa Yapılandırması
st.set_page_config(
    page_title="G-ENGINE // Hardware Search Engine", 
    page_icon="🔍", 
    layout="centered"
)

# Başlık ve Tasarım Düzeni
st.title("🔍 G-ENGINE")
st.caption("Hardware Search Engine // Global Donanım Arama ve Doğrulama Motoru")
st.write("---")

# Seçim Modları
arama_turu = st.radio(
    "Arama Modu:", 
    ["🔗 Link Analizi", "⌨️ Model İsmi ile Arama"], 
    horizontal=True
)

# Arama Formu
with st.form("arama_formu"):
    if arama_turu == "🔗 Link Analizi":
        girdi_alani = st.text_input("Ürün Linkini Girin:", placeholder="https://www.itopya.com/...")
    else:
        girdi_alani = st.text_input("Ürün Modelini Girin:", placeholder="Örn: AMD Ryzen 7 7800X3D")
    
    arama_tetiklendi = st.form_submit_button("🔍 Motoru Çalıştır", type="primary", use_container_width=True)

# 🧠 GELİŞMİŞ LINK ANALİZ MOTORU
def yapay_zeka_link_cozucu(url):
    try:
        url = url.strip()
        if not url.startswith(("http://", "https://")):
            url = "https://" + url
            
        # URL'i çöz ve tamamen küçük harfe çevir
        cozulmus_url = urllib.parse.unquote(url).lower()
        parsed_url = urllib.parse.urlparse(cozulmus_url)
        
        # Domain ve query'leri atıp sadece saf link yolunu alıyoruz
        link_yolu = parsed_url.path
        
        # Linki tüm olası ayıraçlara göre kelimelere böl
        ham_kelimeler = re.split(r'[/_\-+.]', link_yolu)
        
        # Web sitesine ait gereksiz kelime filtre havuzu
        site_copleri = {
            "html", "urun", "p", "detay", "fiyat", "ozellikleri", "satinal", "gaming", 
            "oyuncu", "store", "product", "com", "tr", "net", "org", "item", "shop", 
            "kampanya", "indirim", "firsat", "bilgisayar", "itopya", "vatanbilgisayar",
            "sinerji", "incehesap", "trendyol", "hepsiburada", "amazon", "wraithesports",
            "www", "https", "http"
        }
        
        filtrelenmiş_kelimeler = []
        for k in ham_kelimeler:
            k = k.strip()
            if len(k) > 1 and not k.isdigit() and k not in site_copleri:
                # E-ticaret sitelerinin otomatik bastığı u32084
