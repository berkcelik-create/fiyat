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

# Üç Farklı Arama Modu
arama_turu = st.radio(
    "Arama Modu:", 
    ["🔗 Link Analizi", "⌨️ Model İsmi ile Arama", "🤖 AI Açıklama ile Arama"], 
    horizontal=True
)

# Ana Arama Form Yapısı
with st.form("arama_formu"):
    if arama_turu == "🔗 Link Analizi":
        girdi_alani = st.text_input("Ürün Linkini Girin:", placeholder="https://www.itopya.com/...")
    elif arama_turu == "⌨️ Model İsmi ile Arama":
        girdi_alani = st.text_input("Ürün Modelini Girin:", placeholder="Örn: AMD Ryzen 7 7800X3D")
    else:
        girdi_alani = st.text_input("Aradığınız Ekipmanı Tarif Edin:", placeholder="Örn: siyah hafif kablosuz oyuncu mouse rgb")
    
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
    for kaynak, placeholder in donusum.items():
        metin = metin.replace(kaynak, placeholder)
    return metin

# AI Modu Kelime Süzgeci
def ai_kelime_süzgeci(tarif):
    tarif = tarif.lower()
    gereksizler = [
        "bana", "bul", "getir", "ara", "arat", "tarzı", "gibi", "en", "iyi", "güzel", 
        "kaliteli", "ucuz", "fiyatlı", "bir", "tane", "istiyorum", "lazım", "olan", "ve", "veya"
    ]
    kelimeler = tarif.split()
    temiz_kelimeler = [k for k in kelimeler if k not in gereksizler]
    return " ".join(temiz_kelimeler[:4]) if temiz_kelimeler else "Oyuncu Ekipmanı"

# AI Modu Özellik Yorumlama
def ai_ozellik_yorumlama(tarif):
    tarif = tarif.lower()
    analiz_notlari = []
    
    if "mouse" in tarif or "fare" in tarif:
        analiz_notlari.append("🎯 **Ekipman Türü:** Oyuncu Mouse'u")
        if "hafif" in tarif:
            analiz_notlari.append("⚡ **AI Yorumu:** Hafif tasarımlar (flick atmak) ve FPS oyunlarında (Valorant, CS2) refleks hızını doğrudan artırır.")
        if "kablosuz" in tarif or "wireless" in tarif:
            analiz_notlari.append("📶 **AI Yorumu:** Kablosuz bağlantı masa üstündeki sürtünmeyi sıfırlayarak hareket özgürlüğü sağlar.")
    elif "klavye" in tarif or "keyboard" in tarif:
        analiz_notlari.append("⌨️ **Ekipman Türü:** Oyuncu Klavyesi")
        if "mekanik" in tarif:
            analiz_notlari.append("🕹️ **AI Yorumu:** Mekanik switchler daha düşük tepki süresi (ms) ve daha yüksek tuş ömrü sunar.")
    elif any(x in tarif for x in ["islemci", "cpu", "ekran karti", "gpu", "ram", "anakart"]):
        analiz_notlari.append("🖥️ **Ekipman Türü:** İç Donanım Bileşeni")
        analiz_notlari.append("🚀 **AI Yorumu:** Saf performans odaklı donanım mimarisi. Oyun içi FPS değerini ve kararlılığı doğrudan etkiler.")
    else:
        analiz_notlari.append("🎮 **Ekipman Türü:** Genel Oyuncu Ekipmanı")
        analiz_notlari.append("💡 **AI Yorumu:** Girdiğiniz kriterlere göre mağaza veritabanlarında optimizasyon araması başlatıldı.")
    return analiz_notlari

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
    elif arama_turu == "⌨️ Model İsmi ile Arama":
        arama_kelimesi = girdi_alani
    else:
        arama_kelimesi = ai_kelime_süzgeci(girdi_alani)
            
    if arama_kelimesi:
        arama_kelimesi = akilli_metin_duzelt(arama_kelimesi)

    if hata_var or not arama_kelimesi or len(arama_kelimesi) < 2:
        st.error("❌ Analiz Başarısız. Lütfen girdi formatını kontrol edin.")
    else:
        arama_kelimesi_upper = arama_kelimesi.upper()
        
        # Yapay Zeka Alanı Gösterimi
        if arama_turu == "🤖 AI Açıklama ile Arama":
            st.info("🤖 **G-ENGINE AI ASİSTANI PANELİ**")
            rapor = ai_ozellik_yorumlama(girdi_alani)
            for madde in rapor:
                st.write(madde)
            st.write(f"🔍 *Yapay zeka tarafından optimize edilen arama terimi:* `{arama_kelimesi_upper}`")
            st.write("---")
        else:
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

# --- ⚖️ SENİN MANUEL FİYAT ANALİZ VE HAFIZA PANELİN (Görsel 1) ---
st.write("---")
st.subheader("⚖️ Manuel Fiyat Analiz Paneli")
st.caption("Siteleri gezdikten sonra gördüğünüz en yüksek ve en düşük fiyatı yazın, aradaki farkı hesaplayalım:")

col1, col2 = st.columns(2)
with col1:
    en_dusuk = st.number_input("Gördüğünüz En Düşük Fiyat (TL):", min_value=0.0, value=0.0, step=10.0)
with col2:
    en_yuksek = st.number_input("Gördüğünüz En Yüksek Fiyat (TL):", min_value=0.0, value=0.0, step=10.0)

if en_dusuk > 0 and en_yuksek > 0:
    if en_yuksek >= en_dusuk:
        fark = en_yuksek - en_dusuk
        tasarruf_orani = (fark / en_yuksek) * 100
        st.info(f"📊 **Analiz Sonucu:** Mağazalar arası fark **{fark:,.2f} TL**. En ucuzunu seçerek **%{tasarruf_orani:.1f}** tasarruf edebilirsiniz!")
    else:
        st.warning("⚠️ En yüksek fiyat, en düşük fiyattan küçük olamaz.")

# Hafızaya Kaydetme Bölümü
st.write("---")
st.subheader("📌 Bu Ürünün Fiyatını Hafızaya Kaydet")

with st.form("hafiza_formu"):
    kayit_metni = st.text_input("Bulduğunuz En İyi Fiyat ve Mağaza:", placeholder="Örn: 4200 TL - Amazon")
    kaydet_butonu = st.form_submit_button("Fiyatı Kaydet 💾")
    
    if kaydet_butonu:
        if kayit_metni:
            st.session_state["kayitli_fiyat"] = kayit_metni
            st.success(f"💾 Hafızaya Alındı: '{kayit_metni}'")
        else:
            st.warning("⚠️ Lütfen kaydetmek için bir veri yazın.")

# Eğer hafızada kayıtlı veri varsa ekranda sessizce göster
if "kayitli_fiyat" in st.session_state:
    st.info(f"📌 **Hafızadaki Son Notunuz:** {st.session_state['kayitli_fiyat']}")
