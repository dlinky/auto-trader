import ccxt
import pandas as pd
import numpy as np
import time
import json
import os
from datetime import datetime, timedelta
import itertools
from typing import Dict, List, Tuple, Optional, Any
import threading
import sys
import pprint
from dotenv import load_dotenv

load_dotenv

binance = ccxt.binance({
    'apiKey': os.getenv('BINANCE_API_KEY'),
    'secret': os.getenv('BINANCE_SECRET_KEY'),
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

print("fetching balance...", end="", flush=True)
balance = binance.fetch_balance()
usdt_balance = balance['USDT']
pprint.pprint(usdt_balance)