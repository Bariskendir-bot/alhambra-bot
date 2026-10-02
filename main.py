import os
import time
from threading import Thread
from http.server import HTTPServer, BaseHTTPRequestHandler
from curl_cffi import requests

# Render'ın servisi kapatmasını önleyecek sahte web sunucusu
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Alhambra Bot Aktif!")

def run_web_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(('0.0.0.0', port), SimpleHTTPRequestHandler)
    server.serve_forever()

# Web sunucusunu arka planda başlat
Thread(target=run_web_server, daemon=True).start()

# --- Telegram Bilgileri ---
TELEGRAM_TOKEN = "8659750495:AAHGbqBjPzJWwe2pSITIsEa7hrMn-ZY0XJ0"
CHAT_ID = "5899841533"

URL = "https://tickets.alhambra-patronato.es/"
TARGET_DATE = "2026-10-27"

def send_telegram_msg(message):
    telegram_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
    try:
        requests.post(telegram_url, data=payload)
    except Exception as e:
        print(f"Telegram hatasi: {e}")

# İlk açılış test bildirimi
send_telegram_msg("🏰 *Alhambra Sarayı Bilet Botu Aktif!*\n📅 *27 Ekim 2026 (12:00 Sonrası)* izleniyor.")

while True:
    try:
        # Cloudflare engelini aşmak için Chrome tarayıcı taklidi
        response = requests.get(URL, impersonate="chrome120", timeout=15)
        
        if response.status_code == 200:
            content = response.text
            
            # 27 Ekim tarihi veya bilet açılışı sayfaya yansıdı mı kontrol et
            if TARGET_DATE in content or "27/10/2026" in content:
                msg = f"🚨 *ALHAMBRA SARAYI BİLET ALARMI!*\n\n📅 *27 Ekim 2026* için hareketlilik tespit edildi!\n🔗 Hemen kontrol et: {URL}"
                send_telegram_msg(msg)
                print("Bilet hareketi bulundu, bildirim atildi!")
            else:
                print("27 Ekim biletleri henüz görünmüyor, taranıyor...")
        else:
            print(f"Siteye erişim kısıtlandı veya hata alındı, Kod: {response.status_code}")
            
    except Exception as e:
        print(f"Hata oluştu: {e}")
    
    # 3 dakikada bir kontrol eder
    time.sleep(180)
