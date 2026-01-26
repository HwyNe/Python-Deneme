# 📝 Yenilikçi Görev Yöneticisi

Bu uygulama, günlük işlerinizi organize etmenizi sağlayan, önceliklendirme özellikli ve verileri kalıcı olarak saklayan bir komut satırı (CLI) aracıdır.

## 🛠️ Kodun Adım Adım İşleyişi

1. **Sınıf Yapısı (OOP):** Kod, `Task` (Görev) ve `TaskManager` (Yönetici) sınıfları üzerine kurulmuştur. Bu sayede veriler düzenli tutulur.
2. **Renklendirme:** Terminal ekranını daha okunabilir kılmak için ANSI renk kodları kullanılmıştır (Tamamlananlar Yeşil, Bekleyenler Sarı).
3. **Veri Saklama (JSON):** - `load_tasks()`: Program açıldığında `tasks.json` dosyasındaki eski görevleri yükler.
   - `save_tasks()`: Yapılan her değişiklikte (ekleme, silme) güncel listeyi dosyaya kaydeder.
4. **Hata Yakalama:** Kullanıcı hatalı bir sayı girdiğinde veya boş bir görev eklemeye çalıştığında program çökmez, kullanıcıyı uyarır.
5. **Özellikler:** Her görev; isim, öncelik (Yüksek/Orta/Düşük), kategori ve oluşturulma zamanı bilgilerini içerir.



## 🚀 Çalıştırma
1. Terminalinizi açın.
2. Proje klasörüne gidin.
3. Şu komutu çalıştırın: `python main.py`