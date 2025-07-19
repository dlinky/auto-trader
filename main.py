# main.py
from src.utils.logger import setup_logger
from src.utils.trade_logger import TradeLogger
from src.api.binance_client import BinanceClient

# 로거 초기화
trade_logger = TradeLogger()
client = BinanceClient()

class SimpleTrader:
    def __init__(self):
        self.client = BinanceClient()
        self.trade_logger = TradeLogger()
    
    def enter_long_position(self, symbol, strategy, amount, stop_loss_pct=0.05):
        """롱 포지션 진입 + 스탑로스 설정"""
        try:
            # 1. 롱 포지션 진입
            entry_order = self.client.exchange.create_market_order(
                symbol=symbol,
                side='buy',
                amount=amount
            )
            
            entry_price = entry_order['average']
            print(entry_order['id'])
            self.trade_logger.log_order("진입", symbol, strategy, "buy", amount, entry_price)
            
            # 2. 즉시 스탑로스 설정 (진입가 기준 -5%)
            stop_price = entry_price * (1 - stop_loss_pct)
            
            self.client.create_stop_loss_order(
                symbol=symbol,
                strategy=strategy,
                stop_price=stop_price,
                side='sell',  # 롱포지션이므로 매도로 손절
                quantity=amount
            )
            
            return entry_order
            
        except Exception as e:
            self.trade_logger.error(f"롱 포지션 진입 실패: {e}")
            return None
    
    def enter_short_position(self, symbol, strategy, amount, stop_loss_pct=0.05):
        """숏 포지션 진입 + 스탑로스 설정"""
        try:
            # 1. 숏 포지션 진입
            entry_order = self.client.exchange.create_market_order(
                symbol=symbol,
                side='sell',
                amount=amount
            )
            
            entry_price = entry_order['average']
            print(entry_order['id'])
            self.trade_logger.log_order("진입", symbol, strategy, "sell", amount, entry_price)
            
            # 2. 즉시 스탑로스 설정 (진입가 기준 +5%)
            stop_price = entry_price * (1 + stop_loss_pct)
            
            self.client.create_stop_loss_order(
                symbol=symbol,
                strategy=strategy,
                stop_price=stop_price,
                side='buy',  # 숏포지션이므로 매수로 손절
                quantity=amount
            )
            
            return entry_order
            
        except Exception as e:
            self.trade_logger.error(f"숏 포지션 진입 실패: {e}")
            return None

symbol = "XRP/USDT:USDT"
strategy = "test"
trader = SimpleTrader()
trader.enter_long_position(symbol, strategy, trader.client.get_min_amount(symbol), 0.05)
trader.enter_short_position(symbol, strategy, trader.client.get_min_amount(symbol), 0.05)