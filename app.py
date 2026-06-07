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

# 🚀 YENİLENMİŞ GELİŞMİŞ KELİME TEMİZLEME MOTORU
def gelişmiş_kelime_temizle(url):
    try:
        if not url.startswith("http://") and not url.startswith("https://") and "." not in url:
            return None
            
        # URL çözme işlemi (Türkçe karakterleri ve %20 gibi kodları düzeltir)
        url = urllib.parse.unquote(url)
        
        # Query parametrelerini (? ve sonrası) ve hashtagleri temizle
        url_temiz = url.split("?")[0].split("#")[0]
        
        # Linki parçalarına ayır ve temizle
        parcalar = re.split(r'[/_-]', url_temiz)
        
        # E-ticaret sitelerinin kullandığı çöp kelimeler listesi
        yasakli = {
            "html", "urun", "p", "detay", "fiyat", "ozellikleri", "satinal", "gaming", 
            "oyuncu", "store", "product", "com", "tr", "www", "https", "http", "item", 
            "shop", "selling", "kampanya", "indirim", "firsat", "tekno", "bilgisayar"
        }
        
        temiz = []
        for k in parcalar:
            k_temiz = k.replace(".html", "").strip()
            # Kelime kontrolü: Sayısal kod değilse, yasaklı listede yoksa ve 2 karakterden uzunsa al
            if len(k_temiz) > 2 and not k_temiz.isdigit() and k_temiz.lower() not in yasakli:
                # E-ticaret ID yapılarını temizle (Örn: p-234234 veya om34234 gibi sayı içeren ekler)
                if not any(char.isdigit() for char in k_temiz) or len(re.sub(r'\d', '', k_temiz)) > 3:
                    temiz.append(k_temiz)
                    
        if temiz:
            # En anlamlı ilk 4 kelimeyi birleştir (Arama motorlarının en sevdiği uzunluk)
            ham_sonuc = " ".join(temiz[:4])
            # Özel karakterleri tamamen uçur, sadece harf ve sayı bırak
            temiz_sonuc = re.sub(r'[^a-zA-Z0-9\s]', '', ham_sonuc)
            return temiz_sonuc.strip()
            
        return "Oyuncu Ekipmanı"
    except:
        return "Oyuncu Ekipmanı"

# Akıllı Boşluk ve Türkçe Karakter Toleransı
def akilli_metin_duzelt(metin):
    metin = " ".join(metin.split())
    donusum = {"İ": "I", "ı": "i", "Ş": "S", "ş": "s", "Ç": "C", "ç": "c", "Ğ": "G", "ğ": "g", "Ü": "U", "ü": "u", "Ö": "O", "ö": "o"}
    for kaynak, placeholder in donusum.items():
        metin = metin.replace(kaynak, placeholder)
    return metin

# Arama Motorunun Çalıştırılma Aşaması
if arama_tetiklendi and girdi_alani:
    hata_var = False
    arama_kelimesi = ""
    
    if arama_turu == "🔗 Link Analizi":
        sonuc = gelişmiş_kelime_temizle(girdi_alani)
        if sonuc is None:
            hata_var = True
        else:
            arama_kelimesi = sonuc
    else:
        arama_kelimesi = girdi_alani
            
    if arama_kelimesi:
        arama_kelimesi = akilli_metin_duzelt(arama_kelimesi)
