# ssl_test.py
import ssl
import certifi
import urllib.request

def test_ssl_with_context():
    try:
        # 인증서 위치 확인
        cert_path = certifi.where()
        print(f"인증서 위치: {cert_path}")
        
        # SSL 컨텍스트 생성
        ssl_context = ssl.create_default_context(cafile=cert_path)
        
        # HTTPS 요청 테스트 (SSL 컨텍스트 사용)
        request = urllib.request.Request('https://httpbin.org/get')
        response = urllib.request.urlopen(request, context=ssl_context)
        print("SSL 연결 성공!")
        
        return True
        
    except Exception as e:
        print(f"SSL 오류: {e}")
        return False

def test_slack_ssl():
    """슬랙 API SSL 테스트"""
    try:
        from slack_sdk import WebClient
        import ssl
        
        ssl_context = ssl.create_default_context(cafile=certifi.where())
        
        # 임시 테스트용 (실제 토큰 없어도 SSL은 확인 가능)
        client = WebClient(token="test", ssl=ssl_context)
        
        # auth_test는 토큰이 잘못되면 invalid_auth 에러가 나야 정상
        # SSL 문제면 다른 에러가 남
        try:
            client.auth_test()
        except Exception as e:
            if "invalid_auth" in str(e):
                print("슬랙 SSL 연결 성공! (토큰만 확인하면 됨)")
                return True
            else:
                print(f"슬랙 SSL 오류: {e}")
                return False
                
    except Exception as e:
        print(f"슬랙 테스트 실패: {e}")
        return False

if __name__ == "__main__":
    print("=== 일반 SSL 테스트 ===")
    test_ssl_with_context()
    
    print("\n=== 슬랙 SSL 테스트 ===")
    test_slack_ssl()