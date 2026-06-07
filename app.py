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

# 🛠️ NOKTA ATIŞI YENİ KELİME AYIKLAMA ALGORİTMASI
def gelişmiş_kelime_temizle(url):
    try:
        if not url.startswith("http://") and not url.startswith("https://") and "." not in url:
            return None
            
        # URL'i decode et (%20, %30 veya Türkçe karakter karmaşasını çöz)
        url_cozulmus = urllib.parse.unquote(url)
        
        # Query parametrelerini (?p=234, ?boutiqueId vb.) tamamen uçur
        url_temiz = url_cozulmus.split("?")[0].split("#")[0]
        
        # Linki slash, tire ve alt tirelere göre parçala
        parcalar = re.split(r'[/_\-+]', url_temiz)
        
        yasakli = {
            "html", "urun", "p", "detay", "fiyat", "ozellikleri", "satinal", "gaming", 
            "oyuncu", "store", "product", "com", "tr", "www", "https", "http", "item", 
            "shop", "kampanya", "indirim", "firsat", "bilgisayar", "merchantid", "seller"
        }
        
        # 1. Aşama: Sadece gerçek kelime olabilecek harf ağırlıklı parçaları filtrele
        anlamli_parcalar = []
        for p in parcalar:
            p_temiz = p.replace(".html", "").strip()
            # Kısa kodları, saf sayıları ve yasaklı kelimeleri eliyoruz
            if len(p_temiz) > 2 and not p_temiz.isdigit() and p_temiz.lower() not in yasakli:
                # İçinde çok fazla sayı barındıran anlamsız e-ticaret ID'lerini eliyoruz
                if len(re.sub(r'\d', '', p_temiz)) > 2:
                    anlamli_parcalar.append(p_temiz)
        
        # 2. Aşama: Eğer ayıkladığımız kelimeler çok uzun bir liste oluşturduysa
        # Genellikle e-ticaret siteleri ürün adını linkin sonuna doğru ardışık yazar.
        # Bu yüzden listedeki anlamsız tek tük kelimeleri elemek için en uzun blokları seçiyoruz.
        if anlamli_parcalar:
            # En son kısımdaki mantıklı 3 veya 4 kelimeyi birleştiriyoruz
            if len(anlamli_parcalar) > 4:
                # Eğer listenin en son elemanı çok kısaysa muhtemelen koddur, onu es geçip bir öncekileri al
                if len(anlamli_parcalar[-1]) <= 3 and anlamli_parcalar[-1].isalnum():
                    sonuc_kelimeleri = anlamli_parcalar[-5:-1]
                else:
                    sonuc_kelimeleri = anlamli_parcalar[-4:]
            else:
                sonuc_kelimeleri = anlamli_parcalar
                
            ham_sonuc = " ".join(sonuc_kelimeleri)
            # Sadece harf, sayı ve boşluk kalsın
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
        
        # Donanım Kontrolü ve Dinamik Mağaza
