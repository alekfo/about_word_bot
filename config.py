from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
APP_KEY = os.getenv('YANDEX_KEY')
APP_URL = os.getenv('YANDEX_URL')

if not BOT_TOKEN:
    raise ValueError("Ошибка конфигурации: BOT_TOKEN не найден. Проверьте файл .env")

