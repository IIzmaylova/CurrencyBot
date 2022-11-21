import requests
import json
from config import currency

# Создаем класс исключений для вывода ошибок со стороны пользователя
class APIException(Exception):
    pass

##########

# Для отправки запросов к API создаем класс со статическим методом get_price(),принимающий три аргумента:
# имя переводимой валюты, имя валюты, цену в которой надо узнать,количество переводимой валюты
# и возвращающий нужную сумму в валюте.
class CurrencyConverter():
    @staticmethod
    def get_price(base_ticker: str, quote_ticker: str, amount: str):
        try:
            # Делаем запрос к API для получения котировки валюты и сохраняем результат в словарь
            r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={base_ticker}&tsyms={quote_ticker}')
            quotation = json.loads(r.content)[currency[quote_ticker]]
            # Присваиваем переменной итоговую стоимость с учетом количества переводимой валюты
            # Округляем до двух знаков после запятой
            total_quote = round(quotation * amount, 2)
        except Exception as e:
            raise Exception ('Что-то пошло не так...')
        else:
        # Возвращаем
            return total_quote

##########

class Validation():
    # Для проверки соотвествия ввода пользователя шаблону программы создаем метод parametrs(),
    # который принимает один параметр текст сообщения пользователя,
    # возвращает три параметра base_ticker, quote_ticker, amount
    @staticmethod
    def request_template(user_message):
        try:
            # Разбиваем сообщение пользователя по пробелам и сохраняем в массив
            values = user_message.split()
            # Вызываем исключение, если пользователь ввел менее или более трех параметров
            if len(values) != 3:
                raise APIException('Введите три параметра:\n'
                '<имя валюты> <в какую валюту перевести> <количество переводимой валюты>\n'
                'Например: доллар рубль 100')
            # Выводим сообщения для пользователя в случае ошибки
        except APIException as e:
            raise APIException (f'Неверное количество параметров.\n{e}')
        # Отправляем пользователю результат конвертации выбранной им валюты
        else:
            # Последовательно присваиваем переменным base, quote, amount значения, введенные пользователем
            base, quote, amount = values
            # Переводим имена валют в поддерживаемый API формат
            base_ticker, quote_ticker = Validation.currency_name(base, quote)
            # Проверяем, что пользователь использует только положительные числовые значения для количества валюты
            amount = Validation.currency_amount(amount)
            # Возращаем прошедшие проверку параметры
            return base_ticker, quote_ticker, amount

    # Метод принимает два аргумента: имя валюты, цену на которую надо узнать, — base,
    #  имя валюты, цену в которой надо узнать, — quote,
    #  возвращает преобразованные в корректные для API имена валют
    @staticmethod
    def currency_name(base: str, quote: str):
        # Проверяем, что пользователь вводит доступные для конвертации валюты
        try:
            base_ticker = currency[base.upper()]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту "{base}"\nСписок доступных валют: /values')
        try:
            quote_ticker = currency[quote.upper()]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту "{quote}"\nСписок доступных валют: /values')
        # Проверяем, что пользователь не переводит валюту в саму себя
        if quote_ticker == base_ticker:
            raise APIException(f'Невозможно перевести валюту "{base}" в саму себя')
        return base_ticker, quote_ticker

    # Метод принимает один аргумент amount, если передано число >= 0 возращает float(amount)
    @staticmethod
    def currency_amount(amount):
        try:
            amount = float(amount)
            # Вызываем исключение, если введено отрицательное число
            if amount < 0:
                raise APIException('Пожалуйста, указывая количество валюты, не используйте отрицательные значения')
        # Вызываем исключение, если введено не число
        except ValueError:
            raise APIException(f'Не удалось обработать количество \"{amount}\".\n\
        Пожалуйста, указывая количество валюты, используйте только числа')
        #  Выводим сообщение об ошибке, если введено отрицательно значение
        except APIException as e:
            raise APIException(f'Не удалось обработать количество \"{amount}\".\n{e}')
        else:
            return amount

##########

# Создаем класс, обрабатывающий комманды пользователя
class Commands():
    # Метод возвращает все доступные валюты
    @staticmethod
    def values():
        text = 'Доступные валюты:'
        for c in currency['available']:
            text = '\n'.join((text, c,))
        return text

    # Метод возвращает инструкцию к приложению
    @staticmethod
    def help():
        text = 'Чтобы начать работу введите команду в следующем формате:\n' \
               '<имя валюты> <в какую валюту перевести> <количество переводимой валюты>\n' \
               'Увидеть список всех доступных валют: /values'
        return text

