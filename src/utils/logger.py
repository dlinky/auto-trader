# src/utils/logger.py
import logging
import os
from datetime import datetime


def setup_logger():
    '''로깅 시스템 설정'''

    if not os.path.exists('logs'):
        os.makedirs('logs')

    now = datetime.now().strftime('%Y%m%d %H:%M:%S')
    
    # 기존 로거 설정 초기화(싱글톤 패턴) : 잘못하면 호출할때마다 핸들러가 추가됨
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.handlers.clear() # 기존 핸들러 제거

    info_handler = logging.FileHandler(f'logs/trader_{now}.log', encoding='utf-8')
    info_handler.setLevel(logging.INFO)

    warning_handler = logging.FileHandler(f'logs/warning_{now}.log', encoding='utf-8')
    warning_handler.setLevel(logging.WARNING)

    error_handler = logging.FileHandler(f'logs/error_{now}.log', encoding='utf-8')
    error_handler.setLevel(logging.ERROR)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # 포맷터 설정
    detailed_formatter = logging.Formatter(
        '%(asctime)s | %(levelname)s | %(name)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    console_formatter = logging.Formatter(
        '%(asctime)s | %(levelname)s | %(message)s',
        datefmt='%H:%M:%S' # 실시간으로 볼거라 시간만 기입
    )

    # 포맷터 적용
    info_handler.setFormatter(detailed_formatter)
    warning_handler.setFormatter(detailed_formatter)
    error_handler.setFormatter(detailed_formatter)
    console_handler.setFormatter(console_formatter)

    # 핸들러 추가
    logger.addHandler(info_handler)
    logger.addHandler(warning_handler)
    logger.addHandler(error_handler)
    logger.addHandler(console_handler)

    return logger