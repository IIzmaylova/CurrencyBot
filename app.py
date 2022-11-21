import telebot
from telebot import types
from config import TOKEN
from extensions import APIException, Commands, Validation, CurrencyConverter

bot = telebot.TeleBot(TOKEN)

# Создаем обработчик сообщений для команды /start
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Доступные валюты")
    btn2 = types.KeyboardButton("Справка")
    markup.add(btn1, btn2)
    text = 'Привет, {0.first_name}!\nЧтобы начать работу введите команду в следующем формате:\n' \
           '<имя валюты> <в какую валюту перевести> <количество переводимой валюты>\n' \
           'Увидеть список всех доступных валют: /values'
    bot.send_message(message.chat.id, text.format(message.from_user), reply_markup=markup)

# Создаем обработчик сообщений для команды /help
@bot.message_handler(commands= ['help'])
def help(message: telebot.types.Message):
    text = Commands.help()
    bot.reply_to(message,text)

# Создаем обработчик для комманды /values
@bot.message_handler(commands= ['values'])
def values(message: telebot.types.Message):
    text = Commands.values()
    bot.reply_to(message,text)

# Создаем обработчик для сообщений пользователя
@bot.message_handler(content_types= ['text',])
def convert(message: telebot.types.Message):
        try:
            if (message.text == "Доступные валюты"):
                text = Commands.values()
            elif (message.text == "Справка"):
                text = Commands.help()
            else:
                user_message = message.text
                base_ticker, quote_ticker, amount = Validation.request_template(user_message)
                # Конвертируем валюту
                total_quote = CurrencyConverter.get_price(base_ticker, quote_ticker, amount)
                # Присвоиваем переменной
                text = f'{amount} {base_ticker} = {total_quote} {quote_ticker}'
        # Выводим сообщения для пользователя в случае ошибки
        except APIException as e:
            bot.reply_to(message, f'Ошибка ввода!\n{e}')
        except Exception as e:
            bot.reply_to(message, f'Не удалось обработать команду:\n{e}')
        # Отправляем пользователю результат конвертации выбранной им валюты
        else:
            bot.reply_to(message, text)


bot.polling(none_stop=True)