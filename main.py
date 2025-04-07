import asyncio
import requests
from bs4 import BeautifulSoup
from telegram import Bot

# === Cấu hình bot ===
TOKEN = '7480548667:AAGFT6pEYlSGw2JSbCSC82fTd63C0lJNWzc'
CHAT_ID = '6182003634'
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
        await asyncio.sleep(600)  # 10 phút
        new_data = fetch_data()
        if new_data is None:
            await bot.send_message(chat_id=CHAT_ID, text="⚠️ Lỗi khi cập nhật dữ liệu.")
            continue

        if new_data != last_data:
            message = "🔔 Có DN mới trên website: https://internship.cse.hcmut.edu.vn/"
            try:
                await bot.send_message(chat_id=CHAT_ID, text=message)
                last_data = new_data
            except Exception as e:
                await bot.send_message(chat_id=CHAT_ID, text="❌ Lỗi khi gửi thông báo")

if __name__ == '__main__':
    asyncio.run(run_bot())
