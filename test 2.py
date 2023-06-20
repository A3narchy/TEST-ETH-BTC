from binance.client import Client
import pandas as pd
from config import api_key, secret_key
import datetime
import time

client = Client(api_key, secret_key)


class Coin:
    @staticmethod
    def get_coin_data(symbol, limit=61):
        # Получение данных о цене валюты с биржи Binance
        data = client.get_klines(symbol=symbol, interval=Client.KLINE_INTERVAL_1MINUTE, limit=limit)

        df = pd.DataFrame()

        # Преобразование данных в DataFrame
        for candle in range(limit):
            timestamp = data[candle][0]
            date_time = datetime.datetime.fromtimestamp(timestamp / 1000)
            close_price = float(data[candle][4])
            new_df = pd.DataFrame({'Time': [date_time], f'{symbol}': [close_price]})
            df = pd.concat([df, new_df], ignore_index=True)
        return df


def calculate_change(symbol):
    # Получение данных о цене валюты
    data = Coin.get_coin_data(symbol)

    # Расчет изменения цены
    max_price = data[symbol].max()
    min_price = data[symbol].min()
    price_change = (max_price - min_price) / min_price

    # Расчет "скорректированного" изменения цены ETH
    if price_change >= 0.01:
        return True
    
    return False


def monitor_changes(symbol, interval=60):
    # Проверка изменений цены по первичному датафрейму
    if calculate_change(symbol):
        print("Цена менялась более чем на 1% за прошедший час")
    else:
        print("За час цена не менялась на 1%+")

    # Проверка изменений цены в цикле каждую минуту
    while True:
        time.sleep(interval)

        if calculate_change(symbol):
            print("Цена изменилась более чем на 1%")
        else:
            print("За час цена не менялась на 1%+")

        # Вывод прогресса
        print("Прошло {} минут".format(interval/60))