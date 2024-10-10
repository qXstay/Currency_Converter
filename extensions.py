import requests
import json
from final_config import keys

# Класс для обработки исключений, связанных с API
class APIException(Exception):
    pass

# Класс для конвертации валют
class CryptoConverter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        # Проверяем, что валюты не одинаковы
        if quote == base:
            raise APIException(f'Невозможно паревести одинаковые валюты {base}.')

        # Попробуем получить код валюты для quote из словаря
        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {quote}.')

        # Попробуем получить код валюты для base из словаря
        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {base}.')

        try:  # Пробуем привести amount к типу float
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}.')

        # Выполняем запрос к API для получения текущего курса обмена
        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = json.loads(r.content)[keys[base]]   # Извлекаем стоимость обмена

        return total_base * amount   # Умножаем курс на количество для получения итоговой суммы