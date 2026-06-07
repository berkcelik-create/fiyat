import streamlit as st
import urllib.parse
import re

# --- Sayfa Yapılandırması ---
st.set_page_config(
    page_title="G-ENGINE // Hardware Search Engine", 
    page_icon="🔍", 
    layout="centered"
)

# --- Yan Menü ---
st.sidebar.title("👤 İletişim")
st.sidebar.info("G-ENGINE geliştiricisi ile iletişime geçmek için:")
st.sidebar.link_button("Discord Profilim", "https://discord.com/users/714481744295886990", use_container_width=True)
st.sidebar.write("---")
st.sidebar.caption("G-ENGINE v1.0 // Hardware Search")

# --- Ana Sayfa ---
st.title("G-ENGINE")
st.caption("Hardware Search Engine // Orijinal Arama Motoru")
st.write("---")

# --- Kullanım Kılavuzu (Eklendi) ---
with st.expander("ℹ️ G-ENGINE Nasıl Kullanılır?"):
    st.write("""
    G-ENGINE, donanım arayışlarınızı hızlandırmak için tasarlandı:
    1. **Arama Modunu Seçin:** Link üzerinden mi yoksa model ismi yazarak mı arama yapmak istediğinizi seçin.
    2. **Veriyi Girin:** - *Link Analizi:* Mağazadan kopyaladığınız ürün linkini yapıştırın, motor linki temizleyip arama terimlerini otomatik çıkarsın.
       - *Model İsmi:* Doğrudan aradığınız donanımı yazın (Örn: RTX 4070).
    3. **Motoru Çalıştır:** Butona bastığınızda seçili tüm mağazalarda otomatik arama sayfaları açılacaktır.
    """)

arama_turu = st.radio(
    "Arama Modu:", 
    ["Link Analizi", "Model İsmi ile Arama"], 
    horizontal=True
)

with st.form("arama_formu"):
    if arama_turu == "Link Analizi":
        girdi_alani = st.text_input("Ürün Linkini Girin:", placeholder="https://www.itopya.com/...")
    else:
        girdi_alani = st.text_input("Ürün Modelini Girin:", placeholder="Örn: PNY RTX 5070")
    arama_tetiklendi = st.form_submit_button("Motoru Çalıştır", type="primary", use_container_width=True)

# --- Fonksiyonlar ---
def link_temizle_ve_coz(url):
    try:
        url = url.strip().lower()
        if not url.startswith(("http://", "https://")): url = "https://" + url
        parsed_url = urllib.parse.urlparse(urllib.parse.unquote(url))
        ham = re.split(r'[/_\-+.]', parsed_url.path)
        
        engelli = ["html", "urun", "p", "detay", "ara", "geforce", "oc", "overclock", "v2", "gaming", "rgb", "white", "black", "mouse", "kulaklik"]
        filtrelenmis = [k for k in ham if k and k not in engelli and not (k.startswith('u') and any(c.isdigit() for c in k)) and not (k.isdigit() and len(k) <= 3)]
        return filtrelenmis[:4] if filtrelenmis else ["donanimi"]
    except: return ["donanimi"]

def guvenli_metin_onar(metin):
    return metin.lower().strip().replace("ı", "i").replace("ş", "s").replace("ç", "c").replace("ğ", "g").replace("ü", "u").replace("ö", "o")

# --- İşlem ---
if arama_tetiklendi and girdi_alani:
    if arama_turu == "Link Analizi": 
        kelimeler = link_temizle_ve_coz(girdi_alani)
    else: 
        kelimeler = [k.strip() for k in girdi_alani.split() if k.strip()][:4]
    
    temiz_list = [guvenli_metin_onar(k) for k in kelimeler if k.strip()]
    sonuc_model = " ".join(temiz_list).upper()
    
    st.success("Model Basariyla Cozuldu: " + sonuc_model)
    
    normal = urllib.parse.quote(" ".join(temiz_list))
    artili = "+".join(temiz_list)
    incehesap = "%20".join(temiz_list)
    
    magazalar = [
        ("Wraith Esports", f"https://wraithesports.com/search?q={normal}"),
        ("İncehesap",
