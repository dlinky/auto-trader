import logging

class TradeLogger:
    def __init__(self):
        self.logger = logging.getLogger('TRADE')
    
    def log_order(self, action, symbol, strategy, side, amount, price=None, order_type='market'):
        """주문 로그"""
        msg = f"[주문] {action} | {symbol} | {strategy} | {side.upper()} | 수량: {amount}"
        if price:
            msg += f" | 가격: {price}"
        msg += f" | 타입: {order_type.upper()}"
        
        self.logger.info(msg)
    
    def log_position_change(self, symbol, strategy, old_pos, new_pos):
        """포지션 변화 로그"""
        self.logger.info(f"[포지션변화] {symbol} | {strategy} | {old_pos} → {new_pos}")
    
    def log_pnl(self, symbol, strategy, pnl, pnl_percent):
        """수익/손실 로그"""
        status = "이익" if pnl > 0 else "손실"
        self.logger.info(f"[수익현황] {symbol} | {strategy} | {status}: ${pnl:.2f} ({pnl_percent:.2f}%)")
    
    def log_safety_action(self, action, symbol, strategy, reason):
        """안전장치 작동 로그"""
        self.logger.warning(f"[안전장치] {action} | {symbol} | {strategy} | 사유: {reason}")

    def info(self, message):
        """정보 로그"""
        self.logger.info(message)
    
    def warning(self, message):
        """경고 로그"""
        self.logger.warning(message)
    
    def error(self, message):
        """에러 로그"""
        self.logger.error(message)
    
    def debug(self, message):
        """디버그 로그"""
        self.logger.debug(message)