import streamlit as st
import urllib.parse

st.set_page_config(page_title="Gamer Fiyat", page_icon="🎮", layout="centered")
st.title("🎮 Oyuncu Ekipmanı & Sistem Karşılaştırıcı")
st.write("Link yapıştırın; Wraith, İtopya, Sinerji ve diğer pazar yerlerindeki canlı sonuçları görün!")

hedef_link = st.text_input("Ürün Linkini Buraya Yapıştırın:", placeholder="Link giriniz...")

def urun_adini_temizle(url):
    try:
        parcalar = url.split("/")[-1].split("?")[0].split("-")
        temiz = [k.replace(".html", "") for k in parcalar if len(k) > 2 and not k.startswith("p") and not k.isdigit()]
        return " ".join(temiz[:4]) if temiz else "Oyuncu Ekipmanı"
    except:
        return "Oyuncu Ekipmanı"

if hedef_link:
    arama_kelimesi = urun_adini_temizle(hedef_link)
    st.info(f"📋 Algılanan Ürün: **{arama_kelimesi.upper()}**")
    
    safe_search = urllib.parse.quote(arama_kelimesi)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 👾 Oyuncu Mağazaları")
        st.link_button("🚀 Wraith Esports", f"https://wraithesports.com/search?q={safe_search}", use_container_width=True)
        st.link_button("🔥 Incehesap", f"https://www.incehesap.com/arama/?fiyat_kriteri=1&s={safe_search}", use_container_width=True)
        st.link_button("🦎 Itopya", f"https://www.itopya.com/Arama?q={safe_search}", use_container_width=True)
        st.link_button("⚡ Sinerji", f"https://www.sinerji.gen.tr/arama?q={safe_search}", use_container_width=True)
        
    with col2:
        st.markdown("### 📦 Büyük Siteler")
        st.link_button("🧡 Trendyol", f"https://www.trendyol.com/sr?q={safe_search}", use_container_width=True)
        st.link_button("💙 Hepsiburada", f"https://www.hepsiburada.com/ara?q={safe_search}", use_container_width=True)
        st.link_button("💛 Amazon TR", f"https://www.amazon.com.tr/s?k={safe_search}", use_container_width=True)
        st.link_button("🔍 Akakçe", f"https://www.akakce.com/arama/?q={safe_search}", use_container_width=True)
else:
    st.warning("Lütfen bir ürün linki yapıştırın.")
