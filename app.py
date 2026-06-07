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

# 🚀 İTOPYA %100 ÇÖZÜM: YENİ NESİL KELİME AYIKLAMA ALGORİTMASI
def gelişmiş_kelime_temizle(url):
    try:
        if not url.startswith("http://") and not url.startswith("https://") and "." not in url:
            return None
            
        # URL'i decode et (%20 ve Türkçe karakterleri kurtar)
        url_cozulmus = urllib.parse.unquote(url).lower()
        
        # Query parametrelerini (? ve sonrasını) tamamen kopar
        url_temiz = url_cozulmus.split("?")[0].split("#")[0]
        
        # Gereksiz web protokollerini ve domain uzantılarını temizle
        url_temiz = re.sub(r'https?://', '', url_temiz)
        url_temiz = re.sub(r'www\.', '', url_temiz)
        
        # Linki tüm ayırıcılara göre (slash, tire, alt tire, artı) parçala
        parcalar = re.split(r'[/_\-+]', url_temiz)
        
        # Tamamen elenecek çöp ve site adı kelimeleri Havuzu
        yasakli = {
            "html", "urun", "p", "detay", "fiyat", "ozellikleri", "satinal", "gaming", 
            "oyuncu", "store", "product", "com", "net", "tr", "org", "item", "shop", 
            "kampanya", "indirim", "firsat", "bilgisayar", "itopya", "vatanbilgisayar",
            "sinerji", "incehesap", "trendyol", "hepsiburada", "amazon", "wraithesports"
        }
        
        anlamli_parcalar = []
        for p in parcalar:
            p_temiz = p.strip()
            # Kelime boş değilse, tamamen sayıdan oluşmuyorsa ve yasaklı listede yoksa al
            if len(p_temiz) > 1 and not p_temiz.isdigit() and p_temiz not in yasakli:
                # Sitelerin otomatik bastığı ürün kodlarını (Örn: u32084 veya p234) eliyoruz
                if not (any(char.isdigit() for char in p_temiz) and len(p_temiz) <= 6):
                    anlamli_parcalar.append(p_temiz)
        
        if anlamli_parcalar:
            # Ürün markası ve modeli her zaman bu listenin ilk kelimeleridir
            # Arama motorlarının sapıtmaması için en net ilk 4 kelimeyi çekiyoruz
            sonuc_kelimeleri = anlamli_parcalar[:4]
            ham_sonuc = " ".join(sonuc_kelimeleri)
            
            # Sadece harf, sayı ve boşlukları koru
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

    if hata_var or not arama_kelimesi or len(arama_kelimesi) < 2:
        st.error("❌ Analiz Başarısız. Lütfen girdi formatını kontrol edin.")
    else:
        arama_kelimesi_upper = arama_kelimesi.upper()
        
        st.success(f"🎯 Kriptonize Edilen Model:
