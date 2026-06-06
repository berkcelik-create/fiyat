import streamlit as st
import urllib.parse

# Sayfa Ayarları ve Premium Tema Dokunuşu
st.set_page_config(
    page_title="GamerFinder // Akıllı Karşılaştırma", 
    page_icon="🎮", 
    layout="centered"
)

# Tarayıcı Hafızasını Başlatma (Geçmiş Aramalar İçin)
if "gecmis" not in st.session_state:
    st.session_state.gecmis = []

# Başlık Bölümü
st.title("🎮 GamerFinder Pro")
st.caption("Oyuncu ekipmanları ve bilgisayar bileşenleri için akıllı yönlendirme motoru v2.0")

# Kullanıcı Rehberi
with st.expander("ℹ️ Sistem Nasıl Çalışır? (Tıkla - Öğren)"):
    st.write("""
    1. Herhangi bir e-ticaret sitesinden beğendiğiniz ürünün **linkini kopyalayın**.
    2. Aşağıdaki kutuya yapıştırın (Sistem ürün modelini otomatik analiz eder).
    3. Açılan butonlara tıklayarak en ucuz fiyatı canlı olarak görün!
    """)

st.write("---")

# Arama Yöntemi Seçimi (Kalite Artırıcı Özellik)
arama_turu = st.radio("Arama Yöntemi Seçin:", ["🔗 Link ile Analiz Et", "⌨️ Ürün Adı ile Doğrudan Ara"], horizontal=True)

arama_kelimesi = ""

if arama_turu == "🔗 Link ile Analiz Et":
    hedef_link = st.text_input("Ürün Linkini Yapıştırın:", placeholder="https://www.itopya.com/...")
    
    # Gelişmiş Kelime Ayıklama Fonksiyonu
    def gelişmiş_kelime_temizle(url):
        try:
            # Gereksiz uzantı ve parametreleri uçur
            url_temiz = url.split("?")[0].split("#")[0]
            parcalar = url_temiz.split("/")[-1].split("-")
            
            # Sitelerin sistem kelimelerini filtrele
            yasakli_kelimeler = {
                "html", "urun", "html", "p", "detay", "fiyat", "ozellikleri", 
                "satinal", "gaming", "oyuncu", "bilgisayar", "store", "product"
            }
            
            temiz = [
                k.replace(".html", "").replace(".txt", "") for k in parcalar 
                if len(k) > 2 and not k.isdigit() and k.lower() not in yasakli_kelimeler
            ]
            
            return " ".join(temiz[:4]) if temiz else "Oyuncu Ekipmanı"
        except:
            return "Oyuncu Ekipmanı"

    if hedef_link:
        arama_kelimesi = gelişmiş_kelime_temizle(hedef_link)

else:
    manuel_isim = st.text_input("Ürün Modelini Yazın:", placeholder="Örn: Razer Deathadder V3 Pro")
    if manuel_isim:
        arama_kelimesi = manuel_isim.strip()

# --- SONUÇLAR VE YÖNLENDİRME BÖLÜMÜ ---
if arama_kelimesi:
    arama_kelimesi_upper = arama_kelimesi.upper()
    st.success(f"🎯 Hedef Ürün Belirlendi: **{arama_kelimesi_upper}**")
    
    # Geçmişe Ekleme Mantığı (Tekrar edenleri engeller, son 4 aramayı tutar)
    if arama_kelimesi_upper not in st.session_state.gecmis:
        st.session_state.gecmis.insert(0, arama_kelimesi_upper)
        st.session_state.gecmis = st.session_state.gecmis[:4]
    
    safe_search = urllib.parse.quote(arama_kelimesi)
    
    # Link Tanımlamaları
    siteler = {
        "👾 Wraith Esports": f"https://wraithesports.com/search?q={safe_search}",
        "🔥 İncehesap": f"https://www.incehesap.com/arama/?fiyat_kriteri=1&s={safe_search}",
        "🦎 İtopya": f"https://www.itopya.com/Arama?q={safe_search}",
        "⚡ Sinerji": f"https://www.sinerji.gen.tr/arama?q={safe_search}",
        "🧡 Trendyol": f"https://www.trendyol.com/sr?q={safe_search}",
        "💙 Hepsiburada": f"https://www.hepsiburada.com/ara?q={safe_search}",
        "💛 Amazon TR": f"https://www.amazon.com.tr/s?k={safe_search}",
        "🔍 Akakçe (Genel)": f"https://www.akakce.com/arama/?q={safe_search}"
    }
    
    st.subheader("🛍️ Mağaza Seçenekleri")
    st.write("Fiyatları ve stokları canlı görmek için mağaza butonuna basın:")
    
    # Butonları ikili şık sütunlara dağıtma
    sol_col, sag_col = st.columns(2)
    liste_siteler = list(siteler.items())
    
    with sol_col:
        for isim, url in liste_siteler[:4]:
            st.link_button(isim, url, use_container_width=True)
            
    with sag_col:
        for isim, url in liste_siteler[4:]:
            st.link_button(isim, url, use_container_width=True)

# --- GEÇMİŞ ARAMALAR BÖLÜMÜ ---
if st.session_state.gecmis:
    st.write("---")
    st.subheader("🕒 Son Arattıklarınız")
    # Küçük yan yana butonlar şeklinde geçmiş
    for gecmis_urun in st.session_state.gecmis:
        st.info(f"🔹 {gecmis_urun}")
