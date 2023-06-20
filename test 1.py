from binance.client import Client
import pandas as pd
from config import api_key, secret_key

client = Client(api_key, secret_key)

class AssessmentModel:

    def __init__(self, symbol1, symbol2):
        self.symbol1 = symbol1
        self.symbol2 = symbol2

    def get_price_df(self, symbol):
        # Получение данных о ценах для символа с помощью Binance API
        data = client.futures_klines(symbol=symbol, interval=Client.KLINE_INTERVAL_1DAY, limit=1000)
        
        # Преобразование данных в DataFrame с использованием pandas
        df = pd.DataFrame(data, columns=["Open Time", "Open", "High", "Low", "Close", "Volume", "Close Time", "Quote Asset Volume", "Number of Trades", "Taker Buy Base Asset Volume", "Taker Buy Quote Asset Volume", "Ignore"])
        
        # Преобразование значений столбцов в числовой формат
        df['Close'] = df['Close'].astype(float)
        df['High'] = df['High'].astype(float)
        df['Low'] = df['Low'].astype(float)
        df['Open'] = df['Open'].astype(float)
        
        # Преобразование времени открытия в формат datetime и установка его в качестве индекса DataFrame
        df['Open Time'] = pd.to_datetime(df['Open Time'], unit='ms')
        df.set_index('Open Time', inplace=True)
        
        return df[['Open', 'High', 'Low', 'Close']]

    def calculate_r_squared(self):
        # Получение данных о ценах для каждого символа
        df1 = self.get_price_df(self.symbol1)
        df2 = self.get_price_df(self.symbol2)
        
        # Слияние двух DataFrame по времени открытия
        merged_df = pd.merge(df1, df2, left_index=True, right_index=True)
        
        total_iterations = len(merged_df)
        iteration = 0
        
        print("Расчет R-квадрата:")
        
        for _ in merged_df.iterrows():
            # Расчет корреляции и R-квадрата для каждой итерации
            corr = merged_df.iloc[iteration]['Close_x'].corr(merged_df.iloc[iteration]['Close_y'])
            r_squared = corr ** 2
            iteration += 1
            progress = f"Прогресс: {iteration}/{total_iterations}"
            print(progress, end="\r")
        
        print()
        return r_squared

# Создание экземпляра класса AssessmentModel с символами ETHUSDT и BTCUSDT
model = AssessmentModel("ETHUSDT", "BTCUSDT")

# Расчет R-квадрата
r_squared = model.calculate_r_squared()
print(f"R-квадрат: {r_squared}")
