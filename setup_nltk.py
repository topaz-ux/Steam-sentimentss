"""
NLTK 데이터 자동 다운로드 스크립트
이 스크립트는 감정 분석에 필요한 NLTK 데이터를 자동으로 다운로드합니다.
"""

import nltk
import ssl

# SSL 인증서 검증 임시 비활성화 (NLTK 다운로드용)
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

def download_nltk_data():
    """필요한 NLTK 데이터를 다운로드합니다."""
    print("=" * 50)
    print("NLTK 데이터 다운로드 시작")
    print("=" * 50)
    
    required_data = [
        ('stopwords', '불용어 데이터'),
        ('punkt', '토큰화 데이터'),
        ('punkt_tab', '토큰화 데이터 (최신 버전)'),
        ('vader_lexicon', 'VADER 감정 분석 사전'),
        ('averaged_perceptron_tagger', '품사 태거 데이터')
    ]
    
    for data_name, description in required_data:
        try:
            print(f"\n[{data_name}] {description} 다운로드 중...")
            nltk.download(data_name, quiet=False)
            print(f"✓ {data_name} 다운로드 완료")
        except Exception as e:
            print(f"✗ {data_name} 다운로드 실패: {e}")
    
    print("\n" + "=" * 50)
    print("NLTK 데이터 다운로드 완료!")
    print("=" * 50)
    
    # 다운로드 확인
    print("\n다운로드 확인:")
    try:
        from nltk.corpus import stopwords
        from nltk.sentiment import SentimentIntensityAnalyzer
        from nltk.tokenize import word_tokenize
        
        stop_words = stopwords.words('english')
        print(f"✓ stopwords: {len(stop_words)}개 단어")
        
        sia = SentimentIntensityAnalyzer()
        test_text = "This is a great game!"
        scores = sia.polarity_scores(test_text)
        print(f"✓ VADER 감정 분석: 테스트 성공 (점수: {scores['compound']:.3f})")
        
        tokens = word_tokenize(test_text)
        print(f"✓ 토큰화: {len(tokens)}개 토큰 생성")
        
        print("\n모든 NLTK 데이터가 정상적으로 작동합니다!")
        return True
    except Exception as e:
        print(f"\n오류: {e}")
        return False

if __name__ == "__main__":
    success = download_nltk_data()
    if success:
        print("\n이제 'python app.py'를 실행하여 Flask 앱을 시작할 수 있습니다!")
    else:
        print("\n일부 데이터 다운로드에 실패했습니다. 수동으로 다시 시도해주세요.")

