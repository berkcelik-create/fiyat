import streamlit as st
import urllib.parse
import re

# Sayfa Yapılandırması
st.set_page_config(
    page_title="G-ENGINE // Hardware Search Engine", 
    page_icon="🔍", 
    layout="centered"
)

# Başlık ve Tasarım Düzeni
st.title("🔍 G-ENGINE")
st.caption("Hardware Search Engine // Global Donanım Arama ve Doğrulama Motoru")
st.write("---")

# Seçim Modları
arama_turu = st.radio(
    "Arama Modu:", 
    ["🔗 Link Analizi", "⌨️ Model İsmi ile Arama"], 
    horizontal=True
)

# Arama Formu
with st.form("arama_formu"):
    if arama_turu == "🔗 Link Analizi":
        girdi_alani = st.text_input("Ürün Linkini Girin:", placeholder="https://www.itopya.com/...")
    else:
        girdi_alani = st.text_input("Ürün Modelini Girin:", placeholder="Örn: AMD Ryzen 7 7800X3D")
    
    arama_tetiklendi = st.form_submit_button("🔍 Motoru Çalıştır", type="primary", use_container_width=True)

# 🧠 GERÇEK AI TABANLI MODEL AYIKLAMA MOTORU
def yapay_zeka_link_cozucu(url):
    try:
        if not url.startswith(("http://", "https://")):
            url = "https://" + url
            
        # URL'i çöz ve analiz edilebilir düz metne dönüştür
        cozulmus_url = urllib.parse.unquote(url).lower()
        parsed_url = urllib.parse.urlparse(cozulmus_url)
        
        # Domain ve gereksiz parametreleri ele, sadece ürün patikasını al
        link_yolu = parsed_url.path
        
        # Link karakterlerini temizle ve ham kelimeleri çıkar
        ham_kelimeler = re.split(r'[/_\-+.]', link_yolu)
        
        # Algoritmik Süzgeç: Web sitesi çöplerini ilk aşamada ayıkla
        site_copleri = {
            "html", "urun", "p", "detay", "fiyat", "ozellikleri", "satinal", "gaming", 
            "oyuncu", "store", "product", "com", "tr", "net", "org", "item", "shop", 
            "kampanya", "indirim", "firsat", "bilgisayar", "itopya", "vatanbilgisayar",
            "sinerji", "incehesap", "trendyol", "hepsiburada", "amazon", "wraithesports"
        }
        
        filtrelenmiş_kelimeler = []
        for k in ham_kelimeler:
            k = k.strip()
            if len(k) > 1 and not k.isdigit() and k not in site_copleri:
                # E-ticaret sitelerinin otomatik ürettiği u32084 gibi kodları eliyoruz
                if not (any(char.isdigit() for char in k) and len(k) <= 7):
                    filtrelenmiş_kelimeler.append(k)

        # 🧠 AI Akıl Yürütme Katmanı: Donanım dünyasındaki global markaları önceliklendir
        bilinen_markalar = {
            "kingston", "asus", "msi", "gigabyte", "amd", "intel", "nvidia", "corsair", 
            "gskill", "team", "t-force", "samsung", "crucial", "wd", "western", "digital", 
            "seagate", "pny", "zotac", "palit", "gainward", "sapphire", "xfx", "powercolor",
            "razer", "logitech", "steelseries", "hyperx", "glorious", "corsair", "benq"
        }
        
        # Eğer filtrelenen kelimelerin başında bilinen bir marka varsa, marka ve yanındaki 2 kelimeyi al
        for i, kelime in enumerate(filtrelenmiş_kelimeler):
            if kelime in bilinen_markalar:
                return " ".join(filtrelenmiş_kelimeler[i:i+3])
                
        # Eğer bilinen bir marka yakalanamadıysa, en yüksek anlam barındıran ilk 3 kelimeyi döndür
        if filtrelenmiş_kelimeler:
            return " ".join(filtrelenmiş_kelimeler[:3])
            
        return "oyuncu ekipmani"
    except:
        return "oyuncu ekipmani"

