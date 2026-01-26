import random
import string
import time

def get_yes_no(prompt):
    while True:
        response = input(f"{prompt} (y/n): ").strip().lower()
        if response in ['y', 'n']:
            return response == 'y'
        print("Lütfen sadece 'y' (Evet) veya 'n' (Hayır) giriniz.")

def get_length():
    while True:
        try:
            length_str = input("Şifre uzunluğu (8-50 arası): ").strip()
            length = int(length_str)
            if 8 <= length <= 50:
                return length
            print("Hata: Lütfen 8 ile 50 arasında bir sayı giriniz.")
        except ValueError:
            print("Hata: Lütfen geçerli bir sayı giriniz.")

def generate_password(length, use_upper, use_lower, use_digits, use_symbols):
    chars = ""
    if use_upper:
        chars += string.ascii_uppercase
    if use_lower:
        chars += string.ascii_lowercase
    if use_digits:
        chars += string.digits
    if use_symbols:
        chars += "!@#$%^&*()_+-=[]{}|;:,.<>?"
    
    if not chars:
        return None

    return "".join(random.choice(chars) for _ in range(length))

def print_summary(length, use_upper, use_lower, use_digits, use_symbols):
    print("\n" + "-"*30)
    print("SEÇİLEN AYARLAR")
    print("-"*30)
    print(f"Uzunluk        : {length}")
    print(f"Büyük Harf     : {'EVET' if use_upper else 'HAYIR'}")
    print(f"Küçük Harf     : {'EVET' if use_lower else 'HAYIR'}")
    print(f"Rakamlar       : {'EVET' if use_digits else 'HAYIR'}")
    print(f"Semboller      : {'EVET' if use_symbols else 'HAYIR'}")
    print("-"*30 + "\n")

def main():
    print("="*50)
    print("   PROFESYONEL ŞİFRE OLUŞTURUCU (DETAYLI CLI)")
    print("="*50)
    print("Hoş geldiniz! Güvenli şifrelerinizi oluşturmak için ayarları girin.\n")

    while True:
        length = get_length()
        
        print("\n--- Karakter Seçenekleri ---")
        use_upper = get_yes_no("Büyük Harfler (A-Z) olsun mu?")
        use_lower = get_yes_no("Küçük Harfler (a-z) olsun mu?")
        use_digits = get_yes_no("Rakamlar (0-9) olsun mu?")
        use_symbols = get_yes_no("Semboller (!@#) olsun mu?")

        print_summary(length, use_upper, use_lower, use_digits, use_symbols)

        if not any([use_upper, use_lower, use_digits, use_symbols]):
            print("[HATA] En az bir karakter türü seçmelisiniz! Ayarlar sıfırlanıyor...\n")
            continue

        if get_yes_no("Bu ayarlarla şifre oluşturulsun mu?"):
            password = generate_password(length, use_upper, use_lower, use_digits, use_symbols)
            
            print("\n" + "*"*40)
            print(f"OLUŞTURULAN ŞİFRE: {password}")
            print("*"*40 + "\n")
        else:
            print("\nİşlem iptal edildi. Ayarlar başa dönüyor...\n")
            continue

        if not get_yes_no("Yeni bir şifre oluşturmak ister misiniz?"):
            print("\nProgramdan çıkılıyor... İyi günler!")
            time.sleep(1)
            break
        print("\n" + "="*50 + "\n")

if __name__ == "__main__":
    main()
