import streamlit as st
import urllib.parse

# Sayfa Ayarları
st.set_page_config(
    page_title="GamerFinder Pro", 
    page_icon="🎮", 
    layout="centered"
)

# Tarayıcı Hafızasını Başlatma (Geçmiş Aramalar ve Kaydedilen Fiyatlar İçin)
if "gecmis" not in st.session_state:
    st.session_state.gecmis = []
if "kayitlar" not in st.session_state:
    st.session_state.kayitlar = {}

# Başlık
st.title("🎮 GamerFinder Pro")
st.caption("Fiyat Farkı Hesaplayıcı ve Hafıza Destekli Arama Motoru")
st.write("---")

arama_turu = st.radio("Arama Yöntemi:", ["🔗 Link Analizi", "⌨️ Ürün İsim Arama"], horizontal=True)

# Girdileri saklamak için form yapısı (Enter yerine buton kontrolü için)
with st.form("arama_formu"):
    if arama_turu == "🔗 Link Analizi":
        girdi_alani = st.text_input("Ürün Linkini Yapıştırın:", placeholder="https://www.itopya.com/...")
    else:
        girdi_alani = st.text_input("Ürün Modelini Yazın:", placeholder="Örn: Razer Deathadder V3 Pro")
    
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

# Aktif aranan ürünü hafızada tutmak için yardımcı değişken
if arama_tetiklendi and girdi_alani:
    if arama_turu == "🔗 Link Analizi":
        st.session_state.aktif_urun = kelime_temizle(girdi_alani).upper()
    else:
        st.session_state.aktif_urun = girdi_alani.strip().upper()

    if st.session_state.aktif_urun not in st.session_state.gecmis:
        st.session_state.gecmis.insert(0, st.session_state.aktif_urun)
        st.session_state.gecmis = st.session_state.gecmis[:4]

# --- EĞER BELİRLENMİŞ BİR ÜRÜN VARSA EKRANA BAS ---
if "aktif_urun" in st.session_state:
    urun_adi = st.session_state.aktif_urun
    st.success(f"🎯 Hedef Ürün: **{urun_adi}**")
    
    # HIZLI KOPYALAMA ALANI
    st.code(urun_adi, language="text")
    
    # ⚖️ YENİ ÖZELLİK: FİYAT FARKI HESAPLAMA PANELİ
    st.subheader("⚖️ Manuel Fiyat Analiz Paneli")
    st.write("Siteleri gezdikten sonra gördüğünüz en yüksek ve en düşük fiyatı yazın, aradaki farkı hesaplayalım:")
    
    f_col1, f_col2 = st.columns(2)
    with f_col1:
        en_dusuk = st.number_input("Gördüğünüz En Düşük Fiyat (TL):", min_value=0.0, step=100.0, key="min_f")
    with f_col2:
        en_yuksek = st.number_input("Gördüğünüz En Yüksek Fiyat (TL):", min_value=0.0, step=100.0, key="max_f")
        
    if en_yuksek > 0 and en_dusuk > 0:
        fark = en_yuksek - en_dusuk
        yuzde_fark = (fark / en_dusuk) * 100 if en_dusuk > 0 else 0
        if fark > 0:
            st.warning(f"💰 Siteler arasında tam **{fark:,.2f} TL** fiyat farkı var! En ucuz siteden alırsak **%{yuzde_fark:.1f}** daha kârlısınız.")
        elif fark == 0:
            st.info("İki fiyata da aynı değeri girdiniz. Fark bulunmuyor.")
        else:
            st.error("En yüksek fiyat, en düşük fiyattan az olamaz!")

    # 💾 YENİ ÖZELLİK: FİYATI HAFIZAYA KAYDETME KUTUSU
    st.write("---")
    st.subheader("📌 Bu Ürünün Fiyatını Hafızaya Kaydet")
    
    k_col1, k_col2 = st.columns([2, 1])
    with k_col1:
        bulunan_fiyat = st.text_input("Bulduğunuz En İyi Fiyat ve Mağaza:", placeholder="Örn: 3200 TL - İtopya", key="kayit_not")
    with k_col2:
        st.write(" ") # Hizalama boşluğu
        if st.button("Fiyatı Kaydet 💾", use_container_width=True):
            if bulunan_fiyat:
                st.session_state.kayitlar[urun_adi] = bulunan_fiyat
                st.toast("Fiyat başarıyla hafızaya kaydedildi!", icon="💾")
            else:
                st.warning("Lütfen bir not yazın.")

    # --- LİNKLER VE MAĞAZALAR ---
    st.write("---")
    safe_search = urllib.parse.quote(urun_adi.lower())
    
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
    st.write("Canlı arama sonuçlarını yeni sekmede görmek için tıklayın:")
    
    sol_col, sag_col = st.columns(2)
    for i, m in enumerate(magazalar):
        ek_etiket = f" ({m['tag']})" if m['tag'] else ""
        buton_metni = f"{m['logo']} {m['ad']}{ek_etiket}"
        
        if i % 2 == 0:
            sol_col.link_button(buton_metni, m['url'], use_container_width=True)
        else:
            sag_col.link_button(buton_metni, m['url'], use_container_width=True)

# --- KAYDEDİLENLER VE GEÇMİŞ LİSTESİ ---
if st.session_state.kayitlar or st.session_state.gecmis:
    st.write("---")
    g_col1, g_col2 = st.columns(2)
    
    with g_col1:
        if st.session_state.kayitlar:
            st.subheader("📋 Kaydettiğiniz Fiyatlar")
            for urun, notu in st.session_state.kayitlar.items():
                st.info(f"**{urun}** \n\n 📌 {notu}")
                
    with g_col2:
        if st.session_state.gecmis:
            st.subheader("🕒 Son Aramalarınız")
            for gecmis_urun in st.session_state.gecmis:
                st.caption(f"🔹 {gecmis_urun}")
