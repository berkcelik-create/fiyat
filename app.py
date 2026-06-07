import streamlit as st
import urllib.parse
import re
import time

# Sayfa Ayarları ve Sekme Emojisi
st.set_page_config(
    page_title="G-Engine", 
    page_icon="🎮", 
    layout="centered"
)

# Başlık
st.title("🎮 G-Engine")
st.caption("Gelişmiş Oyuncu Ekipmanı Arama Motoru v7.5")
st.write("---")

arama_turu = st.radio("Arama Yöntemi:", ["🔗 Link Analizi", "⌨️ Ürün İsim Arama"], horizontal=True)

# Form Yapısı
with st.form("arama_formu"):
    if arama_turu == "🔗 Link Analizi":
        girdi_alani = st.text_input("Ürün Linkini Yapıştırın:", placeholder="https://www.itopya.com/...")
    else:
        girdi_alani = st.text_input("Ürün Modelini Yazın:", placeholder="Örn: Razer Deathadder V3 Pro")
    
    arama_tetiklendi = st.form_submit_button("🔍 Fiyatları Karşılaştır", type="primary", use_container_width=True)

# Gelişmiş Kelime Temizleme Fonksiyonu
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

# Türkçe Karakter ve Akıllı Boşluk Toleransı
def akilli_metin_duzelt(metin):
    metin = " ".join(metin.split())
    donusum = {"İ": "I", "ı": "i", "Ş": "S", "ş": "s", "Ç": "C", "ç": "c", "Ğ": "G", "ğ": "g", "Ü": "U", "ü": "u", "Ö": "O", "ö": "o"}
    for kaynak, hedef in donusum.items():
        metin = metin.replace(kaynak, hedef)
    return metin

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
            arama_kelimesi = girdi_alani
            
    if arama_kelimesi:
        arama_kelimesi = akilli_metin_duzelt(arama_kelimesi)

    if hata_var or not arama_kelimesi or len(arama_kelimesi) < 2:
        st.error("❌ Geçersiz Girdi! Lütfen geçerli bir ürün adı veya doğru bir e-ticaret linki girin.")
    else:
        arama_kelimesi_upper = arama_kelimesi.upper()
        st.success(f"🎯 Hedef Ürün Belirlendi: **{arama_kelimesi_upper}**")
        
        # HIZLI KOPYALAMA ALANI
        st.write("📋 Başka yerde aratmak için ismi buradan hızlıca kopyalayabilirsiniz:")
        st.code(arama_kelimesi_upper, language="text")
            
        safe_search = urllib.parse.quote(arama_kelimesi.lower())
        
        # --- 🚫 DİNAMİK GİZLEME ALTYAPISI ---
        # Donanım kelimeleri aratılıyorsa Wraith listeye hiç eklenmeyecek
        donanim_kelimeleri = ["ekran karti", "islemci", "anakart", "ram", "ssd", "power", "psu", "kasa", "gpu", "cpu", "sivi sogutma", "fan"]
        is_donanim = any(x in arama_kelimesi.lower() for x in donanim_kelimeleri)
        
        # Ham mağaza listesi
        tum_magazalar = [
            {"ad": "Wraith Esports", "url": f"https://wraithesports.com/search?q={safe_search}", "logo": "🚀", "tag": "⭐ En Ucuz Potansiyeli", "tip": "ekipman"},
            {"ad": "İncehesap", "url": f"https://www.incehesap.com/arama/?fiyat_kriteri=1&s={safe_search}", "logo": "🔥", "tag": "", "tip": "hepsi"},
            {"ad": "İtopya", "url": f"https://www.itopya.com/Arama?q={safe_search}", "logo": "🦎", "tag": "⭐ En Ucuz Potansiyeli", "tip": "hepsi"},
            {"ad": "Sinerji", "url": f"https://www.sinerji.gen.tr/arama?q={safe_search}", "logo": "⚡", "tag": "", "tip": "hepsi"},
            {"ad": "Trendyol", "url": f"https://www.trendyol.com/sr?q={safe_search}", "logo": "🧡", "tag": "", "tip": "hepsi"},
            {"ad": "Hepsiburada", "url": f"https://www.hepsiburada.com/ara?q={safe_search}", "logo": "💙", "tag": "", "tip": "hepsi"},
            {"ad": "Amazon TR", "url": f"https://www.amazon.com.tr/s?k={safe_search}", "logo": "💛", "tag": "⭐ En Ucuz Potansiyeli", "tip": "hepsi"},
            {"ad": "Akakçe", "url": f"https://www.akakce.com/arama/?q={safe_search}", "logo": "🔍", "tag": "📊 Genel Karşılaştırma", "tip": "hepsi"}
        ]
        
        # Ürün donanımsa, tipi sadece 'ekipman' olan mağazaları filtreleyip listeye almıyoruz
        aktif_magazalar = []
        for m in tum_magazalar:
            if is_donanim and m["tip"] == "ekipman":
                continue  # Wraith'i listeye dahil etme, pas geç
            aktif_magazalar.append(m)
        
        st.subheader("🛍️ Mağaza Seçenekleri")
        
        sol_col, sag_col = st.columns(2)
        
        # Filtrelenmiş yeni listeyi sütunlara dengeli dağıtarak ekrana bas
        for i, m in enumerate(aktif_magazalar):
            ek_etiket = f" ({m['tag']})" if m['tag'] else ""
            buton_metni = f"{m['logo']} {m['ad']}{ek_etiket}"
            
            if i % 2 == 0:
                sol_col.link_button(buton_metni, m['url'], use_container_width=True)
            else:
                sag_col.link_button(buton_metni, m['url'], use_container_width=True)
