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

# 🛠️ GÜVENLİ LINK ÇÖZÜMLEME MOTORU
def link_analiz_et(url):
    try:
        url = url.strip()
        if not url.startswith(("http://", "https://")):
            url = "https://" + url
            
        # URL'i decode et ve tamamen küçük harfe çevir
        cozulmus_url = urllib.parse.unquote(url).lower()
        parsed_url = urllib.parse.urlparse(cozulmus_url)
        
        # Domain ve query'leri temizleyip sadece saf ürün yolunu alıyoruz
        link_yolu = parsed_url.path
        
        # Linki tüm olası ayıraçlara göre kelimelere böl
        ham_kelimeler = re.split(r'[/_\-+.]', link_yolu)
        
        # Siteden gelebilecek gereksiz çöp kelimeler havuzu
        site_copleri = {
            "html", "urun", "p", "detay", "fiyat", "ozellikleri", "satinal", "gaming", 
            "oyuncu", "store", "product", "com", "tr", "net", "org", "item", "shop", 
            "kampanya", "indirim", "firsat", "bilgisayar", "itopya", "vatanbilgisayar",
            "sinerji", "incehesap", "trendyol", "hepsiburada", "amazon", "wraithesports",
            "www", "https", "http"
        }
        
        filtrelenmis_kelimeler = []
        for k in ham_kelimeler:
            k = k.strip()
            if len(k) > 1 and not k.isdigit() and k not in site_copleri:
                # E-ticaret sitelerinin otomatik ürettiği kısa kodları (u32084 gibi) eliyoruz
                if not (any(char.isdigit() for char in k) and len(k) <= 7):
                    filtrelenmis_kelimeler.append(k)

        # Küresel donanım markaları havuzu
        bilinen_markalar = {
            "kingston", "asus", "msi", "gigabyte", "amd", "intel", "nvidia", "corsair", 
            "gskill", "team", "t-force", "samsung", "crucial", "wd", "western", "digital", 
            "seagate", "pny", "zotac", "palit", "gainward", "sapphire", "xfx", "powercolor",
            "razer", "logitech", "steelseries", "hyperx", "glorious", "benq"
        }
        
        # Marka adı bulunursa, marka ve yanındaki en kritik 2 kelimeyi seç
        for i, kelime in enumerate(filtrelenmis_kelimeler):
            if kelime in bilinen_markalar:
                return filtrelenmis_kelimeler[i:i+3]
                
        if filtrelenmis_kelimeler:
            return filtrelenmis_kelimeler[:3]
            
        return ["oyuncu", "ekipmani"]
    except:
        return ["oyuncu", "ekipmani"]

# Karakter Onarıcı (Listenin her elemanına uygulanır)
def karakter_onari(metin):
    sozluk = {"İ": "i", "ı": "i", "Ş": "s", "ş": "s", "Ç": "c", "ç": "c", "Ğ": "g", "ğ": "g", "Ü": "u", "ü": "u", "Ö": "o", "ö": "o"}
    for eski, yeni in sozluk.items():
        metin = metin.replace(eski, yeni)
    return metin.lower().strip()

# Motorun Çalışma Senaryosu
if arama_tetiklendi and girdi_alani:
    kelime_listesi = []
    
    if arama_turu == "🔗 Link Analizi":
        kelime_listesi = link_analiz_et(girdi_alani)
    else:
        # Metin araması yapıldıysa kelimeleri boşluğa göre ayır
        ham_kelimeler = girdi_alani.split()
        kelime_listesi = [k.strip() for k in ham_kelimeler if k.strip()]
        
    # Kelimeleri Türkçe karakterlerden arındırıp temizleyelim
    temiz_kelimeler = [karakter_onari(k) for k in kelime_listesi if k.strip()]
    
    if temiz_kelimeler:
        # Ekranda şık görünmesi için kelimeleri birleştirip büyük harfe çeviriyoruz
        gosterim_metni = " ".join(temiz_kelimeler).upper()
        
        st.success(f"🎯 Kriptonize Edilen Model: **{gosterim_metni}**")
        
        st.write("📋
