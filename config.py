from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
APP_KEY = os.getenv('YANDEX_KEY')
APP_URL = os.getenv('YANDEX_URL')
DB_PATH = os.getenv('DB_PATH')
ADMIN_ID = os.getenv('ADMIN_ID')

if not BOT_TOKEN:
    raise ValueError("Ошибка конфигурации: BOT_TOKEN не найден. Проверьте файл .env")

