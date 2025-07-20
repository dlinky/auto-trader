import os
import logging
import ccxt
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('trader.log'),
        logging.StreamHandler()
    ]
)

class BinanceClient:
    def __init__(self, use_testnet=False):
        if use_testnet:
            api_key = os.getenv('BINANCE_TESTNET_API_KEY')
            api_secret = os.getenv('BINANCE_TESTNET_API_SECRET')
            sandbox = True
        else:
            api_key = os.getenv('BINANCE_API_KEY')
            api_secret = os.getenv('BINANCE_API_SECRET')
            sandbox = False

        if not api_key or not api_secret:
            raise ValueError("API 키가 설정되지 않았습니다")
        
        config = {
            'apiKey': api_key,
            'secret': api_secret,
            'enableRateLimit': True,
            'options': {
                'defaultType': 'future'
            },
            'sandbox': sandbox,
        }

        self.exchange = ccxt.binance(config)
        self.logger = logging.getLogger(__name__)
    
    def check_environment(self):
        try:
            account_info = self.exchange.fetch_balance()
            if 'testnet' in str(self.exchange.urls):
                print("테스트넷 환경")
            else:
                print("실제 거래 환경")
        except Exception as e:
            print(f"환경 확인 실패 : {e}")

    def get_balance(self):
        balance = self.exchange.fetch_balance()
        usdt_balance = balance['USDT']
        print(usdt_balance)

    def get_position(self, symbol):
        resp = self.exchange.fetch_open_orders(symbol=symbol)
    
    def get_all_positions(self):
        """모든 포지션 조회 (0이 아닌 것만)"""
        try:
            positions = self.exchange.fetch_positions()
            active_positions = [pos for pos in positions if pos['contracts']> 0]

            self.logger.info(f"활성 포지션 {len(active_positions)}개 조회됨")
            for pos in active_positions:
                self.logger.info(f"포지션: {pos['symbol']} | 수량: {pos['contracts']} | PnL: {pos['unrealizedPnl']}")
            
            return active_positions
        except Exception as e:
            self.logger.error(f"포지션 조회 실패: {e}")
            return []
        
    def close_position(self, symbol, strategy, side='market'):
        """포지션 전체 청산"""
        try:
            position = self.exchange.fetch_position(symbol)
            if position['contracts'] == 0:
                self.logger.warning(f"{symbol} 포지션이 없습니다.")
                return False
            
            side_to_close = 'sell' if position['side'] == 'long' else 'buy'
            amount = abs(position['contracts'])

            order = self.exchange.create_market_order(
                symbol=symbol,
                side=side_to_close,
                amount=amount,
                params={'reduceOnly': True}
            )
            
            self.logger.info(f"포지션 청산 성공: {symbol} | {strategy}, 수량: {amount} | 주문ID: {order['id']}")
            return order
        
        except Exception as e:
            self.logger.error(f"포지션 청산 실패 {symbol}: {e}")
            return None
        
    def set_leverage(self, symbol, strategy, leverage):
        try:
            result = self.exchange.set_leverage(leverage, symbol)
            self.logger.info(f"레버리지 설정 완료: {symbol} | {strategy} | x{leverage}")
            return result
        except Exception as e:
            self.logger.error(f"레버리지 설정 실패 {symbol}: {e}")
            return None
    
    def get_min_amount(self, symbol):
        symbol_text = symbol.split(':')[0]
        market = self.exchange.load_markets()[symbol_text]
        market_limit = market['limits']
        market_precision = market['precision']
        ticker = self.exchange.fetch_ticker(symbol)

        limit_min_amount = market_limit['amount']['min']
        limit_min_cost = market_limit['cost']['min']
        current_price = ticker['last']
        min_amount_by_cost = float(self.exchange.amount_to_precision(symbol, limit_min_cost/current_price))+market_precision['amount']
        real_min_amount = max(limit_min_amount, min_amount_by_cost)

        return real_min_amount
    
    def get_ticker(self, symbol):
        tickers = self.exchange.fetch_tickers()
        print(tickers[symbol])

    def create_stop_loss_order(self, symbol, strategy, stop_price, side, quantity=None):
        try:
            order = self.exchange.create_order(
                symbol=symbol,
                type='stop_market',
                side=side,
                amount=quantity,
                params={
                    'stopPrice': stop_price,
                    'reduceOnly': True
                }
            )

            self.logger.info(f"스탑로스 설정: {symbol} | {strategy} | 손절가: {stop_price} | 수량: {quantity}")
            return order
        
        except Exception as e:
            self.logger.error(f"스탑로스 설정 실패 {symbol} | {strategy}: {e}")
            return None

def main():
    symbol = "XRP/USDT:USDT"
    client = BinanceClient(use_testnet=True)
    client.check_environment()
    client.get_balance()
    client.get_position(symbol)

    min_amount = client.get_min_amount(symbol)
    resp = client.exchange.create_market_buy_order(symbol, min_amount)
    print('orderId = ', resp['info']['orderId'])

if __name__=="__main__":
    main()