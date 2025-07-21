import sqlite3
import os
from datetime import datetime

def create_database():
    # 데이터 디렉토리 생성
    if not os.path.exists('data'):
        os.makedirs('data')
    
    # SQLite 연결 (파일이 없으면 자동 생성)
    conn = sqlite3.connect('data/trading.db')
    cursor = conn.cursor()
    
    # 테이블 생성
    create_tables(cursor)
    
    conn.commit()
    conn.close()
    print("✅ 데이터베이스 생성 완료: data/trading.db")

def create_tables(cursor):
    """모든 테이블 생성"""
    
    # 1. candles_1m 테이블
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS candles_1m (
            symbol TEXT NOT NULL,
            dt TEXT NOT NULL,
            open REAL NOT NULL,
            high REAL NOT NULL,
            low REAL NOT NULL,
            close REAL NOT NULL,
            volume REAL NOT NULL,
            PRIMARY KEY (symbol, dt)
        )
    ''')
    
    # 2. indicator 테이블
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS indicator (
            symbol TEXT NOT NULL,
            idc_name TEXT NOT NULL,
            dt TEXT NOT NULL,
            value REAL NOT NULL,
            PRIMARY KEY (symbol, idc_name, dt)
        )
    ''')
    
    # 3. trader 테이블
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS trader (
            trader_id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT NOT NULL,
            strategy TEXT NOT NULL,
            started_at TEXT NOT NULL,
            parameter TEXT NOT NULL,
            status TEXT NOT NULL,
            start_balance REAL NOT NULL,
            current_balance REAL NOT NULL,
            total_pnl REAL NOT NULL DEFAULT 0
        )
    ''')
    
    # 4. logging 테이블
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS logging (
            log_id INTEGER PRIMARY KEY AUTOINCREMENT,
            trader_id INTEGER NOT NULL,
            session_id INTEGER NOT NULL,
            reg_dt TEXT NOT NULL,
            symbol TEXT NOT NULL,
            strategy TEXT NOT NULL,
            category TEXT NOT NULL,
            position TEXT,
            action TEXT,
            open_price REAL,
            open_amount REAL,
            open_cost REAL,
            balance REAL,
            pnl REAL,
            FOREIGN KEY (trader_id) REFERENCES trader(trader_id)
        )
    ''')
    
    # 인덱스 생성 (성능 향상)
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_logging_trader ON logging(trader_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_logging_dt ON logging(reg_dt)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_candles_symbol_dt ON candles_1m(symbol, dt)')

if __name__ == "__main__":
    create_database()