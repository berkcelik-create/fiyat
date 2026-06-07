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

# 🛠️ GELİŞMİŞ SÜZGEÇLİ LINK ANALİZ MOTORU
def link_analiz_et(url):
    try:
        url = url.strip()
        if not url.startswith(("http://", "https://")):
            url = "https://" + url
            
        # URL'i çöz ve tamamen küçük harfe çevir
        cozulmus_url = urllib.parse.unquote(url).lower()
        parsed_url = urllib.parse.urlparse(cozulmus_url)
        
        # Link yolunu al
        link_yolu = parsed_url.path
        
        # Linki tüm olası ayıraçlara göre kelimelere böl
        ham_kelimeler = re.split(r'[/_\-+.]', link_yolu)
        
        # Web sitesi çöp kelime filtre havuzu
        site_copleri = {
            "html", "urun", "p", "detay", "fiyat", "ozellikleri", "satinal", "gaming", 
            "oyuncu", "store", "product", "com", "tr", "net", "org", "item", "shop", 
            "kampanya", "indirim", "firsat", "bilgisayar", "itopya", "vatanbilgisayar",
            "sinerji", "incehesap", "trendyol", "hepsiburada", "amazon", "wraithesports",
            "www", "https", "http"
        }
        
        filtrelenmis = []
        for k in ham_kelimeler:
            k = k.strip()
            # Kelime boş değilse, çöp listesinde değilse ve sadece anlamsız kısa sayılardan ibaret değilse al
            if k and k not in site_copleri and len(k) > 1:
                # E-ticaret sitelerinin otomatik ürettiği u32084 benzeri kodları eliyoruz
                if not (k.startswith('u') and any(char.isdigit() for char in k)):
                    filtrelenmis.append(k)

        # Global donanım markaları havuzu
        bilinen_markalar = {"kingston", "asus", "msi", "gigabyte", "amd", "intel", "nvidia", "corsair", "gskill", "samsung", "crucial"}
        
        # Marka adını yakala ve peşinden gelen modeli temizle
        for i, kelime in enumerate(filtrelenmis):
            if kelime in bilinen_markalar:
                aday_kelimeler = filtrelenmis[i:i+4]
                temiz_model = []
                
                for sira, ak in enumerate(aday_kelimeler):
                    # İlk iki kelimeden sonrakiler tamamen sayıysa (örn link sonundaki '43') veya çok kısaysa ekleme
                    if sira >= 2 and ak.isdigit() and len(ak) <= 3:
                        continue
                    temiz_model.append(ak)
                return temiz_model
                
        if filtrelenmis:
            return filtrelenmis[:3]
            
        return ["oyuncu", "ekipmani"]
    except:
        return ["oyuncu", "ekipmani"]

# Karakter Onarıcı
def karakter_onari(metin):
    sozluk = {"İ": "i", "ı": "i", "Ş": "s", "ş": "s", "Ç": "c", "ç": "c", "Ğ": "g", "ğ": "g", "Ü": "u", "ü": "u", "Ö": "o", "ö": "o"}
    for eski, yeni in sozluk.items():
        metin = metin.replace(eski, yeni)
    return metin.lower().strip()

# Motorun Çalışma Mantığı
if arama_tetiklendi and girdi_alani:
    kelime_listesi = []
    
    if arama_turu == "Link Analizi":
        kelime_listesi = link_analiz_et(girdi_alani)
    else:
        kelime_listesi = [k.strip() for k in girdi_alani.split() if k.strip()]
        
    temiz_kelimeler = [karakter_onari(k) for k in kelime_listesi if k.strip()]
    
    if temiz_kelimeler:
        gosterim_metni = " ".join(temiz_kelimeler).upper()
        
        st.success("Model Basariyla Cozuldu: " + gosterim_metni)
        st.write("Kopyalama Alani:")
        st.code(gosterim_metni, language="text")
        
        # URL Standartlaştırma (Boşluklu güvenli yapı - Tüm siteler için en stabil yöntem)
        standart_sorgu = " ".join(temiz_kelimeler)
        safe_search = urllib.parse.quote(standart_sorgu)
        
        # Mağazalar Listesi 
        magaza_listesi = [
            {"ad": "Wraith Esports", "url": f"https://wraithesports.com/search?q={safe_search}"},
            {"ad": "Incehesap", "url": f"https://www.incehesap.com/arama/?fiyat_kriteri=1&s={safe_search}"},
            {"ad": "Itopya", "url": f"https://www.itopya.com/Arama?q={safe_search}"},
            {"ad": "Sinerji", "url": f"https://www.sinerji.gen.tr/arama?q={safe_search}"},
            {"ad": "Trendyol", "url": f"https://www.trendyol.com/sr?q={safe_search}"},
            {"ad": "Hepsiburada", "url": f"https://www.hepsiburada.com/ara?q={safe_search}"},
            {"ad": "Amazon TR", "url": f"https://www.amazon.com.tr/s?k={safe_search}"},
            {"ad": "Akakce", "url": f"https://www.akakce.com/arama/?q={safe_search}"}
        ]
        
        st.subheader("Magaza Secenekleri")
        sol_sutun, sag_sutun = st.columns(2)
        
        for sira, veri in enumerate(magaza_listesi):
            if sira % 2 == 0:
                sol_sutun.link_button(veri["ad"], veri["url"], use_container_width=True)
            else:
                sag_sutun.link_button(veri["ad"], veri["url"], use_container_width=True)
    else:
        st.error("Analiz Hatasi: Girilen veri okunamadi.")
