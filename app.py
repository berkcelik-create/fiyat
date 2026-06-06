import streamlit as st
import urllib.parse

# Sayfa Ayarları
st.set_page_config(page_title="Akıllı Fiyat Karşılaştırıcı", page_icon="🔍", layout="centered")

st.title("🔍 Akıllı Fiyat Karşılaştırma Asistanı")
st.write("Yapıştırdığınız linkten ürünü analiz eder ve sizi en büyük pazar yerlerindeki canlı sonuçlara yönlendirir.")

# Kullanıcıdan link alma
hedef_link = st.text_input("Ürün Linkini Buraya Yapıştırın:", placeholder="Örn: https://www.hepsiburada.com/...")

def urun_adini_temizle(url):
    try:
        # Linkin son kısmındaki kelimeleri ayıkla
        parcalar = url.split("/")[-1].split("?")[0].split("-")
        # p-1234 gibi id'leri ve anlamsız kısa kelimeleri temizle
        temiz_kelimeler = [k for k in parcalar if len(k) > 2 and not k.startswith("p") and not k.isdigit()]
        if temiz_kelimeler:
            return " ".join(temiz_kelimeler[:4]) # En önemli 4 kelime
        return "Gamer Monitör"
    except:
        return "Gamer Monitör"

if hedef_link:
    # Kelime analizi yap
    arama_kelimesi = urun_adini_temizle(hedef_link)
    st.info(f"📋 Algılanan Ürün: **{arama_kelimesi.upper()}**")
    
    st.subheader("🛍️ Canlı Fiyatları Gör")
    st.write("Aşağıdaki butonlara tıklayarak sitelerdeki en güncel fiyatları bot engeline takılmadan canlı görebilirsiniz:")
    
    # URL kodlama (Boşlukları %20 yapar)
    safe_search = urllib.parse.quote(arama_kelimesi)
    
    # Dinamik Arama Linkleri
    trendyol_url = f"https://www.trendyol.com/sr?q={safe_search}"
    hepsiburada_url = f"https://www.hepsiburada.com/ara?q={safe_search}"
    n11_url = f"https://www.n11.com/arama?q={safe_search}"
    pazarama_url = f"https://www.pazarama.com/arama?q={safe_search}"
    teknosa_url = f"https://www.teknosa.com/arama/?s={safe_search}"
    
    # Görsel butonlar (Yan yana şık durması için sütunlar kullanıyoruz)
    col1, col2 = st.columns(2)
    
    with col1:
        st.link_button("🧡 Trendyol'da Fiyatları Gör", trendyol_url, use_container_width=True)
        st.link_button("💙 Hepsiburada'da Fiyatları Gör", hepsiburada_url, use_container_width=True)
        st.link_button("❤️ N11'de Fiyatları Gör", n11_url, use_container_width=True)
        
    with col2:
        st.link_button("💜 Pazarama'da Fiyatları Gör", pazarama_url, use_container_width=True)
        st.link_button("🔴 Teknosa'da Fiyatları Gör", teknosa_url, use_container_width=True)
        st.link_button("🔍 Akakçe'de Doğrudan Ara", f"https://www.akakce.com/arama/?q={safe_search}", use_container_width=True)

else:
    st.warning("Sistemin çalışması için yukarıdaki kutuya herhangi bir e-ticaret sitesinden ürün linki yapıştırın.")
