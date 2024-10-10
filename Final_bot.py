import telebot
import json
from final_config import keys, TOKEN
from extensions import APIException, CryptoConverter

bot = telebot.TeleBot(TOKEN)

# Обработчик команд /start и /help
@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    # Сообщение с информацией о формате ввода команды
    text = 'Чтобы начать работу введите команду боту в слеующем формате:\n<имя валюты>  \
<в какую валюту перевести> \
<количество переводимой валюты>\nУвидить список доступных валют: /values'
    bot.reply_to(message, text)  # Ответ пользователю

# Обработчик команды /values
@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    # Формируем сообщение со списком доступных валют
    text = 'Доступные валюты:'
    for key in keys.keys():  # Перебираем все ключи в словаре
        text = '\n' .join((text, key, ))  # Добавляем валюту в текст
    bot.reply_to(message, text)  # Ответ пользователю с доступными валютами

# Обработчик текстовых сообщений
@bot.message_handler(content_types=['text'], )
def convert(message: telebot.types.Message):
    try:
        # Разбиваем текст сообщения на части
        values = message.text.split(' ')

        # Проверяем, что введено ровно три параметра
        if len(values) != 3:
            raise APIException('Слишком много параметров')

        quote, base, amount = values  # Извлекаем валюты и сумму из сообщения
        total_base = CryptoConverter.get_price(quote, base, amount)  # Вызываем метод для получения суммы преобразования
    except APIException as e:
        # Обработка пользовательских ошибок
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        # Обработка других исключений
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')

    else:
        # Формируем и отправляем ответ пользователю
        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)

bot.polling()