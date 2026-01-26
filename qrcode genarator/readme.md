# 📱 Python QR Kod Oluşturucu

Girdiğiniz metin veya web sitesi bağlantılarını (URL) anında taranabilir yüksek çözünürlüklü `.png` görsellerine dönüştürür.

## 🛠️ Kodun Adım Adım İşleyişi

1. **Veri Girişi:** QR koda dönüştürmek istediğiniz linki veya metni girersiniz.
2. **Dosya Adlandırma:** Kaydedilecek görsele bir isim verirsiniz. İsim vermezseniz otomatik olarak `qr_code.png` ismi atanır.
3. **Uzantı Denetimi:** Dosya isminin sonuna `.png` yazmasanız bile kod bunu algılar ve eksikse otomatik ekler.
4. **Görsel Tasarımı:** `version=1` ve `box_size=10` parametreleri ile standart, okunaklı bir QR matrisi oluşturulur.
5. **Kayıt ve Konum:** Dosya başarıyla kaydedildiğinde, dosyanın bilgisayarınızdaki tam adresi (tam yol) ekrana yazdırılır.



## 📋 Gereksinimler
Çalıştırmadan önce kütüphaneyi yükleyin:
```bash
pip install qrcode[pil]