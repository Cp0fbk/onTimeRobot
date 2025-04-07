import os
import asyncio
import requests
from bs4 import BeautifulSoup
from telegram import Bot
from http.server import SimpleHTTPRequestHandler, HTTPServer

# === Cấu hình bot từ biến môi trường ===
TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
URL = 'https://internship.cse.hcmut.edu.vn/'

bot = Bot(token=TOKEN)

def fetch_data():
    try:
        response = requests.get(URL, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        data_section = soup.find('div', class_='news-list')
        return data_section.get_text(strip=True) if data_section else ""
    except Exception as e:
        print("Lỗi khi lấy dữ liệu:", e)
        return None

async def run_bot():
    last_data = fetch_data()
    if last_data is None:
        await bot.send_message(chat_id=CHAT_ID, text="❌ Không thể lấy dữ liệu ban đầu.")
        return

    while True:
        await asyncio.sleep(600)
        new_data = fetch_data()
        if new_data is None:
            await bot.send_message(chat_id=CHAT_ID, text="⚠️ Lỗi khi cập nhật dữ liệu.")
            continue

        if new_data != last_data:
            message = "🔔 Có DN mới trên website: https://internship.cse.hcmut.edu.vn/"
            try:
                await bot.send_message(chat_id=CHAT_ID, text=message)
                last_data = new_data
            except Exception:
                await bot.send_message(chat_id=CHAT_ID, text="❌ Lỗi khi gửi thông báo")

if __name__ == '__main__':
    # Lấy cổng từ biến môi trường, nếu không có sẽ mặc định là 10000
    port = int(os.environ.get("PORT", 10000))
    print(f"Server is running on port {port}...")

    # Tạo một HTTP server trống để Render nhận diện cổng
    def run_http_server():
        server_address = ('', port)
        httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
        print(f'Starting HTTP server on port {port}...')
        httpd.serve_forever()

    # Chạy HTTP server trong một luồng riêng
    import threading
    threading.Thread(target=run_http_server, daemon=True).start()

    # Chạy bot Telegram
    asyncio.run(run_bot())
