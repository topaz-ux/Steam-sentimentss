"""
Steam Game Review Scraping and Sentiment Analysis
This script scrapes Steam game reviews and performs sentiment analysis using NLTK and VADER.
"""

import time
import pandas as pd
import re
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.sentiment import SentimentIntensityAnalyzer
import ssl
import warnings
warnings.filterwarnings('ignore')

# SSL 인증서 검증 임시 비활성화 (NLTK 다운로드용)
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

# NLTK 데이터 다운로드
print("NLTK 데이터를 다운로드하는 중...")
nltk.download('stopwords', quiet=True)
nltk.download('punkt', quiet=True)
nltk.download('punkt_tab', quiet=True)  # 최신 NLTK 버전용
nltk.download('averaged_perceptron_tagger', quiet=True)
nltk.download('vader_lexicon', quiet=True)

class SteamReviewScraper:
    """Steam 게임 리뷰를 스크래핑하는 클래스"""
    
    def __init__(self, game_id, game_name="Counter Strike 2"):
        """
        Args:
            game_id: Steam 게임 ID
            game_name: 게임 이름 (기본값: Counter Strike 2)
        """
        self.game_id = game_id
        self.game_name = game_name
        self.base_url = f"https://store.steampowered.com/appreviews/{game_id}?json=1"
        self.reviews = []
        self.driver = None
        
    def setup_driver(self):
        """Chrome WebDriver 설정"""
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # 백그라운드 실행
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        print("Chrome WebDriver가 설정되었습니다.")
        
    def scrape_reviews(self, num_pages=5, delay=2):
        """
        Steam 리뷰 스크래핑
        
        Args:
            num_pages: 스크래핑할 페이지 수
            delay: 페이지 간 대기 시간 (초)
        """
        if not self.driver:
            self.setup_driver()
            
        print(f"{self.game_name}의 리뷰를 스크래핑하는 중...")
        
        cursor = "*"
        page = 0
        
        while page < num_pages:
            try:
                url = f"{self.base_url}&cursor={cursor}&num_per_page=100&filter=all&language=all"
                self.driver.get(url)
                time.sleep(delay)
                
                # JSON 응답 파싱
                page_source = self.driver.page_source
                
                # JSON 데이터 추출 (간단한 방법)
                import json
                try:
                    # 페이지 소스에서 JSON 데이터 찾기
                    json_match = re.search(r'<pre[^>]*>(.*?)</pre>', page_source, re.DOTALL)
                    if json_match:
                        json_data = json.loads(json_match.group(1))
                    else:
                        # 직접 JSON 파싱 시도
                        json_start = page_source.find('{')
                        json_end = page_source.rfind('}') + 1
                        if json_start != -1 and json_end > json_start:
                            json_data = json.loads(page_source[json_start:json_end])
                        else:
                            print(f"페이지 {page + 1}에서 JSON 데이터를 찾을 수 없습니다.")
                            break
                    
                    if 'reviews' in json_data and json_data['reviews']:
                        for review in json_data['reviews']:
                            review_data = {
                                'review_text': review.get('review', ''),
                                'recommended': review.get('voted_up', False),
                                'playtime_at_review': review.get('author', {}).get('playtime_at_review', 0),
                                'date_posted': datetime.fromtimestamp(review.get('timestamp_created', 0)).strftime('%Y-%m-%d'),
                                'review_length': len(review.get('review', ''))
                            }
                            self.reviews.append(review_data)
                        
                        # 다음 페이지를 위한 cursor 업데이트
                        cursor = json_data.get('cursor', '')
                        if not cursor or cursor == '*':
                            break
                            
                        page += 1
                        print(f"페이지 {page} 완료: {len(self.reviews)}개 리뷰 수집됨")
                    else:
                        print(f"페이지 {page + 1}에 리뷰가 없습니다.")
                        break
                        
                except json.JSONDecodeError as e:
                    print(f"JSON 파싱 오류: {e}")
                    break
                except Exception as e:
                    print(f"오류 발생: {e}")
                    break
                    
            except Exception as e:
                print(f"페이지 {page + 1} 스크래핑 중 오류: {e}")
                break
        
        print(f"총 {len(self.reviews)}개의 리뷰를 수집했습니다.")
        
    def scrape_reviews_selenium(self, num_reviews=100, delay=2):
        """
        Selenium을 사용하여 Steam 리뷰 페이지에서 직접 스크래핑
        
        Args:
            num_reviews: 수집할 리뷰 수
            delay: 페이지 스크롤 간 대기 시간
        """
        if not self.driver:
            self.setup_driver()
            
        print(f"{self.game_name}의 리뷰를 Selenium으로 스크래핑하는 중...")
        
        # Steam 리뷰 페이지로 이동
        review_url = f"https://store.steampowered.com/app/{self.game_id}/#app_reviews_hash"
        self.driver.get(review_url)
        time.sleep(3)
        
        # 페이지가 로드될 때까지 대기
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "app_review"))
            )
        except:
            print("리뷰 요소를 찾을 수 없습니다. 페이지 구조를 확인하세요.")
            return
        
        # 페이지 스크롤하여 더 많은 리뷰 로드
        scroll_pause_time = delay
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        
        while len(self.reviews) < num_reviews:
            # 페이지 끝까지 스크롤
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(scroll_pause_time)
            
            # 리뷰 요소 찾기
            review_elements = self.driver.find_elements(By.CLASS_NAME, "app_review")
            
            for element in review_elements[len(self.reviews):]:
                if len(self.reviews) >= num_reviews:
                    break
                    
                try:
                    # 리뷰 텍스트 추출
                    review_text_elem = element.find_element(By.CLASS_NAME, "app_review_content")
                    review_text = review_text_elem.text.strip()
                    
                    # 추천 여부 확인
                    recommended = "Recommended" in element.get_attribute("class") or \
                                 element.find_elements(By.XPATH, ".//div[contains(@class, 'title') and contains(text(), 'Recommended')]")
                    
                    # 플레이 시간 추출 시도
                    playtime = 0
                    try:
                        playtime_elem = element.find_element(By.CLASS_NAME, "hours")
                        playtime_text = playtime_elem.text
                        playtime_match = re.search(r'(\d+\.?\d*)', playtime_text)
                        if playtime_match:
                            playtime = float(playtime_match.group(1))
                    except:
                        pass
                    
                    # 날짜 추출 시도
                    date_posted = datetime.now().strftime('%Y-%m-%d')
                    try:
                        date_elem = element.find_element(By.CLASS_NAME, "date_posted")
                        date_posted = date_elem.text.strip()
                    except:
                        pass
                    
                    review_data = {
                        'review_text': review_text,
                        'recommended': bool(recommended),
                        'playtime_at_review': playtime,
                        'date_posted': date_posted,
                        'review_length': len(review_text)
                    }
                    
                    self.reviews.append(review_data)
                    
                except Exception as e:
                    continue
            
            # 새로운 높이 확인
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                # 더 이상 새로운 콘텐츠가 없음
                break
            last_height = new_height
        
        print(f"총 {len(self.reviews)}개의 리뷰를 수집했습니다.")
        
    def to_dataframe(self):
        """수집한 리뷰를 pandas DataFrame으로 변환"""
        if not self.reviews:
            print("수집된 리뷰가 없습니다.")
            return None
        return pd.DataFrame(self.reviews)
    
    def close(self):
        """WebDriver 종료"""
        if self.driver:
            self.driver.quit()
            print("WebDriver가 종료되었습니다.")


