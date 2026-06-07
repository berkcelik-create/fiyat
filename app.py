import streamlit as st
import urllib.parse
import re

st.set_page_config(
    page_title="G-ENGINE // Hardware Search Engine", 
    page_icon="🔍", 
    layout="centered"
)

st.title("G-ENGINE")
st.caption("Hardware Search Engine // Global Donanım Arama ve Doğrulama Motoru")
st.write("---")

arama_turu = st.radio(
    "Arama Modu:", 
    ["Link Analizi", "Model İsmi ile Arama"], 
    horizontal=True
)

with st.form("arama_formu"):
    if arama_turu == "Link Analizi":
        girdi_alani = st.text_input("Ürün Linkini Girin:", placeholder="https://www.itopya.com/...")
    else:
        girdi_alani = st.text_input("Ürün Modelini Girin:", placeholder="Örn: AMD Ryzen 7 7800X3D")
    arama_tetiklendi = st.form_submit_button("Motoru Çalıştır", type="primary", use_container_width=True)

def link_temizle_ve_kisalt(url):
    try:
        url = url.strip().lower()
        if not url.startswith(("http://", "https://")):
            url = "https://" + url
        cozulmus_url = urllib.parse.unquote(url)
        parsed_url = urllib.parse.urlparse(cozulmus_url)
        link_yolu = parsed_url.path
        ham_kelimeler = re.split(r'[/_\-+.]', link_yolu)
        
        sistem_copleri = ["html", "urun", "p", "detay", "fiyat", "ozellikleri", "satinal", "gaming", "oyuncu", "store", "product", "net", "org", "item", "shop", "bilgisayar", "ara"]
        teknik_copler = ["rgb", "dpi", "hz", "1000hz", "26000", "26000dpi", "mouse", "kulaklik", "klavye", "kablosuz", "wireless", "kablolu", "siyah", "black", "beyaz", "white", "opaline", "gray", "gri", "gaming", "oyuncu", "ses", "kart", "g01", "v01", "m1", "m2", "v60", "aaa", "s", "x", "p"]
        
        filtrelenmis = []
        for k in ham_kelimeler:
            k = k.strip()
            if k.startswith("aaa") and len(k) > 3:
                k = k[3:]
            if len(k) <= 1 or k in sistem_copleri or k in teknik_copler:
                continue
            if k.startswith('u') and any(c.isdigit() for c in k):
                continue
            if k.isdigit() and len(k) <= 4:
                continue
            filtrelenmis.append(k)
            
        if len(filtrelenmis) > 0:
            return filtrelenmis[:3]
            
        yedek_liste = []
        for x in ham_kelimeler:
            x = x.strip()
            if x and (x not in sistem_copleri) and len(x) > 1:
                yedek_liste.append(x)
        return yedek_liste[:3]
    except:
        return ["oyuncu", "donanimi"]

def guvenli_metin_onar(metin):
    metin = metin.lower().strip()
    metin = metin.replace("ı", "i").replace("ş", "s").replace("ç", "c").replace("ğ", "g").replace("ü", "u").replace("ö", "o")
    return metin

if arama_tetiklendi and girdi_alani:
    kelimeler = []
    if arama_turu == "Link Analizi":
        kelimeler = link_temizle_ve_kisalt(girdi_alani)
    else:
        kelimeler = [k.strip() for k in girdi_alani.split() if k.strip()][:3]
        
    temiz_list = [guvenli_metin_onar(k) for k in kelimeler if k.strip()]
    
    if temiz_list:
        sonuc_model = " ".join(temiz_list).upper()
        st.success("Model Basariyla Cozuldu ve Kisaltildi: " + sonuc_model)
        st.write("Kopyalama Alani:")
        st.code(sonuc_model, language="text")
        
        sorgu_cumlesi = " ".join(temiz_list)
        safe_search = urllib.parse.quote(sorgu_cumlesi)
        
        magaza_listesi = [
            {"ad": "Wraith Esports", "url": "https://wraithesports.com/search?q=" + safe_search},
            {"ad": "Incehesap", "url": "https://www.incehesap.com/arama/?fiyat_kriteri=1&s=" + safe_search},
            {"ad": "Itopya", "url": "https://www.itopya.com/ara?bul=" + safe_search},
            {"ad": "Sinerji", "url": "https://www.sinerji.gen.tr/arama?q=" + safe_search},
            {"ad": "Trendyol", "url": "https://www.trendyol.com/sr?q=" + safe_search},
            {"ad": "Hepsiburada", "url": "https://www.hepsiburada.com/ara?q=" + safe_search},
            {"ad": "Amazon TR", "url": "https://www.amazon.com.tr/s?k=" + safe_search},
            {"ad": "Akakce", "url": "https://www.akakce.com/arama/?q=" + safe_search}
        ]
        
        st.subheader("Magaza Secenekleri")
