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
st.title("G-ENGINE")
st.caption("Hardware Search Engine // Global Donanım Arama ve Doğrulama Motoru")
st.write("---")

# Seçim Modları
arama_turu = st.radio(
    "Arama Modu:", 
    ["Link Analizi", "Model İsmi ile Arama"], 
    horizontal=True
)

# Arama Formu
with st.form("arama_formu"):
    if arama_turu == "Link Analizi":
        girdi_alani = st.text_input("Ürün Linkini Girin:", placeholder="https://www.itopya.com/...")
    else:
        girdi_alani = st.text_input("Ürün Modelini Girin:", placeholder="Örn: AMD Ryzen 7 7800X3D")
    
    arama_tetiklendi = st.form_submit_button("Motoru Çalıştır", type="primary", use_container_width=True)

# 🧠 REGEX TABANLI DONANIM YAKALAMA MOTORU (Kesin Çözüm)
def gelişmiş_donanım_yakalayıcı(url):
    try:
        url = urllib.parse.unquote(url).lower()
        
        # Marka tespiti
        marka = ""
        for m in ["amd", "intel", "kingston", "asus", "msi", "gigabyte", "corsair", "gskill", "samsung", "crucial"]:
            if m in url:
                marka = m
                break
        
        # Donanım model kalıplarını yakalayan güçlü Regex mimarisi
        # İşlemci modellerini (örn: 9950x3d, 7800x3d, 12700f, 14900k) cımbızlar
        islemci_match = re.search(r'(\d{4,5}[xX]?[3-5]?[dD]?\d?|[iI][3579]-\d{4,5}[kKfF]?[sS]?)', url)
        
        # RAM/Bellek kalıplarını (örn: ddr5, ddr4, 32gb, 16gb, 6400mhz) cımbızlar
        ram_match = re.findall(r'(\d{2,3}gb|ddr[45]|\d{4}mhz)', url)
        
        sonuc_kelimeleri = []
        if marka:
            sonuc_kelimeleri.append(marka)
            
        if islemci_match:
            sonuc_kelimeleri.append(islemci_match.group(1))
        elif ram_match:
            # RAM linkiyse yakalanan ddr ve gb bilgilerini ekle
            sonuc_kelimeleri.extend(ram_match[:2])
            
        # Eğer özel mimari hiçbir şey yakalayamazsa eski güvenli sisteme dön
        if len(sonuc_kelimeleri) <= 1:
            link_yolu = urllib.parse.urlparse(url).path
            ham_kelimeler = re.split(r'[/_\-+.]', link_yolu)
            site_copleri = {"html", "urun", "p", "detay", "fiyat", "ozellikleri", "satinal", "gaming", "com", "tr", "itopya", "www", "https"}
            temiz = [k for k in ham_kelimeler if k and k not in site_copleri and len(k) > 1 and not (k.isdigit() and len(k) <= 3)]
            return temiz[:3]
            
        return sonuc_kelimeleri
    except:
        return ["oyuncu", "ekipmani"]

# Karakter Onarıcı
def karakter_onari(metin):
    sozluk = {"İ": "i", "ı": "i", "Ş": "s", "ş": "s", "Ç": "c", "ç": "c", "Ğ": "g", "ğ": "g
