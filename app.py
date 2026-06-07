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

# 🛠️ TAHMİN BAZLI DEĞİL, KATI KURAL BAZLI DOĞRUDAN MODEL FİLTRESİ
def saf_model_yakala(url):
    try:
        url = urllib.parse.unquote(url).lower()
        
        # Sadece URL'in path (yol) kısmını alarak domain gürültülerini (itopya.com, www vb.) tamamen dışarıda bırakıyoruz
        parsed = urllib.parse.urlparse(url)
        saf_yol = parsed.path if parsed.path else url
        
        # 1. Adım: İşlemci Modeli Yakalama (Örn: 9950x3d, 7800x3d, 12700f, 14900k, 5600x)
        islemci_deseni = re.search(r'(\d{4,5}[xX]?[3-5]?[dD]?|[iI][3579]-\d{4,5}[kKfF]?[sS]?)', saf_yol)
        if islemci_deseni:
            model = islemci_deseni.group(1)
            # İtopya aramalarında tire işaretleri bazen patlatır, temizleyelim
            return [model.replace("-", "")]
            
        # 2. Adım: Eğer işlemci değilse, RAM veya Ekipman ismi için genel temizlik yap
        ham_kelimeler = re.split(r'[/_\-+.]', saf_yol)
        copler = {
            "html", "urun", "p", "detay", "fiyat", "ozellikleri", "satinal", "gaming", 
            "oyuncu", "store", "product", "net", "org", "item", "shop", "bilgisayar",
            "itopya", "vatanbilgisayar", "sinerji", "incehesap", "trendyol", "hepsiburada", "amazon"
        }
        
        filtrelenmis = []
        for k in ham_kelimeler:
            k = k.strip()
            if k and k not in copler and len(k) > 1:
                # Link sonundaki kimlik numaralarını (u3165, 43 vb.) kesin olarak engelle
                if not (k.startswith('u') and any(c.isdigit() for c in k)):
                    if not (k.isdigit() and len(k) <= 4):
                        filtrelenmis.append(k)
                        
        # İtopya'da en yüksek eşleşme oranı için marka hariç en kritik ilk 2 kelimeyi gönderiyoruz
        if filtrelenmis:
            for marka in ["kingston", "asus", "msi", "gigabyte", "corsair", "gskill", "samsung"]:
                if marka in filtrelenmis:
                    filtrelenmis.remove(marka)
            return filtrelenmis[:2]
            
        return ["oyuncu", "donanimi"]
    except:
        return ["oyuncu", "donanimi"]

# Hata Riski Sıfır Olan Karakter Onarıcı
def karakter_duzelt(metin):
    metin = metin.lower().strip()
    metin = metin.replace("ı", "i")
    metin = metin.replace("ş", "s")
    metin = metin.replace("ç", "c")
    metin = metin.replace("ğ", "g")
    metin = metin.replace("ü", "u")
    metin = metin.replace("ö", "o")
    return metin

# Çalışma Senaryosu
if arama_tetiklendi and girdi_alani:
    sonuc_kelimeleri = []
    
    if arama_turu == "Link Analizi":
        sonuc_kelimeleri = saf_model_yakala(girdi_alani)
    else:
        sonuc_kelimeleri = [k.strip() for k in girdi_alani.split() if k.strip()]
        
    temiz_list = [karakter_duzelt(k) for k in sonuc_kelimeleri if k.strip()]
    
    if temiz_list:
        gosterim = " ".join(temiz_list).upper()
        
        st.success("Model Basariyla Cozuldu: " + gosterim)
        st.write("Kopyalama Alani:")
        st.code(gosterim, language="text")
        
        # Web siteleri için arama terimini encode et
        sorgu_cumlesi = " ".join(temiz_list)
        safe_search = urllib.parse.quote(sorgu_cumlesi)
        
        # Mağazalar Listesi (Nokta atışı filtrelenmiş kelimeler gider)
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
        st.error("Analiz Hatasi: Girdi icerisinde gecerli bir model kodu tespit edilemedi.")
