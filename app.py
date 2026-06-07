import streamlit as st
import urllib.parse
import re
import time

# Sayfa Ayarları ve Sekme Emojisi (Favicon)
st.set_page_config(
    page_title="GamerFinder Pro", 
    page_icon="🎮", 
    layout="centered"
)

# Başlık
st.title("🎮 GamerFinder Pro")
st.caption("Gelişmiş Oyuncu Ekipmanı Arama Motoru v6.0")
st.write("---")

arama_turu = st.radio("Arama Yöntemi:", ["🔗 Link Analizi", "⌨️ Ürün İsim Arama"], horizontal=True)

# Butona basınca araması için form yapısı
with st.form("arama_formu"):
    if arama_turu == "🔗 Link Analizi":
        girdi_alani = st.text_input("Ürün Linkini Yapıştırın:", placeholder="https://www.itopya.com/...")
    else:
        girdi_alani = st.text_input("Ürün Modelini Yazın:", placeholder="Örn: Razer Deathadder V3 Pro")
    
    # Enter yerine arama tetiği olan buton
    arama_tetiklendi = st.form_submit_button("🔍 Fiyatları Karşılaştır", type="primary", use_container_width=True)

# Gelişmiş Regex Destekli Kelime Temizleme Fonksiyonu
def gelişmiş_kelime_temizle(url):
    try:
        # Link kontrolü (Gerçekten bir link mi yoksa düz metin mi?)
        if not url.startswith("http://") and not url.startswith("https://") and "." not in url:
            return None
            
        url_temiz = url.split("?")[0].split("#")[0]
        parcalar = url_temiz.split("/")[-1].split("-")
        
        # Gereksiz sistem kelimeleri filtreleme
        yasakli = {"html", "urun", "p", "detay", "fiyat", "ozellikleri", "satinal", "gaming", "oyuncu", "store", "product", "com", "tr"}
        temiz = [k.replace(".html", "") for k in parcalar if len(k) > 2 and not k.isdigit() and k.lower() not in yasakli]
        
        if temiz:
            ham_sonuc = " ".join(temiz[:4])
            # Regex ile ekstra özel karakterleri temizle (Sadece harf ve sayıları bırak)
            temiz_sonuc = re.sub(r'[^a-zA-Z0-9\s]', '', ham_sonuc)
            return temiz_sonuc.strip()
        return "Oyuncu Ekipmanı"
    except:
        return "Oyuncu Ekipmanı"

# Butona basıldıysa işlemleri başlat
if arama_tetiklendi and girdi_alani:
    # 1. Animasyon Eklemesi: Kısa bir yükleme simülasyonu
    with st.spinner("🔄 Ürün Modeli Analiz Ediliyor..."):
        time.sleep(0.5) # Gerçekçi bir arama hissi için yarım saniye gecikme
        
        hata_var = False
        if arama_turu == "🔗 Link Analizi":
            arama_kelimesi = gelişmiş_kelime_temizle(girdi_alani)
            if arama_kelimesi is None:
                hata_var = True
        else:
            arama_kelimesi = girdi_alani.strip()

    # 2. Hatalı Link Koruması Kontrolü
    if hata_var:
        st.error("❌ Geçersiz Link Formatı! Lütfen kutuya gerçek bir e-ticaret ürün linki yapıştırın veya 'Ürün İsim Arama' modunu kullanın.")
    else:
        arama_kelimesi_upper = arama_kelimesi.upper()
        st.success(f"🎯 Hedef Ürün Belirlendi: **{arama_kelimesi_upper}**")
        
        # HIZLI KOPYALAMA ALANI
        st.write("📋 Başka yerde aratmak için ismi buradan hızlıca kopyalayabilirsiniz:")
        st.code(arama_kelimesi_upper, language="text")
            
        safe_search = urllib.parse.quote(arama_kelimesi)
        
        # Mağazalar ve En Ucuz Etiketleri
        magazalar =
