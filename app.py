import streamlit as st
import urllib.parse

# Sayfa Ayarları
st.set_page_config(page_title="Gamer Fiyat Karşılaştırıcı", page_icon="🎮", layout="centered")

st.title("🎮 Oyuncu Ekipmanı & Sistem Karşılaştırıcı")
st.write("Bir ürün linki yapıştırın; Wraith, İtopya, Sinerji, İncehesap ve diğer pazar yerlerindeki canlı sonuçları anında görün!")

# Kullanıcıdan link alma
hedef_link = st.text_input("Ürün Linkini Buraya Yapıştırın:", placeholder="Örn: https://www.itopya.com/... veya herhangi bir link")

def urun_adini_temizle(url):
    try:
        # Linkin sonundaki parametreleri temizle ve kelimeleri ayır
        parcalar = url.split("/")[-1].split("?")[0].split("-")
        # p-1234 gibi id'leri, html uzantılarını ve anlamsız kısa kodları temizle
        temiz_kelimeler = [k.replace(".html", "") for k in parcalar if len(k) > 2 and not k.startswith("p") and not k.isdigit()]
        if temiz_kelimeler:
            return " ".join(temiz_kelimeler[:4]) 
        return "Oyuncu Ekipmanı"
    except:
        return "Oyuncu Ekipmanı"

if hedef_link:
    arama_kelimesi = urun_adini_temizle(hedef_link)
    st.info(f"📋 Algılanan Ürün Arama Kelimesi: **{arama_kelimesi.upper()}**")
    
    st.subheader("🛍️ Sitelerdeki Canlı Sonuçlar")
    st.write("Aşağıdaki butonlara tıklayarak en güncel fiyatlara ve stok durumlarına canlı olarak ulaşabilirsiniz:")
    
    safe_search = urllib.parse.quote(arama_kelimesi)
    
    # 🔥 İSTEDİĞİN ÖZEL GAMING SİTELERİ
    wraith_url = f"https://wraithesports.com/search?q={safe_search}"
    incehesap_url = f"https://www.incehesap.com/arama/?fiyat_kriteri=1&s={safe_search}"
    itopya_url = f"https://www.itopya.com/Arama?q={safe_search}"
    sinerji_url = f"https://www.sinerji.gen.tr/arama?q={safe_search}"
    
    # DİĞER BÜYÜK PAZAR YERLERİ
    trendyol_url = f"https://www.trendyol.com/sr?q={safe_search}"
    hepsiburada_url = f"https://www.hepsiburada.com/ara?q={safe_search}"
    amazon_url = f"https://www.amazon.com.tr/s?k={safe_search}"
    teknosa_url = f"https://www.teknosa.com/arama/?s={safe_search}"
    akakce_url = f"https://www.akakce.com/arama/?q={safe_search}"
    
    # 3 Sütunlu Harika Arayüz Tasarımı
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 👾 Oyuncu Mağazaları")
        st.link_button("🚀 Wraith Esports", wraith_url, use_container_width=True)
        st.link_button("🔥 İncehesap", incehesap_url, use_container_width=True)
        st.link_button("🦎 İtopya", itopya_url, use_container_width=True)
        st.link_button("⚡ Sinerji Bilgisayar", sinerji_url, use_container_width=True)
        
    with col2:
        st.markdown("### 📦 Büyük Pazar Yerleri")
        st.link_button("🧡 Trendyol",
