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
        # Link temizleme ön hazırlığı
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
        
        # Web sitelerine ait gereksiz kelime filtre havuzu
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
                # E-ticaret sitelerinin otomatik bastığı u32084 gibi benzersiz kodları eliyoruz
                if not (any(char.isdigit() for char in k) and len(k) <= 7):
                    filtrelenmiş_kelimeler.append(k)

        # Küresel donanım markaları öncelik havuzu
        bilinen_markalar = {
            "kingston", "asus", "msi", "gigabyte", "amd", "intel", "nvidia", "corsair", 
            "gskill", "team", "t-force", "samsung", "crucial", "wd", "western", "digital", 
            "seagate", "pny", "zotac", "palit", "gainward", "sapphire", "xfx", "powercolor",
            "razer", "logitech", "steelseries", "hyperx", "glorious", "benq"
        }
        
        # Eğer temizlenen kelimelerde marka adı bulunursa, marka ve yanındaki en kritik 2 kelimeyi seç
        for i, kelime in enumerate(filtrelenmiş_kelimeler):
            if kelime in bilinen_markalar:
                return " ".join(filtrelenmiş_kelimeler[i:i+3])
                
        # Marka bulunamazsa en anlamlı ilk 3 kelimeyi döndür
        if filtrelenmiş_kelimeler:
            return " ".join(filtrelenmiş_kelimeler[:3])
            
        return "oyuncu ekipmani"
    except:
        return "oyuncu ekipmani"

# Karakter Onarıcı
def karakter_onari(metin):
    metin = " ".join(metin.split())
    sozluk = {"İ": "i", "ı": "i", "Ş": "s", "ş": "s", "Ç": "c", "ç": "c", "Ğ": "g", "ğ": "g", "Ü": "u", "ü": "u", "Ö": "o", "ö": "o"}
    for eski, yeni in sozluk.items():
        metin = metin.replace(eski, yeni)
    return metin.lower()

# Motor Çalışma Mantığı
if arama_tetiklendi and girdi_alani:
    ana_arama_terimi = ""
    
    if arama_turu == "🔗 Link Analizi":
        ana_arama_terimi = yapay_zeka_link_cozucu(girdi_alani)
    else:
        ana_arama_terimi = girdi_alani
        
    if ana_arama_terimi and len(ana_arama_terimi) >= 2:
        # Arama kelimelerini küçük harfle normalize ediyoruz (İtopya uyumluluğu için şart!)
        sorgu_temiz = karakter_onari(ana_arama_terimi)
        sorgu_gosterim = sorgu_temiz.upper()
        
        # Sonuç Ekranı
        st.success(f"🎯 Kriptonize Edilen Model: **{sorgu_gosterim}**")
        
        st.write("📋 Başka yerde aratmak için ismi buradan hızlıca kopyalayabilirsiniz:")
        st.code(sorgu_gosterim, language="text")
        
        # 🌟 Standart Boşluklu Encode (Diğer tüm siteler için)
        safe_search_normal = urllib.parse.quote(sorgu_temiz
