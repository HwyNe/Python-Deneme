import requests
import csv
import re
import sys
import time

# Önemli kelimeler
IMPORTANT_KEYWORDS = [
    'admin', 'api', 'login', 'private', 'config', 'settings',
    'user', 'password', 'auth', 'backup', 'database', 'db',
    'secret', 'key', 'token', 'internal', 'panel', 'dashboard',
    'debug', 'test', 'staging', 'dev', 'development', 'console',
    'manage', 'control', 'staff', 'employee', 'member', 'account',
    'wp-admin', 'administrator', 'moderator', 'superuser'
]

TIMEOUT = 10
MAX_RETRIES = 3
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

class SitemapAnalyzer:
    def __init__(self, domain):
        self.domain = self._normalize_domain(domain)
        self.base_url = self.domain if self.domain.startswith('http') else f'https://{self.domain}'
        self.base_url = self.base_url.rstrip('/')
        self.found_sitemaps = []
        self.all_urls = []
        
    def _normalize_domain(self, domain):
        """Domain'i normalize et"""
        domain = domain.strip()
        if not domain.startswith('http'):
            domain = 'https://' + domain
        return domain.rstrip('/')
    
    def _make_request(self, url):
        """URL'ye istek yap, retry desteği"""
        for attempt in range(MAX_RETRIES):
            try:
                print(f"[↻] Bağlanılıyor ({attempt + 1}/{MAX_RETRIES})...")
                response = requests.get(url, timeout=TIMEOUT, headers=HEADERS)
                return response
            except requests.Timeout:
                print(f"[!] Timeout ({attempt + 1}/{MAX_RETRIES})")
                if attempt == MAX_RETRIES - 1:
                    return None
                time.sleep(1)
            except requests.RequestException as e:
                print(f"[!] Hata: {str(e)[:50]}")
                if attempt == MAX_RETRIES - 1:
                    return None
                time.sleep(1)
        return None
    
    def find_sitemaps_in_robots(self):
        """robots.txt dosyasında sitemap URL'lerini bul"""
        print(f"\n[*] robots.txt taranıyor...")
        
        robots_url = f"{self.base_url}/robots.txt"
        response = self._make_request(robots_url)
        
        if not response or response.status_code != 200:
            print(f"[-] robots.txt bulunamadı")
            return False
        
        try:
            content = response.text
            sitemaps = []
            
            for line in content.split('\n'):
                line = line.strip()
                if line.lower().startswith('sitemap:'):
                    sitemap_url = line.split(':', 1)[1].strip()
                    sitemaps.append(sitemap_url)
                    print(f"[+] Bulundu: {sitemap_url}")
            
            if sitemaps:
                self.found_sitemaps = sitemaps
                return True
            else:
                print("[-] robots.txt'te sitemap yok")
                return False
        except Exception as e:
            print(f"[-] robots.txt hatası: {e}")
            return False
    
    def download_sitemaps(self):
        """Sitemap'leri indir ve URL'leri çıkar"""
        if not self.found_sitemaps:
            print("\n[!] Manual /sitemap.xml deneniyor...")
            self.found_sitemaps = [f"{self.base_url}/sitemap.xml"]
        
        print(f"\n[*] {len(self.found_sitemaps)} sitemap işleniyor...\n")
        
        for sitemap_url in self.found_sitemaps:
            # URL'yi düzelt
            if sitemap_url.startswith('http'):
                full_url = sitemap_url
            else:
                full_url = f"{self.base_url}{sitemap_url}"
            
            print(f"[→] İndiriliyordu: {full_url}")
            response = self._make_request(full_url)
            
            if response and response.status_code == 200:
                print(f"[+] Başarılı!")
                
                # Text olarak oku, regex ile URL'leri çıkar
                urls = self._extract_urls_from_text(response.text)
                
                self.all_urls.extend(urls)
                print(f"    └─ {len(urls)} URL bulundu")
            else:
                status = response.status_code if response else "Hata"
                print(f"[-] Başarısız ({status})\n")
        
        return len(self.all_urls) > 0
    
    def _extract_urls_from_text(self, text):
        """Text'ten regex ile URL'leri çıkar"""
        # https:// veya http:// ile başlayan URL'leri bul
        url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]*'
        matches = re.findall(url_pattern, text)
        
        urls = []
        seen = set()
        
        for url in matches:
            # Temizle (sonda nokta veya virgül varsa çıkar)
            url = url.rstrip('.,;:\'")]}>')
            
            # Duplikasyondan kurtul
            if url not in seen:
                seen.add(url)
                urls.append({
                    'url': url,
                    'lastmod': 'N/A',
                    'changefreq': 'N/A',
                    'priority': 'N/A'
                })
        
        return urls
    
    def analyze_urls(self):
        """URL'leri analiz et"""
        if not self.all_urls:
            print("[-] URL bulunamadı!")
            return None, None
        
        print(f"\n[*] {len(self.all_urls)} URL analiz ediliyor...\n")
        
        important_urls = []
        normal_urls = []
        
        for url_data in self.all_urls:
            url = url_data['url']
            is_important, keyword = self._check_important(url)
            
            if is_important:
                url_data['keyword_found'] = keyword
                important_urls.append(url_data)
            else:
                normal_urls.append(url_data)
        
        return important_urls, normal_urls
    
    def _check_important(self, url):
        """URL'de önemli kelime var mı kontrol et"""
        url_lower = url.lower()
        for keyword in IMPORTANT_KEYWORDS:
            if keyword in url_lower:
                return True, keyword
        return False, None
    
    def save_to_csv(self, important_urls, normal_urls):
        """Sonuçları CSV dosyasına kaydet"""
        domain_name = self.base_url.replace('https://', '').replace('http://', '').split('/')[0]
        filename = f"{domain_name}_sitemap_analysis.csv"
        
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                
                # Başlık
                writer.writerow(['URL', 'Tür', 'Bulunan Kelime'])
                
                # Önemli URL'ler
                for url_data in important_urls:
                    writer.writerow([
                        url_data['url'],
                        'ÖNEMLİ',
                        url_data['keyword_found']
                    ])
                
                # Normal URL'ler
                for url_data in normal_urls:
                    writer.writerow([
                        url_data['url'],
                        'NORMAL',
                        '-'
                    ])
            
            print(f"\n[+] Kaydedildi: {filename}")
            return filename
        except Exception as e:
            print(f"[-] Dosya hatası: {e}")
            return None
    
    def print_results(self, important_urls, normal_urls):
        """Sonuçları ekrana yazdır"""
        print("\n" + "="*80)
        print("ÖZET")
        print("="*80)
        print(f"[+] Toplam URL: {len(self.all_urls)}")
        print(f"[!] Önemli URL: {len(important_urls)}")
        print(f"[-] Normal URL: {len(normal_urls)}")
        
        # Önemli URL'leri göster
        if important_urls:
            print("\n" + "="*80)
            print("[!] ÖNEMLİ URL'LER (BUG BOUNTY) 🔴")
            print("="*80)
            for i, url_data in enumerate(important_urls, 1):
                print(f"{i:3d}. [{url_data['keyword_found']:12s}] {url_data['url']}")
        
        # Normal URL'leri göster (ilk 20'si)
        if normal_urls:
            print("\n" + "="*80)
            print("[*] DİĞER URL'LER")
            print("="*80)
            display_count = min(20, len(normal_urls))
            for i, url_data in enumerate(normal_urls[:display_count], 1):
                print(f"{i:3d}. {url_data['url']}")
            
            if len(normal_urls) > display_count:
                print(f"\n    ... ve {len(normal_urls) - display_count} tane daha (CSV dosyasında tümü var)")
    
    def run(self):
        """Ana çalıştırma fonksiyonu"""
        print("="*80)
        print("SITEMAP ANALIZ ARACI v3.0 - REGEX BASED URL EXTRACTOR")
        print("="*80)
        print(f"\n[*] Domain: {self.base_url}")
        
        # robots.txt'te sitemap ara
        robots_found = self.find_sitemaps_in_robots()
        
        # Sitemap'leri indir
        if not self.download_sitemaps():
            print("[-] Sitemap veya URL bulunamadı!")
            return
        
        # URL'leri analiz et
        important_urls, normal_urls = self.analyze_urls()
        
        if important_urls is None:
            print("[-] Analiz başarısız!")
            return
        
        # Sonuçları ekrana yazdır
        self.print_results(important_urls, normal_urls)
        
        # CSV'ye kaydet
        self.save_to_csv(important_urls, normal_urls)
        
        print("\n[+] İşlem tamamlandı!")

def main():
    print()
    domain = input("[?] Domain gir (örn: example.com): ").strip()
    
    if not domain:
        print("[-] Domain boş!")
        return
    
    analyzer = SitemapAnalyzer(domain)
    analyzer.run()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[-] İptal edildi (Ctrl+C)")
        sys.exit(0)
    except Exception as e:
        print(f"\n[-] Hata: {e}")
        sys.exit(1)