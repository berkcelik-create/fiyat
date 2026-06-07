import streamlit as st
import urllib.parse

# Sayfa Ayarları
st.set_page_config(
    page_title="GamerFinder Pro", 
    page_icon="🎮", 
    layout="centered"
)

# Başlık
st.title("🎮 GamerFinder Pro")
st.caption("Gelişmiş Oyuncu Ekipmanı Arama Motoru")
st.write("---")

arama_turu = st.radio("Arama Yöntemi:", ["🔗 Link Analizi", "⌨️ Ürün İsim Arama"], horizontal=True)

# Sadece butona basınca araması için form yapısı (Enter'a basınca tetiklenmez)
with st.form("arama_formu"):
    if arama_turu == "🔗 Link Analizi":
        girdi_alani = st.text_input("Ürün Linkini Yapıştırın:", placeholder="https://www.itopya.com/...")
    else:
        girdi_alani = st.text_input("Ürün Modelini Yazın:", placeholder="Örn: Razer Deathadder V3 Pro")
    
    # Arama tetiği olan tek buton
    arama_tetiklendi = st.form_submit_button("🔍 Fiyatları Karşılaştır", type="primary", use_container_width=True)

# Kelime temizleme fonksiyonu
def kelime_temizle(url):
    try:
        url_temiz = url.split("?")[0].split("#")[0]
        parcalar = url_temiz.split("/")[-1].split("-")
        yasakli = {"html", "urun", "p", "detay", "fiyat", "ozellikleri", "satinal", "gaming", "oyuncu", "store", "product"}
        temiz = [k.replace(".html", "") for k in parcalar if len(k) > 2 and not k.isdigit() and k.lower() not in yasakli]
        return " ".join(temiz[:4]) if temiz else "Oyuncu Ekipmanı"
    except:
        return "Oyuncu Ekipmanı"

# Butona basıldıysa işlemleri başlat
if arama_tetiklendi and girdi_alani:
    if arama_turu == "🔗 Link Analizi":
        arama_kelimesi = kelime_temizle(girdi_alani)
    else:
        arama_kelimesi = girdi_alani.strip()
        
    arama_kelimesi_upper = arama_kelimesi.upper()
    st.success(f"🎯 Hedef Ürün Belirlendi: **{arama_kelimesi_upper}**")
    
    # HIZLI KOPYALAMA ALANI
    st.write("📋 Başka yerde aratmak için ismi buradan hızlıca kopyalayabilirsiniz:")
    st.code(arama_kelimesi_upper, language="text")
        
    safe_search = urllib.parse.quote(arama_kelimesi)
    
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
