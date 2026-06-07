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
st.caption("Gelişmiş Oyuncu Ekipmanı Arama Motoru v6.1")
st.write("---")

arama_turu = st.radio("Arama Yöntemi:", ["🔗 Link Analizi", "⌨️ Ürün İsim Arama"], horizontal=True)

# Sadece butona basınca araması için form yapısı
with st.form("arama_formu"):
    if arama_turu == "🔗 Link Analizi":
        girdi_alani = st.text_input("Ürün Linkini Yapıştırın:", placeholder="https://www.itopya.com/...")
    else:
        girdi_alani = st.text_input("Ürün Modelini Yazın:", placeholder="Örn: Razer Deathadder V3 Pro")
    
    arama_tetiklendi = st.form_submit_button("🔍 Fiyatları Karşılaştır", type="primary", use_container_width=True)

# Gelişmiş Regex Destekli Kelime Temizleme Fonksiyonu
def gelişmiş_kelime_temizle(url):
    try:
        if not url.startswith("http://") and not url.startswith("https://") and "." not in url:
            return None
            
        url_temiz = url.split("?")[0].split("#")[0]
        parcalar = url_temiz.split("/")[-1].split("-")
        
        yasakli = {"html", "urun", "p", "detay", "fiyat", "ozellikleri", "satinal", "gaming", "oyuncu", "store", "product", "com", "tr"}
        temiz = [k.replace(".html", "") for k in parcalar if len(k) > 2 and not k.isdigit() and k.lower() not in yasakli]
        
        if temiz:
            ham_sonuc = " ".join(temiz[:4])
            temiz_sonuc = re.sub(r'[^a-zA-Z0-9\s]', '', ham_sonuc)
            return temiz_sonuc.strip()
        return "Oyuncu Ekipmanı"
    except:
        return "Oyuncu Ekipmanı"

# Butona basıldıysa işlemleri başlat
if arama_tetiklendi and girdi_alani:
    hata_var = False
    arama_kelimesi = ""
    
    with st.spinner("🔄 Ürün Modeli Analiz Ediliyor..."):
        time.sleep(0.5)
        if arama_turu == "🔗 Link Analizi":
            sonuc = gelişmiş_kelime_temizle(girdi_alani)
            if sonuc is None:
                hata_var = True
            else:
                arama_kelimesi = sonuc
        else:
            arama_kelimesi = girdi_alani.strip()

    if hata_var or not arama_kelimesi:
        st.error("❌ Geçersiz Link Formatı! Lütfen kutuya gerçek bir e-ticaret ürün linki yapıştırın veya 'Ürün İsim Arama' modunu kullanın.")
    else:
        arama_kelimesi_upper = arama_kelimesi.upper()
        st.success(f"🎯 Hedef Ürün Belirlendi: **{arama_kelimesi_upper}**")
        
        # HIZLI KOPYALAMA ALANI
        st.write("📋 Başka yerde aratmak için ismi buradan hızlıca kopyalayabilirsiniz:")
        st.code(arama_kelimesi_upper, language="text")
            
        safe_search = urllib.parse.quote(arama_kelimesi.lower())
        
        # Mağazalar ve En Ucuz Etiketleri
        magazalar = [
            {"ad": "Wraith Esports", "url": f"https://wraithesports.com/search?q={safe_search}", "logo": "🚀", "tag": "⭐ En Ucuz Potansiyeli"},
            {"ad": "İncehesap", "url": f"https://www.incehesap.com/arama/?fiyat_kriteri=1&s={safe_search}", "logo": "🔥", "tag": ""},
            {"ad": "İtopya", "url": f"https://www.itopya.com/Arama?q={safe_search}", "logo": "🦎", "tag": "⭐ En Ucuz Potansiyeli"},
            {"ad": "Sinerji", "url": f"https://www.sinerji.gen.tr/arama?q={safe_search}", "logo": "⚡", "tag": ""},
            {"ad": "Trendyol", "url": f"https://www.trendyol.com/sr?q={safe_search}", "logo": "🧡", "tag": ""},
            {"ad": "Hepsiburada", "url": f"https://www.hepsiburada.com/ara?q={safe_search}", "logo": "💙", "tag": ""},
            {"ad": "Amazon TR", "url": f"https://www.amazon.com.tr/s?k={safe_search}", "logo": "💛", "tag": "⭐ En Ucuz Potansiyeli"},
            {"ad": "Akakçe", "url": f"https://www.akakce.com/arama/?q={safe_search}", "logo": "🔍", "tag": "📊 Genel Karşılaştırma"}
        ]
        
        st.subheader("🛍️ Mağaza Seçenekleri")
        
        sol_col, sag_col = st.columns(2)
        
        for i, m in enumerate(magazalar):
            ek_etiket = f" ({m['tag']})" if m['tag'] else ""
            buton_metni = f"{m['logo']} {m['ad']}{ek_etiket}"
            
            if i % 2 == 0:
                sol_col.link_button(buton_metni, m['url'], use_container_width=True)
            else:
                sag_col.link_button(buton_metni, m['url'], use_container_width=True)
