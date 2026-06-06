import streamlit as st
import requests
from bs4 import BeautifulSoup
import urllib.parse
import pandas as pd

# Sayfa Ayarları
st.set_page_config(page_title="Canlı Fiyat Karşılaştırma", page_icon="💰", layout="centered")

st.title("💰 Akakçe Tarzı Canlı Fiyat Karşılaştırma")
st.write("Bir ürün linki yapıştırın, sistem diğer sitelerdeki fiyatları canlı olarak bulsun!")

# Kullanıcıdan link alma (Hata veren tırnak işaretini burada düzelttim)
hedef_link = st.text_input("Ürün Linkini Buraya Yapıştırın:", placeholder="Örn: https://www.hepsiburada.com/...")

def urun_adini_temizle(url):
    """Linkten ürün adını daha temiz bir şekilde çıkarmaya çalışır"""
    try:
        # Link yapısındaki tire işaretlerini temizleyip kelimeleri ayıklar
        parcalar = url.split("/")[-1].split("?")[0].split("-")
        # Anlamsız kısa kodları veya p-1234 gibi id'leri filtrele
        temiz_kelimeler = [k for k in parcalar if len(k) > 2 and not k.startswith("p")]
        if temiz_kelimeler:
            return " ".join(temiz_kelimeler[:4]) # İlk 4 anahtar kelime yeterli
        return "Gamer Monitör"
    except:
        return "Gamer Monitör"

def n11_canli_ara(urun_adi):
    """N11 üzerinde canlı arama yapar"""
    try:
        url = f"https://www.n11.com/arama?q={urllib.parse.quote(urun_adi)}"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        sayfa = requests.get(url, headers=headers, timeout=7)
        soup = BeautifulSoup(sayfa.content, "html.parser")
        
        ilk_urun = soup.find("li", {"class": "column"})
        isim = ilk_urun.find("h3", {"class": "proName"}).text.strip()
        fiyat = ilk_urun.find("ins").text.strip().replace("TL", "").strip()
        link = ilk_urun.find("a")["href"]
        return {"Site": "N11", "Ürün Adı": isim, "Fiyat (TL)": fiyat, "Link": link}
    except:
        return {"Site": "N11", "Ürün Adı": "Ürün bulunamadı veya korumaya takıldı", "Fiyat (TL)": "-", "Link": "#"}

def pazarama_canli_ara(urun_adi):
    """Pazarama üzerinde canlı arama yapar"""
    try:
        url = f"https://www.pazarama.com/arama?q={urllib.parse.quote(urun_adi)}"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        sayfa = requests.get(url, headers=headers, timeout=7)
        soup = BeautifulSoup(sayfa.content, "html.parser")
        
        # Pazarama liste kartı yapısı
        ilk_urun = soup.find("div", {"class": "product-card"})
        isim = ilk_urun.find("p", {"class": "product-name"}).text.strip()
        fiyat = ilk_urun.find("div", {"class": "price"}).text.strip().replace("TL", "").strip()
        link = "https://www.pazarama.com" + ilk_urun.find("a")["href"]
        return {"Site": "Pazarama", "Ürün Adı": isim, "Fiyat (TL)": fiyat, "Link": link}
    except:
        return {"Site": "Pazarama", "Ürün Adı": "Ürün bulunamadı veya korumaya takıldı", "Fiyat (TL)": "-", "Link": "#"}

def teknosa_canli_ara(urun_adi):
    """Teknosa üzerinde canlı arama yapar"""
    try:
        url = f"https://www.teknosa.com/arama/?s={urllib.parse.quote(urun_adi)}"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        sayfa = requests.get(url, headers=headers, timeout=7)
        soup = BeautifulSoup(sayfa.content, "html.parser")
        
        ilk_urun = soup.find("div", {"class": "product-item"})
        isim = ilk_urun.find("span", {"class": "prd-name"}).text.strip()
        fiyat = ilk_urun.find("span", {"class": "prd-prc2"}).text.strip().replace("TL", "").strip()
        link = "https://www.teknosa.com" + ilk_urun.find("a")["href"]
        return {"Site": "Teknosa", "Ürün Adı": isim, "Fiyat (TL)": fiyat, "Link": link}
    except:
        return {"Site": "Teknosa", "Ürün Adı": "Ürün bulunamadı veya korumaya takıldı", "Fiyat (TL)": "-", "Link": "#"}

# Buton Tetikleme
if st.button("Fiyatları Karşılaştır", type="primary"):
    if hedef_link:
        with st.spinner("İnternet canlı olarak taranıyor... (Bu işlem 5-10 saniye sürebilir)"):
            
            # 1. Linkten kelimeleri ayıkla
            arama_kelimesi = urun_adini_temizle(hedef_link)
            st.info(f"🔍 Algılanan Ürün Arama Kelimesi: **{arama_kelimesi}**")
            
            # 2. Canlı Taramaları Gerçekleştir
            sonuclar = []
            sonuclar.append(n11_can