class SentimentAnalyzer:
    """리뷰 텍스트에 대한 감정 분석 클래스"""
    
    def __init__(self):
        self.sia = SentimentIntensityAnalyzer()
        self.stop_words = set(stopwords.words('english'))
        
    def clean_text(self, text):
        """텍스트 정리 및 전처리"""
        if not isinstance(text, str):
            return ""
        
        # 소문자 변환
        text = text.lower()
        
        # 특수 문자 제거 (알파벳과 공백만 유지)
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        
        # 토큰화
        tokens = word_tokenize(text)
        
        # 불용어 제거
        tokens = [word for word in tokens if word not in self.stop_words and len(word) > 2]
        
        return ' '.join(tokens)
    
    def analyze_sentiment(self, text):
        """VADER를 사용한 감정 분석"""
        if not isinstance(text, str) or not text.strip():
            return {'compound': 0.0, 'pos': 0.0, 'neu': 0.0, 'neg': 0.0}
        
        scores = self.sia.polarity_scores(text)
        return scores
    
    def analyze_dataframe(self, df):
        """DataFrame의 모든 리뷰에 대해 감정 분석 수행"""
        print("감정 분석을 수행하는 중...")
        
        # 텍스트 정리
        df['cleaned_text'] = df['review_text'].apply(self.clean_text)
        
        # 감정 분석
        sentiment_scores = df['cleaned_text'].apply(self.analyze_sentiment)
        
        # 점수를 별도 컬럼으로 분리
        df['compound_score'] = sentiment_scores.apply(lambda x: x['compound'])
        df['positive_score'] = sentiment_scores.apply(lambda x: x['pos'])
        df['neutral_score'] = sentiment_scores.apply(lambda x: x['neu'])
        df['negative_score'] = sentiment_scores.apply(lambda x: x['neg'])
        
        # 감정 레이블 추가
        df['sentiment_label'] = df['compound_score'].apply(
            lambda x: 'positive' if x >= 0.05 else ('negative' if x <= -0.05 else 'neutral')
        )
        
        print("감정 분석이 완료되었습니다.")
        return df


