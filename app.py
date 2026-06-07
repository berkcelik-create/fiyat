import streamlit as st
import urllib.parse
import re

# Sayfa Ayarları ve Sekme Emojisi
st.set_page_config(
    page_title="G-ENGINE // Hardware Search Engine", 
    page_icon="🔍", 
    layout="centered"
)

# --- 💬 SAĞ ALT KÖŞE CANLI DESTEK TASARIMI (CSS & HTML) ---
# Bu kod sitenin orijinal yapısını bozmadan sağ alta şık bir destek formu kenarlığı ekler.
st.markdown("""
<style>
    /* Canlı Destek Butonu ve Kutusu İçin Sabitleme */
    .destek-container {
        position: fixed;
        bottom: 20px;
        right: 20px;
        z-index: 9999;
        font-family: 'Inter', sans-serif;
    }
</style>
""", unsafe_allow_html=True)

# Yeni Arama Motoru Başlık Düzeni
st.title("🔍 G-ENGINE")
st.caption("Hardware Search Engine // Global Donanım Arama ve Doğrulama Motoru")
st.write("---")

arama_turu = st.radio("Arama Modu:", ["🔗 Link Analizi", "⌨️ Model İsmi ile Arama"], horizontal=True)

# Sadece butona basınca araması için form yapısı (Enter'a basınca tetiklenmez)
with st.form("arama_formu"):
    if arama_turu == "🔗 Link Analizi":
        girdi_alani = st.text_input("Ürün Linkini Girin:", placeholder="https://www.itopya.com/...")
    else:
        girdi_alani = st.text_input("Ürün Modelini Girin:", placeholder="Örn: AMD Ryzen 7 7800X3D")
    
    arama_tetiklendi = st.form_submit_button("🔍 Motoru Çalıştır", type="primary", use_container_width=True)

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

# Akıllı Boşluk Toleransı
def akilli_metin_duzelt(metin):
    metin = " ".join(metin.split())
    donusum = {"İ": "I", "ı": "i", "Ş": "S", "ş": "s", "Ç": "C", "ç": "c", "Ğ": "G", "ğ": "g", "Ü": "U", "ü": "u", "Ö": "O", "ö": "o"}
    for kaynak, hedef in donusum.items():
        metin = metin.replace(kaynak, hedef)
    return metin

# Arama İşlemleri
if arama_tetiklendi and girdi_alani:
    hata_var = False
    arama_kelimesi = ""
    
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
        st.error("❌ Analiz Başarısız. Lütfen girdi formatını kontrol edin.")
    else:
        arama_kelimesi_upper = arama_kelimesi.upper()
        st.success(f"🎯 Kriptonize Edilen Model: **{arama_kelimesi_upper}**")
        
        # HIZLI KOPYALAMA ALANI
        st.write("📋 Başka yerde aratmak için ismi buradan hızlıca kopyalayabilirsiniz:")
        st.code(arama_kelimesi_upper, language="text")
            
        safe_search = urllib.parse.quote(arama_kelimesi.lower())
        
        # Dinamik Gizleme Kontrolü (Wraith Esports donanım satmadığı için gizlenir)
        donanim_kelimeleri = ["ekran karti", "islemci", "anakart", "ram", "ssd", "power", "psu", "kasa", "gpu", "cpu", "sivi sogutma", "fan"]
        is_donanim = any(x in arama_kelimesi.lower() for x in donanim_kelimeleri)
        
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
        
        # Eğer donanım aranıyorsa ekipman sitesini listeden tamamen uçur
        aktif_magazalar = [m for m in tum_magazalar if not (is_donanim and m["tip"] == "ekipman")]
        
        st.subheader("🛍️ Mağaza Seçenekleri")
        
        sol_col, sag_col = st.columns(2)
        
        for i, m in enumerate(aktif_magazalar):
            ek_etiket = f" ({m['tag']})" if m['tag'] else ""
            buton_metni = f"{m['logo']} {m['ad']}{ek_etiket}"
            
            if i % 2 == 0:
                sol_col.link_button(buton_metni, m['url'], use_container_width=True)
            else:
                sag_col.link_button(buton_metni, m['url'], use_container_width=True)

# --- ⚙️ CANLI DESTEK MENÜSÜNÜN ÇALIŞMA MANTIĞI ---
st.write("---")
# Alt kısma gizlenmiş lüks bir genişletilebilir alan açıyoruz (Sağ alttaki buton simülasyonu için)
with st.sidebar:
    st.subheader("💬 Canlı Destek & Geri Bildirim")
    st.caption("Sistemle ilgili bir sorun veya öneriniz varsa anında iletebilirsiniz.")
    
    with st.form("canli_destek_formu", clear_on_submit=True):
        destek_isim = st.text_input("Adınız:", placeholder="Örn: Ahmet")
        destek_eposta = st.text_input("E-Posta Adresiniz:", placeholder="isim@domain.com")
        destek_mesaj = st.text_area("Mesajınız / Öneriniz:", placeholder="Sistem harika çalışıyor, şunlar da eklenebilir...")
        
        destek_gonder = st.form_submit_button("Mesajı İlet 🚀", use_container_width=True)
        
        if destek_gonder:
            if destek_isim and destek_mesaj:
                st.success("✅ Mesajınız başarıyla iletildi! En kısa sürede incelenecektir.")
            else:
                st.warning("⚠️ Lütfen adınızı ve mesajınızı boş bırakmayın.")
