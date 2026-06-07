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

# 🛠️ GELİŞMİŞ GÜRÜLTÜ ARNDIRICI VE LINK ÇÖZÜCÜ
def link_temizle_ve_coz(url):
    try:
        url = url.strip().lower()
        if not url.startswith(("http://", "https://")):
            url = "https://" + url
            
        cozulmus_url = urllib.parse.unquote(url)
        parsed_url = urllib.parse.urlparse(cozulmus_url)
        
        # Sadece path (yol) kısmını alarak domain adını tamamen dışarıda bırakıyoruz
        link_yolu = parsed_url.path
        ham_kelimeler = re.split(r'[/_\-+.]', link_yolu)
        
        # Web sitelerinin teknik link uzantıları ve sistem çöpleri
        kesin_copler = {
            "html", "urun", "p", "detay", "fiyat", "ozellikleri", "satinal", "gaming", 
            "oyuncu", "store", "product", "net", "org", "item", "shop", "bilgisayar", "ara"
        }
        
        filtrelenmis = []
        for k in ham_kelimeler:
            k = k.strip()
            
            # Sinerji veya benzeri yerlerdeki 'aaa' gibi yapay gürültüleri temizle
            if k.startswith("aaa") and len(k) > 3:
                k = k[3:]
                
            # Kelime boş değilse, çöp listesinde değilse ve uzunluğu 1'den büyükse koru
            if k and k not in kesin_copler and len(k) > 1:
                # Link sonundaki otomatik ID'leri (u3165 vb.) ve kısa anlamsız sayıları eliyoruz
                if not (k.startswith('u') and any(c.isdigit() for c in k)):
                    if not (k.isdigit() and len(k) <= 3):
                        # Tek başına kalan 's' veya benzeri harf çöplerini engelle
                        if k not in ["s", "x", "p"]:
                            filtrelenmis.append(k)
        
        if filtrelenmis:
            return filtrelenmis
            
        return ["oyuncu", "donanimi"]
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
        kelimeler = link_temizle_ve_coz(girdi_alani)
    else:
        kelimeler = [k.strip() for k in girdi_alani.split() if k.strip()]
        
    temiz_list = [guvenli_metin_onar(k) for k in kelimeler if k.strip()]
    
    if temiz_list:
        sonuc_model = " ".join(temiz_list).upper()
        
        st.success("Model Basariyla Cozuldu: " + sonuc_model)
        st.write("Kopyalama Alani:")
        st.code(sonuc_model, language="text")
        
        # Arama motorlarının kabul edeceği güvenli URL formatı
        sorgu_cumlesi = " ".join(temiz_list)
        safe_search = urllib.parse.quote(sorgu_cumlesi)
        
        # Test Edilmiş ve Doğrulanmış Mağazalar Listesi
        magaza_listesi = [
            {"ad": "Wraith Esports", "url": f"https://wraithesports.com/search?q={safe_search}"},
            {"ad": "Incehesap", "url": f"https://www.incehesap.com/arama/?fiyat_kriteri=1&s={safe_search}"},
            {"ad": "Itopya", "url": f"https://www.itopya.com/ara?bul={safe_search}"},
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
        st.error("Analiz Hatasi: Gecersiz girdi.")