def main():
    """메인 실행 함수"""
    # Counter Strike 2의 Steam 게임 ID
    game_id = "730"  # Counter Strike 2 (CS:GO)
    game_name = "Counter Strike 2"
    
    # 스크래퍼 초기화
    scraper = SteamReviewScraper(game_id, game_name)
    
    try:
        # 리뷰 스크래핑 (더 안정적인 방법 사용)
        # API 방식이 작동하지 않을 경우를 대비해 샘플 데이터 생성 옵션 제공
        print("\n=== Steam 리뷰 스크래핑 시작 ===\n")
        
        # 실제 스크래핑 시도
        try:
            scraper.scrape_reviews_selenium(num_reviews=50, delay=2)
        except Exception as e:
            print(f"스크래핑 중 오류 발생: {e}")
            print("샘플 데이터를 생성합니다...")
            # 샘플 데이터 생성
            sample_reviews = [
                {
                    'review_text': 'Great game! I love playing this with my friends. The graphics are amazing and the gameplay is smooth.',
                    'recommended': True,
                    'playtime_at_review': 150.5,
                    'date_posted': '2024-01-15',
                    'review_length': 95
                },
                {
                    'review_text': 'This game is terrible. Too many bugs and the servers are always down. Waste of money.',
                    'recommended': False,
                    'playtime_at_review': 5.2,
                    'date_posted': '2024-01-10',
                    'review_length': 78
                },
                {
                    'review_text': 'Decent game but needs more content. The mechanics are okay but gets boring after a while.',
                    'recommended': True,
                    'playtime_at_review': 45.0,
                    'date_posted': '2024-01-12',
                    'review_length': 82
                },
                {
                    'review_text': 'Amazing experience! Best game I have played in years. Highly recommend to everyone.',
                    'recommended': True,
                    'playtime_at_review': 300.0,
                    'date_posted': '2024-01-20',
                    'review_length': 75
                },
                {
                    'review_text': 'Not worth the price. The game is broken and the developers dont care about fixing it.',
                    'recommended': False,
                    'playtime_at_review': 10.5,
                    'date_posted': '2024-01-08',
                    'review_length': 88
                }
            ]
            scraper.reviews = sample_reviews * 10  # 50개 샘플 생성
        
        # DataFrame으로 변환
        df = scraper.to_dataframe()
        
        if df is not None and not df.empty:
            print(f"\n수집된 리뷰 수: {len(df)}")
            print(f"\n리뷰 데이터 미리보기:")
            print(df.head())
            
            # 감정 분석 수행
            analyzer = SentimentAnalyzer()
            df = analyzer.analyze_dataframe(df)
            
            # 결과 저장
            output_file = 'game_reviews.csv'
            df.to_csv(output_file, index=False, encoding='utf-8-sig')
            print(f"\n결과가 '{output_file}'에 저장되었습니다.")
            
            # 기본 통계 출력
            print("\n=== 감정 분석 결과 ===")
            print(f"전체 리뷰 수: {len(df)}")
            print(f"추천 리뷰: {df['recommended'].sum()} ({df['recommended'].sum()/len(df)*100:.1f}%)")
            print(f"비추천 리뷰: {(~df['recommended']).sum()} ({(~df['recommended']).sum()/len(df)*100:.1f}%)")
            print(f"\n감정 분포:")
            print(df['sentiment_label'].value_counts())
            print(f"\n평균 Compound Score: {df['compound_score'].mean():.3f}")
            print(f"추천 리뷰 평균 Score: {df[df['recommended']]['compound_score'].mean():.3f}")
            print(f"비추천 리뷰 평균 Score: {df[~df['recommended']]['compound_score'].mean():.3f}")
            
        else:
            print("수집된 데이터가 없습니다.")
            
    finally:
        # WebDriver 종료
        scraper.close()


if __name__ == "__main__":
    main()

