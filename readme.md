# 프로젝트 개요
바이낸스 선물 자동매매 프로그램
# 주요 기능
- 다양한 전략 선택
- 백테스팅 및 전략 경쟁을 통해 최적의 조합 선정
- 레버리지 및 위험 관리
- 대시보드 지원
# 폴더 구조
```
📦auto-trader
 ┣ 📂config
 ┣ 📂logs
 ┣ 📂src
 ┃ ┣ 📂api
 ┃ ┃ ┗ 📜binance_client.py - 가격/잔고 조회, 매매 등 기능
 ┃ ┣ 📂backtest
 ┃ ┣ 📂dashboard
 ┃ ┣ 📂strategies
 ┃ ┗ 📂utils
 ┃ ┃ ┣ 📜logger.py
 ┣ 📂tests
 ┣ 📜main.py
 ```
# 모듈 구조
## api/binance_client.py
조회, 매매 등 거래소 객체 구현
### class BinanceClient
심볼/전략이 지정된 단일 거래소 클래스
#### 메소드 목록
init : 심볼, 전략, 테스트넷여부 받아서 계정 연결

set_leverage : 레버리지 설정

get_min_amount : 포지션 진입 시 최소수량 계산

open_market_position : 시장가 주문

create_market_stop_loss_order : 시장가 스탑로스 설정 (포지션 오픈 후 함께 사용)

close position : 포지션 청산

## utils/logger.py
로깅 시스템 구현
- info, warning, error, console 핸들러 구성

## utils/slack_bot.py
슬랙봇 연결

