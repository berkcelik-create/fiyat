import streamlit as st
import urllib.parse
import re

# Sayfa Ayarları
st.set_page_config(
    page_title="G-ENGINE // Hardware Search Engine", 
    page_icon="🔍", 
    layout="centered"
)

# Başlık Düzeni
st.title("🔍 G-ENGINE")
st.caption("Hardware Search Engine // Global Donanım Arama ve Doğrulama Motoru")
st.write("---")

# Arama Modları
arama_turu = st.radio(
    "Arama Modu:", 
    ["🔗 Link Analizi", "⌨️ Model İsmi ile Arama"], 
    horizontal=True
)

# Ana Arama Formu
with st.form("arama_formu"):
    if arama_turu == "🔗 Link Analizi":
        girdi_alani = st.text_input("Ürün Linkini Girin:", placeholder="https://www.itopya.com/...")
    else:
        girdi_alani = st.text_input("Ürün Modelini Girin:", placeholder="Örn: AMD Ryzen 7 7800X3D")
    
    arama_tetiklendi = st.form_submit_button("🔍 Motoru Çalıştır", type="primary", use_container_width=True)

# 🛠️ GÜVENLİ VE SIFIR HATALI KELİME AYIKLAMA FONKSİYONU
def link_analiz_et(url):
    try:
        if not url.startswith(("http://", "https://")):
            url = "https://" + url
            
        # URL'i decode et ve temizle
        cozulmus_url = urllib.parse.unquote(url).lower()
        parsed_url = urllib.parse.urlparse(cozulmus_url)
        
        # Sadece path kısmını al (Domain ve query parametreleri otomatik elenir)
        path = parsed_url.path
        
        # Çöp olabilecek teknik ifadeler ve site isimleri
        yasakli_kelimeler = {
            "html", "urun", "p", "detay", "fiyat", "ozellikleri", "satinal", "gaming", 
            "oyuncu", "store", "product", "com", "tr", "net", "org", "item", "shop", 
            "kampanya", "indirim", "firsat", "bilgisayar", "itopya", "vatanbilgisayar",
            "sinerji", "incehesap", "trendyol", "hepsiburada", "amazon", "wraithesports",
            "mhz", "cl32", "cl30", "cl36", "ddr5", "ddr4", "single", "kit", "dual", "ram"
        }
        
        # Metni parçala
        kelimeler = re.split(r'[/_\-+.]', path)
        temiz_kelimeler = []
        
        for k in kelimeler:
            k = k.strip()
            # Kelime mantıklı uzunluktaysa, saf sayı değilse ve yasaklı havuzda yoksa ekle
            if len(k) > 1 and not k.isdigit() and k not in yasakli_kelimeler:
                # E-ticaret sitelerinin sonuna eklediği u32084 gibi kodları eliyoruz
                if not (any(char.isdigit() for char in k) and len(k) <= 7):
                    temiz_kelimeler.append(k)
                    
        if temiz_kelimeler:
            # Marka ve model genellikle ilk 3 kelimede netleşir
            return " ".join(temiz_kelimeler[:3]).strip()
        return "oyuncu ekipmani"
    except:
        return "oyuncu ekipmani"

# Türkçe Kar
