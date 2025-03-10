import logging
import requests
from bs4 import BeautifulSoup

class SecurityAnalyzer:
    def _init_(self, url):
        self.url = url
        self.report = []

    def scan_all(self):
        self.check_sql_injection()
        self.check_xss()
        self.check_csrf()
        self.check_file_upload()
        self.scan_hidden_paths()
        self.extract_sensitive_data()
        self.check_lfi()
        self.check_idor()
        self.analyze_site_structure()
        self.detect_technologies()
        self.find_creator_info()
        return "\n".join(self.report)

    def check_sql_injection(self):
        try:
            payloads = ["' OR '1'='1", "' OR '1'='1' --", "' OR '1'='1' #", "' OR '1'='1' /*"]
            for payload in payloads:
                response = requests.get(self.url + f"/search?id={payload}", timeout=10)
                if "error" in response.text.lower() or "sql" in response.text.lower():
                    self.report.append(f"[!] SQL Açığı Bulundu! (Payload: {payload})")
                    logging.info(f"SQL Açığı Bulundu: {self.url} - Payload: {payload}")
                    return True
            self.report.append("[+] SQL Açığı Yok")
            return False
        except Exception as e:
            self.report.append(f"[-] SQL Kontrolü Başarısız: {e}")
            logging.error(f"SQL Kontrolü Başarısız: {e}")
            return False

    # Diğer fonksiyonlar buraya eklenecek...

    def analyze_site_structure(self):
        try:
            response = requests.get(self.url, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            title = soup.title.string if soup.title else "Başlık bulunamadı"
            meta_description = soup.find("meta", attrs={"name": "description"})
            description = meta_description["content"] if meta_description else "Açıklama bulunamadı"
            self.report.append("[*] Site Yapısı Analizi:")
            self.report.append(f"- Başlık: {title}")
            self.report.append(f"- Açıklama: {description}")
            logging.info(f"Site Yapısı Analizi: {self.url} - Başlık: {title}, Açıklama: {description}")
        except Exception as e:
            self.report.append(f"[-] Site Yapısı Analizi Başarısız: {e}")
            logging.error(f"Site Yapısı Analizi Başarısız: {e}")

    def detect_technologies(self):
        try:
            response = requests.get(self.url, timeout=10)
            headers = response.headers
            server = headers.get("Server", "Bilinmiyor")
            x_powered_by = headers.get("X-Powered-By", "Bilinmiyor")
            self.report.append("[*] Kullanılan Teknolojiler:")
            self.report.append(f"- Sunucu: {server}")
            self.report.append(f"- X-Powered-By: {x_powered_by}")
            logging.info(f"Kullanılan Teknolojiler: {self.url} - Sunucu: {server}, X-Powered-By: {x_powered_by}")
        except Exception as e:
            self.report.append(f"[-] Teknoloji Tespiti Başarısız: {e}")
            logging.error(f"Teknoloji Tespiti Başarısız: {e}")

    def find_creator_info(self):
        try:
            response = requests.get(self.url, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            creator_info = soup.find("meta", attrs={"name": "author"})
            creator = creator_info["content"] if creator_info else "Kurucu bilgisi bulunamadı"
            self.report.append("[*] Kurucu Bilgisi:")
            self.report.append(f"- Kurucu: {creator}")
            logging.info(f"Kurucu Bilgisi: {self.url} - Kurucu: {creator}")
        except Exception as e:
            self.report.append(f"[-] Kurucu Bilgisi Bulunamadı: {e}")
            logging.error(f"Kurucu Bilgisi Bulunamadı: {e}")

def analyze_url(url):
    analyzer = SecurityAnalyzer(url)
    return analyzer.scan_all()