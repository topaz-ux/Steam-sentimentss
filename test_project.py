"""
프로젝트 테스트 스크립트
기본적인 기능들이 제대로 작동하는지 테스트합니다.
"""

import sys
import os

def test_imports():
    """필요한 라이브러리 import 테스트"""
    print("=== 라이브러리 Import 테스트 ===")
    try:
        import pandas as pd
        print("✓ pandas")
        
        import selenium
        print("✓ selenium")
        
        import nltk
        print("✓ nltk")
        
        from nltk.sentiment import SentimentIntensityAnalyzer
        print("✓ nltk.sentiment")
        
        try:
            from wordcloud import WordCloud
            print("✓ wordcloud")
        except ImportError:
            print("⚠ wordcloud (선택적, 컴파일러 필요)")
        
        import matplotlib
        print("✓ matplotlib")
        
        print("\n모든 필수 라이브러리가 성공적으로 import되었습니다!")
        return True
    except ImportError as e:
        print(f"\n✗ Import 오류: {e}")
        print("requirements.txt의 패키지를 설치해주세요: pip install -r requirements.txt")
        return False

def test_nltk_data():
    """NLTK 데이터 다운로드 테스트"""
    print("\n=== NLTK 데이터 테스트 ===")
    try:
        import nltk
        import ssl
        
        # SSL 인증서 검증 임시 비활성화
        try:
            _create_unverified_https_context = ssl._create_unverified_context
        except AttributeError:
            pass
        else:
            ssl._create_default_https_context = _create_unverified_https_context
        
        # NLTK 데이터 확인
        nltk.download('stopwords', quiet=True)
        nltk.download('punkt', quiet=True)
        nltk.download('vader_lexicon', quiet=True)
        
        from nltk.corpus import stopwords
        from nltk.sentiment import SentimentIntensityAnalyzer
        
        # 테스트
        stop_words = stopwords.words('english')
        print(f"✓ stopwords ({len(stop_words)}개 단어)")
        
        sia = SentimentIntensityAnalyzer()
        test_text = "This is a great game!"
        scores = sia.polarity_scores(test_text)
        print(f"✓ VADER 감정 분석 (테스트 점수: {scores['compound']:.3f})")
        
        print("\nNLTK 데이터가 정상적으로 작동합니다!")
        return True
    except Exception as e:
        print(f"\n✗ NLTK 데이터 오류: {e}")
        return False

def test_classes():
    """프로젝트 클래스 테스트"""
    print("\n=== 클래스 테스트 ===")
    try:
        from finalcode import SteamReviewScraper, SentimentAnalyzer
        
        # SteamReviewScraper 테스트
        scraper = SteamReviewScraper("730", "Counter Strike 2")
        print("✓ SteamReviewScraper 초기화")
        
        # SentimentAnalyzer 테스트
        analyzer = SentimentAnalyzer()
        test_text = "This is an amazing game with great graphics!"
        cleaned = analyzer.clean_text(test_text)
        print(f"✓ SentimentAnalyzer 텍스트 정리: '{cleaned[:30]}...'")
        
        scores = analyzer.analyze_sentiment(test_text)
        print(f"✓ SentimentAnalyzer 감정 분석: {scores['compound']:.3f}")
        
        print("\n모든 클래스가 정상적으로 작동합니다!")
        return True
    except Exception as e:
        print(f"\n✗ 클래스 테스트 오류: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_sample_data():
    """샘플 데이터로 전체 파이프라인 테스트"""
    print("\n=== 샘플 데이터 파이프라인 테스트 ===")
    try:
        from finalcode import SteamReviewScraper, SentimentAnalyzer
        import pandas as pd
        
        # 샘플 데이터 생성
        sample_reviews = [
            {
                'review_text': 'Great game! I love playing this with my friends.',
                'recommended': True,
                'playtime_at_review': 150.5,
                'date_posted': '2024-01-15',
                'review_length': 45
            },
            {
                'review_text': 'This game is terrible. Too many bugs.',
                'recommended': False,
                'playtime_at_review': 5.2,
                'date_posted': '2024-01-10',
                'review_length': 38
            }
        ]
        
        scraper = SteamReviewScraper("730", "Test Game")
        scraper.reviews = sample_reviews
        
        df = scraper.to_dataframe()
        print(f"✓ DataFrame 생성 ({len(df)}개 리뷰)")
        
        analyzer = SentimentAnalyzer()
        df = analyzer.analyze_dataframe(df)
        print(f"✓ 감정 분석 완료")
        print(f"  - 평균 Compound Score: {df['compound_score'].mean():.3f}")
        print(f"  - 감정 레이블 분포:")
        print(df['sentiment_label'].value_counts().to_dict())
        
        # CSV 저장 테스트
        test_file = 'test_reviews.csv'
        df.to_csv(test_file, index=False, encoding='utf-8-sig')
        print(f"✓ CSV 저장 완료: {test_file}")
        
        # 파일 삭제
        if os.path.exists(test_file):
            os.remove(test_file)
            print(f"✓ 테스트 파일 삭제 완료")
        
        print("\n샘플 데이터 파이프라인이 정상적으로 작동합니다!")
        return True
    except Exception as e:
        print(f"\n✗ 파이프라인 테스트 오류: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """메인 테스트 함수"""
    print("=" * 50)
    print("Steam 리뷰 스크래핑 및 감정 분석 프로젝트 테스트")
    print("=" * 50)
    
    results = []
    
    # 각 테스트 실행
    results.append(("라이브러리 Import", test_imports()))
    results.append(("NLTK 데이터", test_nltk_data()))
    results.append(("클래스", test_classes()))
    results.append(("샘플 데이터 파이프라인", test_sample_data()))
    
    # 결과 요약
    print("\n" + "=" * 50)
    print("테스트 결과 요약")
    print("=" * 50)
    
    for test_name, result in results:
        status = "✓ 통과" if result else "✗ 실패"
        print(f"{test_name}: {status}")
    
    all_passed = all(result for _, result in results)
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 모든 테스트를 통과했습니다!")
        print("\n프로젝트를 실행할 준비가 되었습니다:")
        print("  - python finalcode.py")
        print("  - jupyter notebook WebMining.ipynb")
        return 0
    else:
        print("⚠️  일부 테스트가 실패했습니다.")
        print("위의 오류 메시지를 확인하고 문제를 해결해주세요.")
        return 1

if __name__ == "__main__":
    sys.exit(main())

