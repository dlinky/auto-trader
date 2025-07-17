import ccxt
import os
from dotenv import load_dotenv

load_dotenv

binance = ccxt.binance({
    'apiKey': os.getenv('BINANCE_API_KEY'),
    'secret': os.getenv('BINANCE_API_SECRET'),
    'sandbox': False,
    'enableRateLimit': True,
    'options': {
        'defaultType': 'future',
    }
})

print("Crypto Auto Trader")

print("fetching tickers...", end=" ", flush=True)
markets = binance.load_markets()
tickers = binance.fetch_tickers()
symbols = tickers.keys()
usdt_symbols = [_ for _ in symbols if _.endswith('USDT')]
print(f"found {len(usdt_symbols)} tickers")

print("fetching balance...", end=" ", flush=True)
balance = binance.fetch_balance()
usdt_balance = balance['USDT']
print(usdt_balance)
usdt_free = usdt_balance['free']

usdt_in = usdt_free * 0.3
current_price = tickers['BTC/USDT:USDT']['ask']
if current_price is None:
    current_price = tickers['BTC/USDT:USDT']['last']
in_amount = usdt_in / current_price
formatted_amount = binance.amount_to_precision('BTC/USDT:USDT', in_amount)

print("trying to buy")
try:
    binance.create_order('BTC/USDT:USDT','MARKET','buy',formatted_amount,None)
except ccxt.NetworkError as e:
    print(f"네트워크 오류: {e}")
except ccxt.ExchangeError as e:
    print(f"거래소 오류: {e}")
except Exception as e:
    print(f"기타 오류: {e}")

print("trying to sell")
try:
    binance.create_order('BTC/USDT:USDT','MARKET','sell',formatted_amount,None)
except ccxt.NetworkError as e:
    print(f"네트워크 오류: {e}")
except ccxt.ExchangeError as e:
    print(f"거래소 오류: {e}")
except Exception as e:
    print(f"기타 오류: {e}")