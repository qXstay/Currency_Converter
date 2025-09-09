import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')



keys = {             # Словарь для соответствия названий валют их кодам
    'евро': 'EUR',
    'доллар': 'USD',
    'рубль': 'RUB',
}
