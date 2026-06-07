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

# 🧠 NOKTA ATIŞI DOMAIN VE PROTOKOL TEMİZLEME MOTORU
def link_temizle_ve_coz(url):
    try:
        url = url.strip().lower()
        if not url.startswith(("http://", "https://")):
            url = "https://" + url
            
        cozulmus_url = urllib.parse.unquote(url)
        parsed_url = urllib.parse.urlparse(cozulmus_url)
        
        # netloc (domain) ve path kısımlarını tamamen ayırarak analiz ediyoruz
        ham_metin = parsed_url.netloc + parsed_url.path
        ham_kelimeler = re.split(r'[/_\-+.]', ham_metin)
        
        # Arama terimini kirleten tüm web ve domain takıları
        kesin_copler = {
            "http", "https", "www", "itopya", "com", "tr", "html", "urun", "p", 
            "detay", "fiyat", "ozellikleri", "satinal", "gaming", "oyuncu", "store", 
            "product", "net", "org", "item", "shop", "bilgisayar", "vatanbilgisayar",
            "sinerji", "incehesap", "trendyol", "hepsiburada", "amazon", "wraithesports"
        }
        
        filtrelenmis = []
        for k in ham_kelimeler:
            k = k.strip()
            if k and k not in kesin_copler and len(k) > 1:
                # Link sonuna eklenen otomatik ID ve kısa sayı çöplerini eliyoruz
                if not (k.startswith('u') and any(c.isdigit() for c in k)):
                    if not (k.isdigit() and len(k) <= 4):
                        filtrelenmis.append(k)

        # Bilinen donanım markalarını tespit edip önceliklendirme
        markalar = {"amd", "intel", "kingston", "asus", "msi", "gigabyte", "corsair", "gskill", "samsung", "crucial"}
        
        for i, kelime in enumerate(filtrelenmis):
            if kelime in markalar:
                # Markadan başlayarak en kritik model verilerini paketle
                return filtrelenmis[i:i+4]
                
        if filtrelenmis:
            return filtrelenmis[:3]
            
        return ["oyuncu", "ekipmani"]
    except:
        return ["oyuncu", "ekipmani"]

# Karakter Onarıcı
def guvenli_metin_onar(metin):
    metin = metin.lower().strip()
    metin = metin.replace("ı", "i")
    metin = metin.replace("ş", "s")
    metin = metin.replace("ç", "c")
    metin = metin.replace("ğ", "g")
    metin = metin.replace("ü", "u")
    metin = metin.replace("ö", "o")
    return metin

# Ana Çalışma Bloğu
if arama_tetiklendi and girdi_alani:
    kelimeler = []
    
    if arama_turu == "Link Analizi":
        kelimeler = link_temizle_ve_coz(girdi_alani)
    else:
        kelimeler = [k.strip() for k in girdi_alani.split() if k.strip()]
        
    temiz_list = [guvenli_metin_onar(k) for k in kelimeler if k.strip()]
    
    if temiz_list:
        sonuc_model = " ".join(temiz_list).upper()
        
        st.success("Model Basariyla Cozuldu: " + sonuc_model)
        st.write("Kopyalama Alani:")
        st.code(sonuc_model, language="text")
        
        # URL Standartlaştırma (Aralarında düzgünce boşluk olan en kararlı arama biçimi)
        sorgu_cumlesi = " ".join(temiz_list)
        safe_search = urllib.parse.quote(sorgu_cumlesi)
        
        # Mağazalar Listesi
        magaza_listesi =