# Karakter Dönüştürücü ve Stabilizasyon
def karakter_onari(metin):
    metin = " ".join(metin.split())
    sozluk = {"İ": "I", "ı": "i", "Ş": "S", "ş": "s", "Ç": "C", "ç": "c", "Ğ": "G", "ğ": "g", "Ü": "U", "ü": "u", "Ö": "O", "ö": "o"}
    for eski, yeni in sozluk.items():
        metin = metin.replace(eski, yeni)
    return metin

# Motorun Çalışma Aşaması
if arama_tetiklendi and girdi_alani:
    ana_arama_terimi = ""
    
    if arama_turu == "🔗 Link Analizi":
        ana_arama_terimi = yapay_zeka_link_cozucu(girdi_alani)
    else:
        ana_arama_terimi = girdi_alani
        
    if ana_arama_terimi and len(ana_arama_terimi) >= 2:
        # Metni stabilize et ve büyüt
        ana_arama_terimi = karakter_onari(ana_arama_terimi).upper()
        
        # Sonuç Ekranı
        st.success(f"🎯 Kriptonize Edilen Model: **{ana_arama_terimi}**")
        
        st.write("📋 Başka yerde aratmak için ismi buradan hızlıca kopyalayabilirsiniz:")
        st.code(ana_arama_terimi, language="text")
        
        # Web siteleri için arama sorgusunu URL standartlarına uyarla
        url_kodlu_sorgu = urllib.parse.quote(ana_arama_terimi.lower())
        
        # Dinamik Mağazalar Listesi
        magaza_listesi = [
            {"ad": "Wraith Esports", "url": f"https://wraithesports.com/search?q={url_kodlu_sorgu}", "logo": "🚀", "tag": "⭐ En Ucuz Potansiyeli"},
            {"ad": "İncehesap", "url": f"https://www.incehesap.com/arama/?fiyat_kriteri=1&s={url_kodlu_sorgu}", "logo": "🔥", "tag": ""},
            {"ad": "İtopya", "url": f"https://www.itopya.com/Arama?q={url_kodlu_sorgu}", "logo": "🦎", "tag": "⭐ En Ucuz Potansiyeli"},
            {"ad": "Sinerji", "url": f"https://www.sinerji.gen.tr/arama?q={url_kodlu_sorgu}", "logo": "⚡", "tag": ""},
            {"ad": "Trendyol", "url": f"https://www.trendyol.com/sr?q={url_kodlu_sorgu}", "logo": "🧡", "tag": ""},
            {"ad": "Hepsiburada", "url": f"https://www.hepsiburada.com/ara?q={url_kodlu_sorgu}", "logo": "💙", "tag": ""},
            {"ad": "Amazon TR", "url": f"https://www.amazon.com.tr/s?k={url_kodlu_sorgu}", "logo": "💛", "tag": "⭐ En Ucuz Potansiyeli"},
            {"ad": "Akakçe", "url": f"https://www.akakce.com/arama/?q={url_kodlu_sorgu}", "logo": "🔍", "tag": "📊 Genel Karşılaştırma"}
        ]
        
        st.subheader("🛍️ Mağaza Seçenekleri")
        sol_sutun, sag_sutun = st.columns(2)
        
        for sira, veri in enumerate(magaza_listesi):
            ek_bilgi = f" ({veri['tag']})" if veri['tag'] else ""
            buton_adi = f"{veri['logo']} {veri['ad']}{ek_bilgi}"
            
            if sira % 2 == 0:
                sol_sutun.link_button(buton_adi, veri['url'], use_container_width=True)
            else:
                sag_sutun.link_button(buton_adi, veri['url'], use_container_width=True)
    else:
        st.error("❌ Analiz Hatası: Girilen link veya metin çözümlenemedi.")
