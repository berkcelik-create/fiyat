import streamlit as st
import requests
from bs4 import BeautifulSoup
import urllib.parse
import pandas as pd
import time

# Sayfa Ayarları
st.set_page_config(page_title="Canlı Fiyat Karşılaştırma", page_icon="💰", layout="centered")

st.title("💰 Akakçe Tarzı Canlı Fiyat Karşılaştırma")
st.write("Bir ürün linki yapıştırın, sistem diğer sitelerdeki fiyatları canlı olarak bulsun!")

# Kullanıcıdan link alma
hedef_link = st.text_input("Ürün Linkini Buraya Yapıştırın:", placeholder="https://www.hepsiburada.com/... veya herhangi bir link")

def urun_adi_temizle(url):
    """Linkten kabaca bir ürün adı tahmin eder (Gerçek projede geliştirilmelidir)"""
    try:
        # Linkin sonundaki kelimeleri alarak basit bir isim tahmini yapar
        parcalar = url.split("/")[-1].split("-")
        isim = " ".join(parcalar[:4]) # İlk 4 kelimeyi al
        return isim if len(isim) > 3 else "İsim Bulunamadı"
    except:
        return "Örnek Ürün"

def n11_ara(urun_adi):
    """N11 sitesinde arama yapar"""
    try:
        url = f"https://www.n11.com/arama?q={urllib.parse.quote(urun_adi)}"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        sayfa = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(sayfa.content, "html.parser")
        ilk_urun = soup.find("li", {"class": "column"})
        isim = ilk_urun.find("h3", {"class": "proName"}).text.strip()
        fiyat = ilk_urun.find("ins").text.strip().replace("TL", "").strip()
        link = ilk_urun.find("a")["href"]
        return {"Site": "N11", "Ürün Adı": isim, "Fiyat (TL)": fiyat, "Link": link}
    except:
        return {"Site": "N11", "Ürün Adı": "Bulunamadı", "Fiyat (TL)": "-", "Link": "#"}

# Butona basıldığında çalışacak kısım
if st.button("Fiyatları Karşılaştır", type="primary"):
    if hedef_link:
        with st.spinner("Ürün analiz ediliyor ve internet taranıyor..."):
            # 1. Linkten ürün adını çıkar
            tahmini_isim = urun_adi_temizle(hedef_link)
            st.info(f"🔍 Aranan Ürün Grubu: **{tahmini_isim}**")
            
            # 2. Siteleri Tara (Örnek olarak N11 ve simüle edilmiş diğer siteler)
            sonuclar = []
            
            # Gerçek canlı veri (N11)
            n11_veri = n11_ara(tahmini_isim)
            sonuclar.append(n11_veri)
            
            # Mantığı görmen için simüle edilmiş Trendyol ve Hepsiburada verileri
            # (Bot engeline takılmamak için gerçek projede buralara 'Selenium' eklenir)
            sonuclar.append({"Site": "Trendyol", "Ürün Adı": f"{tahmini_isim} (Uyumlu)", "Fiyat (TL)": "14.250", "Link": "https://trendyol.com"})
            sonuclar.append({"Site": "Hepsiburada", "Ürün Adı": f"{tahmini_isim} Siyah", "Fiyat (TL)": "14.100", "Link": "https://hepsiburada.com"})
            
            # 3. Tabloyu Oluştur ve Sırala
            df = pd.DataFrame(sonuclar)
            
            # Temiz bir tablo gösterimi
            st.subheader("📊 Bulunan Fiyat Karşılaştırma Tablosu")
            st.dataframe(df, use_container_width=True)
            
            st.success("İşlem tamamlandı! En ucuz fiyatı yukarıdaki tablodan görebilirsiniz.")
    else:
        st.warning("Lütfen önce geçerli bir link girin.")
