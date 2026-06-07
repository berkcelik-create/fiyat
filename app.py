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

def link_temizle_ve_coz(url):
    try:
        url = url.strip().lower()
        if not url.startswith(("http://", "https://")):
            url = "https://" + url
        cozulmus_url = urllib.parse.unquote(url)
        parsed_url = urllib.parse.urlparse(cozulmus_url)
        link_yolu = parsed_url.path
        ham_kelimeler = re.split(r'[/_\-+.]', link_yolu)
        
        # Arama sonuçlarını bozan agresif/ekstra teknik kelimeleri eliyoruz
        engelli_kelimeler = [
            "html", "urun", "p", "detay", "ara", "geforce", "oc", "overclock", 
            "v1", "v2", "v3", "v4", "v5", "evo", "pro", "plus", "super", 
            "gaming", "oyuncu", "rgb", "edition", "se", "white", "black"
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
            return filtrelenmis[:4]
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
        # Manuel aramalarda da 'geforce', 'oc' gibi kelimeleri eliyoruz
        engelliler = ["geforce", "oc", "overclock", "v2", "gaming"]
        ham_girdi = [k.strip() for k in girdi_alani.split() if k.strip() and k.lower() not in engelliler]
        kelimeler = ham_girdi[:4]
        
    temiz_list = [guvenli_metin_onar(k) for k in kelimeler if k.strip()]
    
    if temiz_list:
        sonuc_model = " ".join(temiz_list).upper()
        st.success("Model Basariyla Cozuldu: " + sonuc_model)
        st.write("Kopyalama Alani:")
        st.code(sonuc_model, language="text")
        
        artili_sorgu = "+".join(temiz_list)
        yuzdelik_sorgu = "%20".join(temiz_list)
        normal_sorgu = urllib.parse.quote(" ".join(temiz_list))
        
        # İncehesap'ın rtx ve 5070'i ayrı veya birleşik bulabilmesi için akıllı birleştirme
        incehesap_list = []
        for i, kelime in enumerate(temiz_list):
            if kelime == "rtx" and i + 1 < len(temiz_list) and temiz_list[i+1].isdigit():
                incehesap_list.append("rtx" + temiz_list[i+1])
            elif kelime.isdigit() and i - 1 >= 0 and temiz_list[i-1] == "rtx":
                continue
            else:
                incehesap_list.append(kelime)
        incehesap_sorgu = "%20".join(incehesap_list)
        
        magaza_listesi = [
            {"ad": "Wraith Esports", "url": "https://wraithesports.com/search?q=" + normal_sorgu},
            {"ad": "Incehesap", "url": "https://www.incehesap.com/arama/?fiyat_kriteri=1&s=" + incehesap_sorgu},
            {"ad": "Itopya", "url": "https://www.itopya.com/ara?bul=" + normal_sorgu},
            {"ad": "Sinerji", "url": "https://www.sinerji.gen.tr/arama?q=" + artili_sorgu},
            {"ad": "Trendyol", "url": "https://www.trendyol.com/sr?q=" + normal_sorgu},
            {"ad": "Hepsiburada", "url": "https://www.hepsiburada.com/ara?q=" + normal_sorgu},
            {"ad": "Amazon TR", "url": "https://www.amazon.com.tr/s?k=" + normal_sorgu},
            {"ad": "Akakce", "url": "https://www.akakce.com/arama/?q=" + normal_sorgu}
        ]
        
        st.subheader("Magaza Secenekleri")
        sol_sutun, sag_sutun = st.columns(2)
        
        for sira, veri in enumerate(magaza_listesi):
            if sira % 2 == 0:
                sol_sutun.link_button(veri["ad"], veri["url"], use_container_width=True)
            else:
                sag_sutun.link_button(veri["ad"], veri["url"], use_container_width=True)
    else:
        st.error("Analiz Hatasi: Gecersiz girdi.")
