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

# 🛠️ GEREKSİZ TEKNİK DETAYLARI SÜZEN GELİŞMİŞ FİLTRE MOTORU
def link_temizle_ve_kisalt(url):
    try:
        url = url.strip().lower()
        if not url.startswith(("http://", "https://")):
            url = "https://" + url
            
        cozulmus_url = urllib.parse.unquote(url)
        parsed_url = urllib.parse.urlparse(cozulmus_url)
        
        # Sadece path kısmını alarak domain gürültülerini engelliyoruz
        link_yolu = parsed_url.path
        ham_kelimeler = re.split(r'[/_\-+.]', link_yolu)
        
        # 1. Aşama: URL ve sistem çöpleri
        sistem_copleri = {
            "html", "urun", "p", "detay", "fiyat", "ozellikleri", "satinal", "gaming", 
            "oyuncu", "store", "product", "net", "org", "item", "shop", "bilgisayar", "ara"
        }
        
        # 2. Aşama: Aramayı bozan upuzun teknik kelime çöpleri (DPI, HZ, Renkler vb.)
        teknik_copler = {
            "rgb", "dpi", "hz", "1000hz", "26000", "26000dpi", "mouse", "kulaklik", 
            "klavye", "kablosuz", "wireless", "kablolu", "siyah", "black", "beyaz", 
            "white", "opaline", "gray", "gri", "gaming", "oyuncu", "ses", "kart", 
            "g01", "v01", "m1", "m2", "v60", "aaa", "s", "x", "p"
        }
        
        filtrelenmis = []
        for k in ham_kelimeler:
            k = k.strip()
            
            # 'aaa' gibi sinerji gürültülerini baştan kırp
            if k.startswith("aaa") and len(k) > 3:
                k = k[3:]
                
            if k and (k not in sistem_copleri) and (k not in teknik_copler) and len(k) > 1:
                # Otomatik basılan u32084 gibi kodları eliyoruz
                if not (k.startswith('u') and any(c.isdigit() for c in k)):
                    if not (k.isdigit() and len(k) <= 4):
                        filtrelenmis.append(k)
        
        # Eğer filtreleme çok sert olduysa ve kelime kalmadıysa, teknik çöplerin ilk 3'ünü geri yükle
        if not filtrelenmis:
            gecici = [k for k in ham_kelimeler if k and k not in sistem_copleri and len(k) > 1]
            return gecici[:3]
            
        # Mağazalarda en iyi arama sonucu için temizlenmiş ilk 3 anahtar kelimeyi döndür
        return filtrelenmis[:3]
    except:
        return ["oyuncu", "donanimi"]

# Güvenli Karakter Onarıcı
def guvenli_metin_onar(metin):
    metin = metin.lower().strip()
    metin = metin.replace("ı", "i")
    metin = metin.replace("ş", "s")
    metin = metin.replace("ç", "c")
    metin = metin.replace("ğ", "g")
    metin = metin.replace("ü", "u")
    metin = metin.replace("ö", "o")
    return metin

# Ana Çalışma Mantığı
if arama_tetiklendi and girdi_alani:
    kelimeler = []
    
    if arama_turu == "Link Analizi":
        kelimeler = link_temizle_ve_kisalt(girdi_alani)
    else:
        # Manuel aramalarda kullanıcının yazdığı ilk 3 kelimeyi baz alarak kısaltma yapıyoruz
        kelimeler = [k.strip() for k in girdi_alani.split() if k.strip()][:3]
        
    temiz_list = [guvenli_metin_onar(k) for k in kelimeler if k.strip()]
    
    if temiz_list:
        sonuc_model = " ".join(temiz_list).upper()
        
        st.success("Model Basariyla Cozuldu ve Kisaltildi: " + sonuc_model)
        st.write("Kopyalama Alani:")
        st.code(sonuc_model, language="text")
        
        # URL Formatlama
        sorgu_cumlesi = " ".join(temiz_list)
        safe_search = urllib.parse.quote(sorgu_cumlesi)
        
        # Doğrulanmış Mağazalar Listesi
        magaza_listesi =
