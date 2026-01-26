# 🔐 Profesyonel Şifre Oluşturucu

Güvenlik ihtiyacınıza göre özelleştirilebilir, tahmin edilmesi imkansız güçlü şifreler üreten bir araçtır.

## 🛠️ Kodun Adım Adım İşleyişi

1. **Kullanıcı Tercihleri:** Program ilk olarak şifrenin uzunluğunu (8-50 karakter arası) sorar.
2. **Karakter Havuzu Oluşturma:** Seçtiğiniz kriterlere göre (Büyük harf, küçük harf, rakam, sembol) bir karakter havuzu hazırlanır.
3. **Rastgele Seçim:** Python'ın `random.choice` fonksiyonu kullanılarak, oluşturulan havuzdan rastgele karakterler seçilir.
4. **Özet Ekranı:** Şifre üretilmeden önce seçtiğiniz ayarlar size bir tablo halinde gösterilir.
5. **Güvenlik Kontrolü:** Eğer hiçbir karakter tipi seçmezseniz, program hata verir ve sizi tekrar seçim ekranına yönlendirir.
6. **Sürekli Döngü:** Bir şifre ürettikten sonra program kapanmaz, yeni bir şifre isteyip istemediğinizi sorar.



## 🚀 Çalıştırma
1. Terminalde klasörünüze gidin.
2. Komutu çalıştırın: `python main.py`