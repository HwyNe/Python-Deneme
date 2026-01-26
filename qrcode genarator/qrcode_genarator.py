import qrcode
import os

def qr_olustur():
    print("--- QR Kod Oluşturucu ---")
    
    # Kullanıcıdan veri al
    veri = input("QR koda dönüştürülecek metni veya URL'yi girin: ")
    
    if not veri:
        print("Hata: Boş veri girdiniz!")
        return

    # Dosya ismini al
    dosya_adi = input("Kaydedilecek dosya adı (sonuna .png eklemene gerek yok): ")
    
    if not dosya_adi:
        dosya_adi = "qr_code"  # Varsayılan isim
    
    # .png uzantısını kontrol et ve ekle
    if not dosya_adi.endswith(".png"):
        dosya_adi += ".png"

    # QR Kodu oluştur
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    
    qr.add_data(veri)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    # Kaydet
    try:
        img.save(dosya_adi)
        print(f"Başarılı! QR kod '{dosya_adi}' olarak kaydedildi.")
        print(f"Konum: {os.path.abspath(dosya_adi)}")
    except Exception as e:
        print(f"Bir hata oluştu: {e}")

if __name__ == "__main__":
    qr_olustur()