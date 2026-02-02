#!/usr/bin/env python3
import requests
import csv
import re
import sys
import time

# ================== CLI STYLE ==================
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"

def info(m): print(f"{BLUE}[*]{RESET} {m}")
def good(m): print(f"{GREEN}[+]{RESET} {m}")
def warn(m): print(f"{YELLOW}[!]{RESET} {m}")
def bad(m):  print(f"{RED}[-]{RESET} {m}")

# ================== CONFIG ==================
IMPORTANT_KEYWORDS = [
    'admin','login','api','config','private','dashboard','panel',
    'wp-admin','administrator','auth','token','secret','key',
    'backup','db','database','debug','test','dev','staging'
]

TIMEOUT = 10
MAX_RETRIES = 3
HEADERS = {
    "User-Agent": "WPScan/3.8.24 (https://wpscan.com/)"
}

# ================== ANALYZER ==================
class AnalyzerSimple:
    def __init__(self, domain):
        self.base = self._normalize(domain)
        self.sitemaps = []
        self.urls = []

    def _normalize(self, d):
        if not d.startswith("http"):
            d = "https://" + d
        return d.rstrip("/")

    def _request(self, url):
        for i in range(MAX_RETRIES):
            try:
                return requests.get(url, timeout=TIMEOUT, headers=HEADERS)
            except requests.RequestException:
                warn(f"Request failed ({i+1}/{MAX_RETRIES})")
                time.sleep(1)
        return None

    def find_sitemaps(self):
        info("Checking robots.txt for sitemaps")
        r = self._request(f"{self.base}/robots.txt")
        if not r or r.status_code != 200:
            warn("robots.txt not found")
            return

        for line in r.text.splitlines():
            if line.lower().startswith("sitemap:"):
                sm = line.split(":", 1)[1].strip()
                self.sitemaps.append(sm)
                good(f"Sitemap found: {sm}")

    def download_sitemaps(self):
        if not self.sitemaps:
            info("Trying default /sitemap.xml")
            self.sitemaps = [f"{self.base}/sitemap.xml"]

        for sm in self.sitemaps:
            url = sm if sm.startswith("http") else self.base + sm
            info(f"Fetching sitemap: {url}")
            r = self._request(url)
            if r and r.status_code == 200:
                found = self._extract_urls(r.text)
                self.urls.extend(found)
                good(f"{len(found)} URLs extracted")
            else:
                bad("Failed to fetch sitemap")

    def _extract_urls(self, text):
        pattern = r'https?://[^\s<>"\']+'
        return list(set(re.findall(pattern, text)))

    def analyze(self):
        info(f"Analyzing {len(self.urls)} URLs")
        important, normal = [], []

        for u in self.urls:
            hit = next((k for k in IMPORTANT_KEYWORDS if k in u.lower()), None)
            if hit:
                important.append((u, hit))
            else:
                normal.append(u)

        return important, normal

    def save_csv(self, important, normal):
        fname = self.base.replace("https://", "").replace("/", "") + "_analysis.csv"
        with open(fname, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["URL", "Type", "Keyword"])
            for u, k in important:
                w.writerow([u, "IMPORTANT", k])
            for u in normal:
                w.writerow([u, "NORMAL", "-"])
        good(f"Results saved to {fname}")

    def run(self):
        info(f"Target: {self.base}")
        self.find_sitemaps()
        self.download_sitemaps()

        if not self.urls:
            bad("No URLs found")
            return

        important, normal = self.analyze()

        print("\n[+] Interesting URLs Found:")
        for i, (u, k) in enumerate(important, 1):
            print(f" {i:02d}. [{k}] {u}")

        info(f"Total URLs: {len(self.urls)}")
        info(f"Important URLs: {len(important)}")

        self.save_csv(important, normal)

# ================== MAIN ==================
def main():
    domain = input("[?] Target URL (example.com): ").strip()
    if not domain:
        bad("No target provided")
        return
    AnalyzerSimple(domain).run()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        bad("Scan aborted")
        sys.exit(0)
