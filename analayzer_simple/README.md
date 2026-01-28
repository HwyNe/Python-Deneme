# Sitemap.XML Analiz Aracı

## ⚠️ YASAL UYARI

Bu araç **eğitim amaçlı** olarak tasarlanmıştır. Kullanmadan önce şunları okumanız gerekir:

### ✅ YAPABILECEĞINIZ ŞEYLER:
- **Kendi web sitelerinizi** analiz etmek
- **Açık test sitelerini** analiz etmek (izin verilmiş alanlar)
- **Şahsi laboratuvarınızı** test etmek
- **Bug bounty programlarında** katıldığınız siteleri test etmek (program kurallarına uygun şekilde)

### ❌ YAPAMAYACAĞINIZ ŞEYLER:
- İzin **olmadan** başkasının sitesini scrape etmek
- Trendyol, N11, Amazon, Instagram gibi **e-ticaret ve sosyal medya** sitelerini scrape etmek
- Banka, sigorta, finansal sitelerine erişim sağlamak
- Başkasının sunucusuna zarar vermek amacıyla kullanmak

**Kural basit: Sadece izin verilen yerlerde kullanın!**

---

---

## 📦 KURULUM

### Gerekli Kütüphaneler:
```bash
pip install requests beautifulsoup4
```

### XML Parser Kurulumu (Windows):
```bash
pip install lxml
```

---

## 🚀 KULLANIM

### Basit Kullanım:
```bash
python sitemap_analyzer.py
```

Sonra sorduğunda domain yazın:
```
[?] Domain gir (örn: example.com): wikipedia.org
```

### Çıktı:
```
================================================================================
[!] ÖNEMLİ URL'LER (BUG BOUNTY)
================================================================================
[+] https://wikipedia.org/wiki/Admin -> Anahtar: admin

[*] DİĞER URL'LER
================================================================================
[-] https://wikipedia.org/wiki/Main_Page
[-] https://wikipedia.org/wiki/About
...

[+] Sonuçlar kaydedildi: wikipedia.org_sitemap_analysis.csv
```

---

## 📊 ÇIKTI DOSYASI

Analiz bitince **CSV dosyası** oluşturulur:

**Dosya adı:** `domain_sitemap_analysis.csv`

**İçeriği:**
| URL | Son Güncelleme | Güncelleme Sıklığı | Öncelik | Tür | Bulunan Kelime |
|-----|----------------|--------------------|---------|-----|----------------|
| https://example.com/admin | 2024-01-15 | weekly | 0.8 | ÖNEMLİ | admin |
| https://example.com/blog | 2024-01-10 | daily | 0.5 | NORMAL | - |

---

## 🔍 ARA KELIMELER

Aracı, bu kelimeleri bulunca URL'yi **ÖNEMLİ** olarak işaretler:

```
admin, api, login, private, config, settings,
user, password, auth, backup, database, db,
secret, key, token, internal, panel, dashboard,
debug, test, staging, dev, development, console
```

Kendi kelimelerinizi eklemek için `IMPORTANT_KEYWORDS` listesini düzenleyin.

---

## 💡 BUG BOUNTY ve CTF İçin İPUÇLARI

1. **Önemli URL'leri kontrol edin** - `/admin`, `/api` vb. bulduğunuzda onları inceyin
2. **Son güncelleme tarihleri** - Yeni güncellenen sayfalar genelde etkin sunuculardır
3. **Robots.txt'i de kontrol edin** - Aynı domaine `/robots.txt` ekleyerek bakın
4. **Sitemap indeks** - `sitemap_index.xml` varsa, daha fazla sitemap olabilir

---

## ❓ SORDUNDA HATALAR

### Hata: "sitemap bulunamadı"
- Site sitemap.xml kullanmıyor olabilir
- Domain doğru yazılmış mı kontrol edin
- `https://` eklemeyin, sadece `example.com` yazın

### Hata: "Bağlantı hatası"
- İnternet bağlantınızı kontrol edin
- Firewall'a bağlı olabilir
- VPN kullanıyorsanız kapatıp deneyin

### Hata: "Parse hatası"
- Sitemap yapısı standart değil olabilir
- Bir başka site deneyin

---

## 🎯 HEDEF KURMAK (CTF İçin)

Ekibinizle birlikte şu hedefleri koyun:

1. ✅ İlk 3 yasal sitede çalıştırma
2. ✅ CSV çıktısını analiz etme
3. ✅ Önemli URL'leri manuel inceleme
4. ✅ Kendi robots.txt analiz aracı yazma
5. ✅ Sitemap indeks analizi ekleme

---

## 📚 KAYNAKLAR

- [Robots.txt Rehberi](https://www.robotstxt.org/)
- [Sitemap Protokolü](https://www.sitemaps.org/)
- [Web Scraping Etikleri](https://en.wikipedia.org/wiki/Web_scraping)
- [OWASP - Recon](https://owasp.org/www-project-web-security-testing-guide/)

---



---

**Başarılar! 🚀**
[Muhammed Emin Karkın](https://github.com/HwyNe)
