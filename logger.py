# src/utils/logger.py
import logging
import os
from datetime import datetime

def setup_logger():
    """로깅 시스템 설정"""
    
    # 로그 디렉토리 생성
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    # 파일명에 날짜 포함
    now = datetime.now().strftime('%Y%m%d-%H:%M:%S')
    
    # 로거 설정
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    # 기존 핸들러 제거
    logger.handlers.clear()
    
    # 파일 핸들러 (전체 로그)
    file_handler = logging.FileHandler(f'logs/trader_{now}.log', encoding='utf-8')
    file_handler.setLevel(logging.INFO)
    
    # 에러 전용 파일 핸들러
    error_handler = logging.FileHandler(f'logs/error_{now}.log', encoding='utf-8')
    error_handler.setLevel(logging.ERROR)
    
    # 콘솔 핸들러
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # 포맷터 설정
    formatter = logging.Formatter(
        '%(asctime)s | %(levelname)s | %(name)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    file_handler.setFormatter(formatter)
    error_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(error_handler)
    logger.addHandler(console_handler)
    
    return logger
