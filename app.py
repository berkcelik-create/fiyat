import streamlit as st
import urllib.parse

# Sayfa Ayarları
st.set_page_config(
    page_title="GamerFinder // Premium", 
    page_icon="🎮", 
    layout="centered"
)

# Tarayıcı Hafızasını Başlatma (Geçmiş Aramalar İçin)
if "gecmis" not in st.session_state:
    st.session_state.gecmis = []

# Başlık Bölümü
st.title("🎮 GamerFinder Pro")
st.caption("Oyuncu ekipmanları ve bilgisayar bileşenleri için akıllı yönlendirme motoru v3.1")

st.write("---")

# Arama Yöntemi Seçimi
arama_turu = st.radio("Arama Yöntemi Seçin:", ["🔗 Link ile Analiz Et", "⌨️ Ürün Adı ile Doğrudan Ara"], horizontal=True)

arama_kelimesi = ""

if arama_turu == "🔗 Link ile Analiz Et":
    hedef_link = st.text_input("Ürün Linkini Yapıştırın:", placeholder="https://www.itopya.com/...")
    
    def gelişmiş_kelime_temizle(url):
        try:
            url_temiz = url.split("?")[0].split("#")[0]
            parcalar = url_temiz.split("/")[-1].split("-")
            yasakli_kelimeler = {
                "html", "urun", "p", "detay", "fiyat", "ozellikleri", 
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

# --- SONUÇLAR VE LOGOLU MAĞAZALAR BÖLÜMÜ ---
if arama_kelimesi:
    arama_kelimesi_upper = arama_kelimesi.upper()
    st.success(f"🎯 Hedef Ürün Belirlendi: **{arama_kelimesi_upper}**")
    
    if arama_kelimesi_upper not in st.session_state.gecmis:
        st.session_state.gecmis.insert(0, arama_kelimesi_upper)
        st.session_state.gecmis = st.session_state.gecmis[:4]
    
    safe_search = urllib.parse.quote(arama_kelimesi)
    
    # Mağazaların Listesi (Parantez hataları giderilmiş net veri yapısı)
    magazalar = [
        {"ad": "Wraith Esports", "url": f"https://wraithesports.com/search?q={safe_search}", "logo": "🚀"},
        {"ad": "İncehesap", "url": f"https://www.incehesap.com/arama/?fiyat_kriteri=1&s={safe_search}", "logo": "🔥"},
        {"ad": "İtopya", "url": f"https://www.itopya.com/Arama?q={safe_search}", "logo": "🦎"},
        {"ad": "Sinerji", "url": f"https://www.sinerji.gen.tr/arama?q={safe_search}", "logo": "⚡"},
        {"ad": "Trendyol", "url": f"https://www.trendyol.com/sr?q={safe_search}", "logo": "🧡"},
        {"ad": "Hepsiburada", "url": f"https://www.hepsiburada.com/ara?q={safe_search}", "logo": "💙"},
        {"ad": "Amazon TR", "url": f"https://www.amazon.com.tr/s?k={safe_search}", "logo": "💛"},
        {"ad": "Akakçe", "url": f"https://www.akakce.com/arama/?q={safe_search}", "logo": "🔍"}
    ]
    
    st.subheader("🛍️ Mağaza Seçenekleri")
    st.write("Canlı arama sonuçlarını yeni sekmede görmek için tıklayın:")
    
    # İki sütunlu şık düzen
    sol_col, sag_col = st.columns(2)
    
    for i, m in enumerate(magazalar):
        buton_metni = f"{m['logo']} {m['ad']}"
        if i % 2 == 0:
            sol_col.link_button(buton_metni, m['url'], use_container_width=True)
        else:
            sag_col.link_button(buton_metni, m['url'], use_container_width=True)

# --- GEÇMİŞ ARAMALAR BÖLÜMÜ ---
if st.session_state.gecmis:
    st.write("---")
    st.subheader("🕒 Son Arattıklarınız")
    for gecmis_urun in
