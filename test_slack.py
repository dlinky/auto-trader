from src.utils.slack_bot import SlackBot
from src.utils.logger import setup_logger

setup_logger()
slack_bot = SlackBot()

# 기본 메시지 테스트
slack_bot.send_message("🤖 비트코인 트레이더 봇 테스트 메시지")

# 거래 알림 테스트
slack_bot.send_trade_alert(
    trader_id="T001",
    symbol="BTC/USDT", 
    strategy="RSI_MA",
    action="BUY 주문",
    details="수량: 0.001, 가격: $42,500"
)