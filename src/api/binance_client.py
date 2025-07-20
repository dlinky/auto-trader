import os
import ccxt
from dotenv import load_dotenv
from src.utils.slack_bot import SlackBot

load_dotenv()

class BinanceClient:
    '''심볼/전략이 지정된 단일 거래소 클래스'''
    def __init__(self, id, symbol, strategy, use_testnet=False):
        self.trader_id = id
        self.symbol = symbol
        self.strategy = strategy

        # 계정 설정
        if use_testnet:
            api_key = os.getenv('BINANCE_TESTNET_API_KEY')
            api_secret = os.getenv('BINANCE_TESTNET_API_SECRET')
            sandbox = True
        else:
            api_key = os.getenv('BINANCE_API_KEY')
            api_secret = os.getenv('BINANCE_API_SECRET')
            sandbox = False

        if not api_key or not api_secret:
            raise ValueError("API_KEY_MISSING")
        
        # 계정 연결
        exchange_config = {
            'apiKey': api_key,
            'secret': api_secret,
            'enableRateLimit': True,
            'options': {
                'defaultType': 'future'
            },
            'sandbox': sandbox,
        }
        self.exchange = ccxt.binance(exchange_config)

        # 슬랙 봇 연결
        self.slack_bot =SlackBot()

    def set_leverage(self, leverage):
        try:
            result = self.exchange.set_leverage(leverage, self.symbol)
            self.logger.info(f"[id:{self.trader_id}][{self.symbol}][{self.strategy}] 레버리지 설정 완료: x{leverage}")
            return result
        except Exception as e:
            self.logger.error(f"[id:{self.trader_id}][{self.symbol}][{self.strategy}] 레버리지 설정 실패: {e}")
            return None
    
    def get_min_amount(self):
        '''주문하기 위한 최소수량 계산'''
        symbol_text = self.symbol.split(':')[0]
        market = self.exchange.load_markets()[symbol_text]
        market_limit = market['limits']
        market_precision = market['precision']
        ticker = self.exchange.fetch_ticker(self.symbol)

        # amount 기반, cost 기반 최소수량 중 큰 값을 반환
        limit_min_amount = market_limit['amount']['min']
        limit_min_cost = market_limit['cost']['min']
        current_price = ticker['last']
        min_amount_by_cost = float(self.exchange.amount_to_precision(self.symbol, limit_min_cost/current_price))+market_precision['amount']
        real_min_amount = max(limit_min_amount, min_amount_by_cost)

        return real_min_amount
    
    def open_market_position(self, side, amount):
        '''시장가 주문 입력'''
        try:
            amount = max(self.get_min_amount(), amount)
            order = self.exchange.create_order(
                symbol=self.symbol,
                type='market',
                side=side,
                amount=amount
            )
            side_text = "롱" if side=="buy" else "sell"
            self.logger.info(f"[id:{self.trader_id}][{self.symbol}][{self.strategy}] {side_text} 포지션 진입 : 수량= {amount} | 금액= {order['cost']}")
            self.slack_bot.send_trade_alert(
                trader_id=self.trader_id,
                symobl=self.symbol,
                strategy=self.strategy,
                action=f"{side.upper()} 주문",
                details=f"수량: {amount}, 가격: ${order['average']:.2f}"
            )
            return order
        
        except Exception as e:
            self.logger.error(f"[id:{self.trader_id}][{self.symbol}][{self.strategy}] {side_text} 포지션 진입 실패 : {e}")
            self.slack_bot.send_error_alert(
                error_message=str(e),
                context=f"{self.trader_id} {self.symbol} {side} 주문"
            )
            return None

    def create_market_stop_loss_order(self, side, amount, stop_price):
        '''시장가 스탑로스 주문 입력 - 포지션 청산용'''
        try:
            order = self.exchange.create_order(
                symbol=self.symbol,
                type='stop_market',
                side=side,
                amount=amount,
                params={
                    'stopPrice': stop_price,
                    'reduceOnly': True
                }
            )

            self.logger.info(f"[id:{self.trader_id}][{self.symbol}][{self.strategy}] 스탑로스 설정 : 손절가= {stop_price} | 수량= {amount}")
            return order
        
        except Exception as e:
            self.logger.error(f"[id:{self.trader_id}][{self.symbol}][{self.strategy}] 스탑로스 설정 실패 : {e}")
            return None
        
    def close_position(self):
        '''포지션 전체 강제 청산'''
        try:
            position = self.exchange.fetch_position(self.symbol)
            if position['contracts'] == 0:
                self.logger.warning(f"[id:{self.trader_id}][{self.symbol}][{self.strategy}] 진입한 포지션이 없습니다.")
                return False
            
            side_to_close = 'sell' if position['side'] == 'long' else 'buy'
            amount = abs(position['contracts'])

            order = self.exchange.create_market_order(
                symbol=self.symbol,
                side=side_to_close,
                amount=amount,
                params={'reduceOnly': True}
            )
            
            self.logger.info(f"[id:{self.trader_id}][{self.symbol}][{self.strategy}] 포지션 청산 성공 : 수량= {amount} ")
            return order
        
        except Exception as e:
            self.logger.error(f"[id:{self.trader_id}][{self.symbol}][{self.strategy}] 포지션 청산 실패: {e}")
            return None

