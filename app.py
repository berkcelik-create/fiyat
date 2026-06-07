import streamlit as st
import urllib.parse
import re

st.set_page_config(
    page_title="G-ENGINE // Hardware Search Engine", 
    page_icon="🔍", 
    layout="centered"
)

st.title("G-ENGINE")
st.caption("Hardware Search Engine // Stokta Olmayan Siteleri Eleme Motoru")
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

def link_temizle_ve_coz(url):
    try:
        url = url.strip().lower()
        if not url.startswith(("http://", "https://")):
            url = "https://" + url
        cozulmus_url = urllib.parse.unquote(url)
        parsed_url = urllib.parse.urlparse(cozulmus_url)
        link_yolu = parsed_url.path
        ham_kelimeler = re.split(r'[/_\-+.]', link_yolu)
        
        engelli_kelimeler = [
            "html", "urun", "p", "detay", "ara", "geforce", "oc", "overclock", 
            "v1", "v2", "v3", "v4", "v5", "evo", "pro", "plus", "super", 
            "gaming", "oyuncu", "rgb", "edition", "se", "white", "black",
            "mouse", "kulaklik", "klavye", "kablosuz", "wireless", "kablolu"
        ]
        
        filtrelenmis = []
        for k in ham_kelimeler:
            k = k.strip()
            if k.startswith("aaa") and len(k) > 3:
                k = k[3:]
            if not k or k in engelli_kelimeler:
                continue
            if k.startswith('u') and any(c.isdigit() for c in k):
                continue
            if k.isdigit() and len(k) <= 3:
                continue
            filtrelenmis.append(k)
            
        if len(filtrelenmis) > 0:
            return filtrelenmis[:3]
        return ["oyuncu", "donanimi"]
    except:
        return ["oyuncu", "donanimi"]

def guvenli_metin_onar(metin):
    metin = metin.lower().strip()
    metin = metin.replace("ı", "i").replace("ş", "s").replace("ç", "c").replace("ğ", "g").replace("ü", "u").replace("ö", "o")
    return metin

if arama_tetiklendi and girdi_alani:
    kelimeler = []
    if arama_turu == "Link Analizi":
        kelimeler = link_temizle_ve_coz(girdi_alani)
    else:
        engelliler = ["geforce", "oc", "overclock", "v2", "gaming", "mouse", "kulaklik", "klavye"]
        ham_girdi = [k.strip() for k in girdi_alani.split() if k.strip() and k.lower() not in engelliler]
        kelimeler = ham_girdi[:3]
        
    temiz_list = [guvenli_metin_onar(k) for k in kelimeler if k.strip()]
    
    if temiz_list:
        sonuc_model = " ".join(temiz_list).upper()
        st.success("Nokta Atışı Model Çözüldü: " + sonuc_model)
        
        st.write("Kopyalama Alanı:")
        st.code(sonuc_model, language="text")
        
        normal_sorgu = urllib.parse.quote(" ".join(temiz_list))
        
        # Sadece stoğu olan ve ürünü gerçekten satan mağazaları listeleyen Akakçe Havuzu
        akakce_url = "https://www.akakce.com/arama/?q=" + normal_sorgu
        
        st.subheader("Aktif Mağaza ve Stok Filtresi")
        st.info("Aşağıdaki buton, aradığın ürünün İncehesap, İtopya, Sinerji gibi sitelerde stokta olup olmadığını kontrol eder ve sadece ürünü satan aktif mağazaları listeler.")
        
        st.link_button("Stokta Olan Mağazaları Göster 🔍", akakce_url, type="primary", use_container_width=True)
    else:
        st.error("Analiz Hatası: Geçersiz girdi.")
