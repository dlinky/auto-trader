import api.binance_client
from api.binance_client import BinanceClient
from utils.logger import setup_logger

class TraderManager:
    def __init__(self, use_testnet=False):
        self.traders = {}
        self.use_testnet = use_testnet
        self.symbols = []
        self.add_trader(0, 'BTC/USDT:USDT', None, False)
        self.fetch_trader = BinanceClient()

    def add_trader(self, trader_id, symbol, strategy, use_testnet):
        self.traders[trader_id] = BinanceClient(trader_id, symbol, strategy, use_testnet)
        self.update_trading_symbols()

    def remove_trader(self, trader_id):
        del self.traders[trader_id]
        self.update_trading_symbols()

    def clear_all_traders(self):
        del self.traders

    def update_trading_symbols(self):
        self.symbols = [_.symbol for _ in self.traders.values()]

    def get_all_ohlcvs(self, interval='1m', limit=1):
        ohlcvs = []
        for symbol in self.symbols:
            ohlcv = None
            while ohlcv is None:
                ohlcv = self.fetch_trader.exchange.fetch_ohlcv(symbol, interval, limit)
            ohlcvs.append(ohlcv)
        return ohlcvs


if __name__ == '__main__':
    trader_manager = TraderManager()
    ohlcvs = trader_manager.get_all_ohlcvs()
    print(ohlcvs)