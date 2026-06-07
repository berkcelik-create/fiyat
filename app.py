import streamlit as st
import urllib.parse
import re
import requests

st.set_page_config(
    page_title="G-ENGINE // Pro", 
    page_icon="⚡", 
    layout="centered"
)

# Döviz Verisi
def get_dolar_kuru():
    try:
        response = requests.get("https://api.exchangerate-api.com/v4/latest/USD")
        data = response.json()
        return round(data['rates']['TRY'], 2)
    except:
        return "N/A"

dolar = get_dolar_kuru()

st.title("G-ENGINE // Pro")
col1, col2 = st.columns([3, 1])
col1.caption("Global Donanım Arama ve Karar Destek Motoru")
col2.metric("USD/TRY", f"{dolar} ₺")
st.write("---")

st.info(f"Piyasa Notu: Şu an kur {dolar} ₺ seviyesinde.")

arama_turu = st.radio("Arama Modu:", ["Link Analizi", "Model İsmi ile Arama"], horizontal=True)

with st.form("arama_formu"):
    if arama_turu == "Link Analizi":
        girdi_alani = st.text_input("Ürün Linkini Girin:", placeholder="https://www.itopya.com/...")
    else:
        girdi_alani = st.text_input("Ürün Modelini Girin:", placeholder="Örn: PNY RTX 5070")
    arama_tetiklendi = st.form_submit_button("Analiz Et ve Mağazaları Getir", type="primary", use_container_width=True)

def link_temizle_ve_coz(url):
    try:
        url = url.strip().lower()
        if not url.startswith(("http://", "https://")): url = "https://" + url
        parsed_url = urllib.parse.urlparse(urllib.parse.unquote(url))
        ham = re.split(r'[/_\-+.]', parsed_url.path)
        engelli = ["html", "urun", "p", "detay", "ara", "geforce", "oc", "overclock", "v2", "gaming", "rgb", "white", "black", "mouse", "kulaklik"]
        filtrelenmis = [k for k in ham if k and k not in engelli and not (k.startswith('u') and any(c.isdigit() for c in k))]
        return filtrelenmis[:4] if filtrelenmis else ["donanimi"]
    except: return ["donanimi"]

def guvenli_metin_onar(metin):
    return metin.lower().strip().replace("ı", "i").replace("ş", "s").replace("ç", "c").replace("ğ", "g").replace("ü", "u").replace("ö", "o")

if arama_tetiklendi and girdi_alani:
    if arama_turu == "Link Analizi": kelimeler = link_temizle_ve_coz(girdi_alani)
    else: kelimeler = [k.strip() for k in girdi_alani.split() if k.strip()][:4]
    
    temiz_list = [guvenli_metin_onar(k) for k in kelimeler if k.strip()]
    sonuc_model = " ".join(temiz_list).upper()
    st.success(f"Analiz Edilen Model: {sonuc_model}")
    
    # URL Varyasyonları
    normal = urllib.parse.quote(" ".join(temiz_list))
    artili = "+".join(temiz_list)
    yuzdelik = "%20".join(temiz_list)
    incehesap = "%20".join([re.sub(r'rtx(\d+)', r'rtx\1', k) for k in temiz_list])
    
    magazalar = [
        ("Wraith Esports", f"https://wraithesports.com/search?q={normal}"),
        ("İncehesap", f"https://www.incehesap.com/arama/?fiyat_kriteri=1&s={incehesap}"),
        ("İtopya", f"https://www.itopya.com/ara?bul={normal}"),
        ("Sinerji", f"https://www.sinerji.gen.tr/arama?q={artili}"),
        ("Trendyol", f"https://www.trendyol.com/sr?q={normal}"),
        ("Hepsiburada", f"https://www.hepsiburada.com/ara?q={normal}"),
        ("Amazon TR", f"https://www.amazon.com.tr/s?k={normal}"),
        ("Akakçe", f"https://www.akakce.com/arama/?q={normal}")
    ]
    
    st.subheader("Mağaza Seçenekleri")
    col_left, col_right = st.columns(2)
    for i, (ad, url) in enumerate(magazalar):
        if i % 2 == 0: col_left.link_button(ad, url, use_container_width=True)
        else: col_right.link_button(ad, url, use_container_width=True)

    st.write("---")
    st.subheader("Piyasa Araçları")
    c1, c2 = st.columns(2)
    c1.link_button("Döviz Takip", "https://www.bigpara.com/doviz/dolar/")
    c2.link_button("GPU Özellikleri", "https://www.techpowerup.com/gpu-specs/")
