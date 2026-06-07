import streamlit as st
import urllib.parse
import re

# Sayfa Ayarları ve Sekme Emojisi
st.set_page_config(
    page_title="G-ENGINE // Hardware Search Engine", 
    page_icon="🔍", 
    layout="centered"
)

# Arama Motoru Başlık Düzeni
st.title("🔍 G-ENGINE")
st.caption("Hardware Search Engine // Global Donanım Arama ve Doğrulama Motoru")
st.write("---")

# İki Farklı Net Arama Modu
arama_turu = st.radio(
    "Arama Modu:", 
    ["🔗 Link Analizi", "⌨️ Model İsmi ile Arama"], 
    horizontal=True
)

# Ana Arama Form Yapısı
with st.form("arama_formu"):
    if arama_turu == "🔗 Link Analizi":
        girdi_alani = st.text_input("Ürün Linkini Girin:", placeholder="https://www.itopya.com/...")
    else:
        girdi_alani = st.text_input("Ürün Modelini Girin:", placeholder="Örn: AMD Ryzen 7 7800X3D")
    
    arama_tetiklendi = st.form_submit_button("🔍 Motoru Çalıştır", type="primary", use_container_width=True)

# 🤖 YAPAY ZEKA DESTEKLİ LINK OKUMA VE TEMİZLEME MOTORU
def gelişmiş_kelime_temizle(url):
    try:
        if not url.startswith("http://") and not url.startswith("https://") and "." not in url:
            return None
            
        # URL'i çöz (Türkçe karakterleri ve %20 gibi boşluk kodlarını onar)
        url_cozulmus = urllib.parse.unquote(url)
        
        # Linkin sonundaki parametreleri (? ve sonrası) temizle
        url_temiz = url_cozulmus.split("?")[0].split("#")[0]
        
        # Linki bölümlere ayır
        parcalar = re.split(r'[/_\-+]', url_temiz)
        
        yasakli = {
            "html", "urun", "p", "detay", "fiyat", "ozellikleri", "satinal", "gaming", 
            "oyuncu", "store", "product", "com", "tr", "www", "https", "http", "item", 
            "shop", "kampanya", "indirim", "firsat", "bilgisayar", "itopya", "vatanbilgisayar",
            "sinerji", "incehesap", "trendyol", "hepsiburada", "amazon", "wraithesports"
        }
        
        # Temiz kelimeleri ayıkla
        anlamli_parcalar = []
        for p in parcalar:
            p_temiz = p.replace(".html", "").strip()
            # Sayısal ID'leri ve çöp kelimeleri eliyoruz
            if len(p_temiz) > 1 and not p_temiz.isdigit() and p_temiz.lower() not in yasakli:
                # Sitenin otomatik bastığı kısa kodları (u32084 gibi) filtrele
                if not (any(char.isdigit() for char in p_temiz) and len(p_temiz) <= 6):
                    anlamli_parcalar.append(p_temiz)
        
        if anlamli_parcalar:
            # 🧠 AI Kuralı: Donanım bileşenlerinde marka/model genellikle linkin BAŞINDA yer alır.
            # "mhz", "cl32", "single", "kit" gibi teknik uzantıları listenin sonundan temizlemek için akıllı filtre:
            teknik_copler = {"mhz", "cl30", "cl32", "cl36", "gb", "ddr4", "ddr5", "single", "kit", "dual", "siyah", "beyaz", "rgb"}
            
            # Baştaki kelimelerden teknik çöp olmayanları önceliklendirerek en mantıklı 3-4 kelimeyi çek
            ai_secimi = []
            for kelime in anlamli_parcalar:
                if len(ai_secimi) < 3:  # En ideal arama kelimesi uzunluğu
                    ai_secimi.append(kelime)
                elif len(ai_secimi) < 4 and kelime.lower() not in teknik_copler:
                    ai_secimi.append(kelime)
            
            ham_sonuc = " ".join(ai_secimi)
            temiz_sonuc = re.sub(r'[^a-zA-Z0-9\s]', '', ham_sonuc)
            return temiz_sonuc.strip()
            
        return "Oyuncu Ekipmanı"
    except:
        return "Oyuncu Ekipmanı"

# Akıllı Boşluk ve Türkçe Karakter Toleransı
def akilli_metin_duzelt(metin):
    metin = " ".join(metin.split())
    donusum = {"İ": "I", "ı": "i", "Ş": "S", "ş": "s", "Ç": "C", "ç": "c", "Ğ": "G", "ğ": "g", "Ü": "U", "ü": "u", "Ö": "O", "ö": "o"}
    for kaynak, placeholder in donusum.items():
        metin = metin.replace(kaynak, placeholder)
    return metin

# Arama Motorunun Çalıştırılma Aşaması
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
        
        # Kopyalama Panosu
        st.write("📋 Başka yerde aratmak için ismi buradan hızlıca kopyalayabilirsiniz:")
        st.code(arama_kelimesi_upper, language="text")
            
        safe_search = urllib.parse.quote(arama_kelimesi.lower())
        
        # Donanım Kontrolü ve Dinamik Mağaza Filtreleme
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
