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

# 🧠 BİLEŞEN ODAKLI LINK ÇÖZÜMLEME MOTORU
def yapay_zeka_link_cozucu(url):
    try:
        if not url.startswith(("http://", "https://")):
            url = "https://" + url
            
        # URL'i çöz ve küçük harfe çevir
        cozulmus_url = urllib.parse.unquote(url).lower()
        parsed_url = urllib.parse.urlparse(cozulmus_url)
        
        # Sadece path (yol) kısmını alıyoruz
        link_yolu = parsed_url.path
        
        # Link karakterlerini parçala
        ham_kelimeler = re.split(r'[/_\-+.]', link_yolu)
        
        # Web sitesi çöplerini ayıkla (RAM, bileşen adları listeden çıkarıldı!)
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
                # u32084 gibi otomatik üretilen kodları uçur
                if not (any(char.isdigit() for char in k) and len(k) <= 7):
                    filtrelenmiş_kelimeler.append(k)

        # Global donanım markaları havuzu
        bilinen_markalar = {
            "kingston", "asus", "msi", "gigabyte", "amd", "intel", "nvidia", "corsair", 
            "gskill", "team", "t-force", "samsung", "crucial", "wd", "western", "digital", 
            "seagate", "pny", "zotac", "palit", "gainward", "sapphire", "xfx", "powercolor",
            "razer", "logitech", "steelseries", "hyperx", "glorious", "benq"
        }
        
        # Marka yakalanırsa yanına 2 kelime daha alıp modeli daralt
        for i, kelime in enumerate(filtrelenmiş_kelimeler):
            if kelime in bilinen_markalar:
                return " ".join(filtrelenmiş_kelimeler[i:i+3])
                
        if filtrelenmiş_kelimeler:
            return " ".join(filtrelenmiş_kelimeler[:3])
            
        return "oyuncu ekipmani"
    except:
        return "oyuncu ekipmani"

# Karakter Onarıcı
def karakter_onari(metin):
    metin = " ".join(metin.split())
    sozluk = {"İ": "I", "ı": "i", "Ş": "S", "ş": "s", "Ç": "C", "ç": "c", "Ğ": "G", "ğ": "g", "Ü": "U", "ü": "u", "Ö": "O", "ö": "o"}
    for eski, yeni in sozluk.items():
        metin = metin.replace(eski, yeni)
    return metin

# Motor Çalışma Mantığı
if arama_tetiklendi and girdi_alani:
    ana_arama_terimi = ""
    
    if arama_turu == "🔗 Link Analizi":
        ana_arama_terimi = yapay_zeka_link_cozucu(girdi_alani)
    else:
        ana_arama_terimi = girdi_alani
        
    if ana_arama_terimi and len(ana_arama_terimi) >= 2:
        ana_arama_terimi = karakter_onari(ana_arama_terimi).upper()
        
        # Sonuç Ekranı
        st.success(f"🎯 Kriptonize Edilen Model: **{ana_arama_terimi}**")
        
        st.write("📋 Başka yerde aratmak için ismi buradan hızlıca kopyalayabilirsiniz:")
        st.code(ana_arama_terimi, language="text")
        
        # 🌟 Standart Boşluklu Encode (Genel Siteler İçin)
        sorgu_kucuk = ana_arama_terimi.lower()
        safe_search_normal = urllib.parse.quote(sorgu_kucuk)
        
        # 🌟 İtopya Özel Artılı Standart Encode (İtopya'da Arama Yapabilmesi İçin Şart!)
        safe_search_itopya = sorgu_kucuk.replace(" ", "+")
        
        # Mağazalar Listesi (Özel itopya sorgusu entegre edildi)
        magaza_listesi = [
            {"ad": "Wraith Esports", "url": f"https://wraithesports.com/search?q={safe_search_normal}", "logo": "🚀", "tag": "⭐ En Ucuz Potansiyeli"},
            {"ad": "İncehesap", "url": f"https://www.incehesap.com/arama/?fiyat_kriteri=1&s={safe_search_normal}", "logo": "🔥", "tag": ""},
            {"ad": "İtopya", "url": f"https://www.itopya.com/Arama?q={safe_search_itopya}", "logo": "🦎", "tag": "⭐ En Ucuz Potansiyeli"},
            {"ad": "Sinerji", "url": f"https://www.sinerji.gen.tr/arama?q={safe_search_normal}", "logo": "⚡", "tag": ""},
            {"ad": "Trendyol", "url": f"https://www.trendyol.com/sr?q={safe_search_normal}", "logo": "🧡", "tag": ""},
            {"ad": "Hepsiburada", "url": f"https://www.hepsiburada.com/ara?q={safe_search_normal}", "logo": "💙", "tag": ""},
            {"ad": "Amazon TR", "url": f"https://www.amazon.com.tr/s?k={safe_search_normal}", "logo": "💛", "tag": "⭐ En Ucuz Potansiyeli"},
            {"ad": "Akakçe", "url": f"https://www.akakce.com/arama/?q={safe_search_normal}", "logo": "🔍", "tag": "📊 Genel Karşılaştırma"}
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
