import streamlit as st
import urllib.parse
import re

# Sayfa Ayarları ve Sekme Emojisi
st.set_page_config(
    page_title="G-ENGINE // Hardware Search Engine", 
    page_icon="🔍", 
    layout="centered"
)

# Arama Motoru Başlık Düzeni
st.title("🔍 G-ENGINE")
st.caption("Hardware Search Engine // Global Donanım Arama ve Doğrulama Motoru")
st.write("---")

# İki Farklı Net Arama Modu
arama_turu = st.radio(
    "Arama Modu:", 
    ["🔗 Link Analizi", "⌨️ Model İsmi ile Arama"], 
    horizontal=True
)

# Ana Arama Form Yapısı
with st.form("arama_formu"):
    if arama_turu == "🔗 Link Analizi":
        girdi_alani = st.text_input("Ürün Linkini Girin:", placeholder="https://www.itopya.com/...")
    else:
        girdi_alani = st.text_input("Ürün Modelini Girin:", placeholder="Örn: AMD Ryzen 7 7800X3D")
    
    arama_tetiklendi = st.form_submit_button("🔍 Motoru Çalıştır", type="primary", use_container_width=True)

# 🚀 İTOPYA VE PAZAR YERLERİ İÇİN %100 GARANTİLİ LINK ÇÖZÜMLEME MOTORU
def gelişmiş_kelime_temizle(url):
    try:
        if not url.startswith("http://") and not url.startswith("https://") and "." not in url:
            return None
            
        # URL'i decode et (%20 ve Türkçe karakter karmaşasını bitir)
        url_cozulmus = urllib.parse.unquote(url).lower()
        
        # Query parametrelerini (? ve sonrasını) uçur
        url_temiz = url_cozulmus.split("?")[0].split("#")[0]
        
        # Protokol ve www kısımlarını temizle
        url_temiz = re.sub(r'https?://', '', url_temiz)
        url_temiz = re.sub(r'www\.', '', url_temiz)
        
        # Linki tüm kırılımlarına (slash, tire, alt tire, artı) göre parçala
        parcalar = re.split(r'[/_\-+]', url_temiz)
        
        # Kesinlikle elenecek domain ve çöp kelimeler havuzu
        yasakli = {
            "html", "urun", "p", "detay", "fiyat", "ozellikleri", "satinal", "gaming", 
            "oyuncu", "store", "product", "com", "net", "tr", "org", "item", "shop", 
            "kampanya", "indirim", "firsat", "bilgisayar", "itopya", "vatanbilgisayar",
            "sinerji", "incehesap", "trendyol", "hepsiburada", "amazon", "wraithesports"
        }
        
        anlamli_parcalar = []
        for p in parcalar:
            p_temiz = p.strip()
            # Kelime yapısal olarak temizse, sadece sayı değilse ve yasaklı grupta değilse ekle
            if len(p_temiz) > 1 and not p_temiz.isdigit() and p_temiz not in yasakli:
                # E-ticaret sitelerinin otomatik bastığı kısa kodları (u32084 gibi
