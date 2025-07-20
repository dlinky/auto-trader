import os, ssl, certifi
from dotenv import load_dotenv
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import logging

load_dotenv()

class SlackBot:
    def __init__(self):
        ssl_context = ssl.create_default_context(cafile=certifi.where())
        self.client = WebClient(
            token=os.getenv('SLACK_BOT_TOKEN'),
            ssl=ssl_context
        )
        self.channel = os.getenv('SLACK_CHANNEL', '#general')
        self.logger = logging.getLogger(__name__)

        self._test_connection()

    def _test_connection(self):
        '''슬랙 연결 테스트'''
        try:
            response = self.client.auth_test()
            bot_name = response['user']
            self.logger.info(f"슬랙 봇 연결 성공 : {bot_name}")
            return True
        except SlackApiError as e:
            self.logger.error(f"슬랙 연결 실패: {e.response['error']}")
            return False
    
    def send_message(self, message, urgent=False):
        '''메시지 전송'''
        try:
            if urgent:
                message = f"<!channel> 🚨 {message}"
            response = self.client.chat_postMessage(
                channel=self.channel,
                text=message,
                username="Bitcoin Trader"
            )
            self.logger.info(f"슬랙 메시지 전송 성공: {message[:50]}...")
            return response
        except SlackApiError as e:
            self.logger.error(f"슬랙 메시지 전송 실패: {e.response['error']}")
            return None
        
    def send_trade_alert(self, trader_id, symbol, strategy, action, details):
        '''거래 알림 전송'''
        emoji = "📈" if "buy" in action.lower() else "📉"
        message = f"{emoji} **거래 알림**\n"
        message += f"• 트레이더: {trader_id}\n"
        message += f"• 심볼: {symbol}\n" 
        message += f"• 전략: {strategy}\n"
        message += f"• 액션: {action}\n"
        message += f"• 상세: {details}"
        
        return self.send_message(message)
    
    def send_safety_alert(self, trader_id, symbol, strategy, reason, action_taken):
        """안전장치 알림 (긴급)"""
        message = f"**⚠️ 안전장치 작동**\n"
        message += f"• 트레이더: {trader_id}\n"
        message += f"• 심볼: {symbol}\n"
        message += f"• 전략: {strategy}\n"
        message += f"• 사유: {reason}\n"
        message += f"• 조치: {action_taken}"
        
        return self.send_message(message, urgent=True)
    
    def send_error_alert(self, error_message, context=""):
        """에러 알림"""
        message = f"🔴 **시스템 에러**\n"
        message += f"• 에러: {error_message}\n"
        if context:
            message += f"• 상황: {context}"
        
        return self.send_message(message, urgent=True)
    
    def send_daily_summary(self, total_pnl, trader_summaries):
        """일일 요약 리포트"""
        status_emoji = "🟢" if total_pnl >= 0 else "🔴"
        message = f"{status_emoji} **일일 거래 요약**\n"
        message += f"• 총 수익: ${total_pnl:.2f}\n\n"
        
        for summary in trader_summaries:
            message += f"📊 {summary['trader_id']} ({summary['symbol']})\n"
            message += f"   수익: ${summary['pnl']:.2f} ({summary['pnl_pct']:.1f}%)\n"
        
        return self.send_message(message)