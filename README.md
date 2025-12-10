# 🎮 Steam 게임 리뷰 스크래핑 및 감정 분석

Steam 게임 리뷰를 스크래핑하고 감정 분석을 수행하는 엔드투엔드 머신러닝 프로젝트입니다.

## 📋 프로젝트 개요

이 프로젝트는 Steam 게임 리뷰를 자동으로 수집하고, 자연어 처리 기술을 사용하여 리뷰의 감정을 분석합니다. 플레이어들이 게임에 대해 어떻게 생각하는지 데이터 기반으로 파악할 수 있습니다.

### 주요 기능

- 🕹️ **게임 리뷰 스크래핑** - Selenium을 사용하여 Steam에서 게임 리뷰 자동 수집
- 🤖 **감정 분석** - NLTK와 VADER를 사용하여 리뷰의 감정(긍정/부정/중립) 분석
- 📊 **데이터 시각화** - 10가지 다양한 시각화 제공 (박스 플롯, 워드 클라우드, 파이 차트 등)
- 🌐 **웹 인터페이스** - Flask를 사용한 사용자 친화적인 웹 애플리케이션
- 📈 **데이터 인사이트** - 추천 여부와 감정 점수의 상관관계 분석

## 🛠️ 기술 스택

- **Python 3.8+**
- **Selenium** - 웹 스크래핑
- **Pandas** - 데이터 조작 및 분석
- **NLTK** - 자연어 처리
- **VADER** - 감정 분석
- **Matplotlib & Seaborn** - 데이터 시각화
- **WordCloud** - 워드 클라우드 생성 (선택적)
- **Flask** - 웹 애플리케이션
- **Jupyter Notebook** - 인터랙티브 분석

## 📦 설치 방법

### 1. 저장소 클론

```bash
git clone https://github.com/yourusername/Steam-sentiment.git
cd Steam-sentiment
```

### 2. 가상 환경 생성 (선택사항)

```bash
python -m venv venv
venv\Scripts\activate  # Windows
# 또는
source venv/bin/activate  # Linux/Mac
```

### 3. 필요한 패키지 설치

```bash
pip install -r requirements.txt
```

### 4. Chrome 브라우저 설치

Chrome 브라우저가 설치되어 있어야 합니다. ChromeDriver는 `webdriver-manager`가 자동으로 관리합니다.

### 5. NLTK 데이터 다운로드

프로그램 실행 시 자동으로 다운로드됩니다. 수동으로 다운로드하려면:

```python
import nltk
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('vader_lexicon')
```

## 🚀 사용 방법

### 방법 1: Python 스크립트 실행

```bash
python finalcode.py
```

이 스크립트는:
1. Steam에서 게임 리뷰를 스크래핑합니다
2. 감정 분석을 수행합니다
3. 결과를 `game_reviews.csv` 파일로 저장합니다

### 방법 2: 웹 인터페이스 사용 (권장) 🌐

#### 로컬 실행 (실제 스크래핑 가능)

```bash
python app.py
```

브라우저에서 `http://localhost:5000`으로 접속하여 웹 인터페이스를 사용할 수 있습니다.

**기능:**
- 🔍 **게임 검색 및 선택**: 게임 ID 입력 또는 인기 게임 선택
- 📥 **리뷰 스크래핑**: Steam에서 실제 리뷰 데이터 수집
- 🤖 **감정 분석**: NLTK VADER를 사용한 자동 감정 분석
- 📊 **시각화 자동 생성**: 10가지 다양한 시각화 자동 생성
- 💾 **결과 다운로드**: CSV 파일 및 이미지 다운로드

**사용 방법:**
1. 웹 인터페이스에서 게임 ID를 입력하거나 인기 게임을 선택
2. 수집할 리뷰 수를 설정 (10-500개)
3. "리뷰 분석 시작" 버튼 클릭
4. 자동으로 스크래핑 → 감정 분석 → 시각화 생성이 수행됩니다

#### GitHub Pages 배포 (서버 없이 실행) 🌐

GitHub Pages에 배포하면 서버 없이 바로 실행할 수 있습니다!

**배포 방법:**
1. GitHub 저장소에 코드 푸시
2. Settings → Pages → Source에서 "GitHub Actions" 선택
3. 자동 배포 완료 후 `https://사용자명.github.io/저장소명/` 접속

**기능:**
- 🔍 게임 검색 및 선택 기능
- 📥 실제 Steam API에서 리뷰 수집 (CORS 프록시 사용)
- 🤖 클라이언트 사이드 감정 분석
- 📊 실시간 시각화 생성

**참고:** 
- 일부 브라우저에서는 CORS 정책으로 인해 작동하지 않을 수 있습니다
- 이 경우 로컬 Flask 앱(`python app.py`)을 사용하세요
- 자세한 배포 방법은 `GITHUB_PAGES_SETUP.md` 참고

### 방법 3: Jupyter Notebook 사용

```bash
jupyter notebook WebMining.ipynb
```

노트북을 실행하여 단계별로 프로세스를 확인하고 수정할 수 있습니다.

### 방법 4: 시각화만 생성

이미 `game_reviews.csv` 파일이 있다면:

```bash
python visualization.py
```

이 명령어는 다음 시각화를 생성합니다 (총 10개):

**기본 시각화:**
- `recommendation_distribution.png` - 추천 분포 막대 그래프
- `sentiment_boxplot.png` - 감정 점수 박스 플롯
- `sentiment_distribution.png` - 감정 레이블 분포
- `wordcloud.png` 또는 `wordcloud_simple.png` - 워드 클라우드
- `playtime_vs_sentiment.png` - 플레이 시간 vs 감정 점수

**추가 시각화:**
- `sentiment_pie_chart.png` - 감정 분포 파이 차트
- `review_length_distribution.png` - 리뷰 길이 분포
- `sentiment_score_histogram.png` - 감정 점수 히스토그램
- `playtime_distribution.png` - 플레이 시간 분포
- `date_sentiment_trend.png` - 날짜별 감정 추이

### 방법 5: 테스트 실행

프로젝트의 기본 기능을 테스트:

```bash
python test_project.py
```

## 📁 프로젝트 구조

```
Steam-sentiment/
│
├── finalcode.py              # 메인 스크래핑 및 감정 분석 스크립트
├── visualization.py          # 시각화 생성 스크립트 (10개 시각화)
├── app.py                    # Flask 웹 애플리케이션
├── test_project.py           # 프로젝트 테스트 스크립트
├── WebMining.ipynb           # Jupyter Notebook (단계별 분석)
├── results_demo.html         # 결과 리포트 (독립 실행형 HTML)
│
├── requirements.txt          # 필요한 패키지 목록
├── README.md                 # 프로젝트 문서
├── .gitignore                # Git 무시 파일
│
├── templates/
│   └── index.html           # 웹 인터페이스 HTML
│
└── [생성되는 파일들]
    ├── game_reviews.csv     # 수집된 리뷰 데이터
    └── *.png                # 시각화 이미지 파일들
```

## 🔧 설정

### 게임 변경하기

#### 웹 인터페이스 사용 시 (권장)

웹 인터페이스에서 직접 게임 ID를 입력하거나 인기 게임을 선택할 수 있습니다.

#### Python 스크립트 사용 시

다른 게임의 리뷰를 분석하려면 `finalcode.py`의 다음 부분을 수정하세요:

```python
# Counter Strike 2의 Steam 게임 ID
game_id = "730"  # 원하는 게임 ID로 변경
game_name = "Counter Strike 2"  # 게임 이름 변경
```

**Steam 게임 ID 찾는 방법:**
1. Steam 스토어 페이지로 이동: `https://store.steampowered.com/app/{GAME_ID}/`
2. URL에서 숫자 부분이 게임 ID입니다
3. 예: `https://store.steampowered.com/app/730/` → 게임 ID는 **730**

**인기 게임 ID 예시:**
- Counter Strike 2: `730`
- Grand Theft Auto V: `271590`
- Red Dead Redemption 2: `1174180`
- Cyberpunk 2077: `1091500`
- Dota 2: `570`

### 스크래핑 옵션 조정

```python
# 리뷰 수 조정
scraper.scrape_reviews_selenium(num_reviews=100, delay=2)

# delay: 페이지 간 대기 시간 (초) - 서버 부하를 줄이기 위해 조정 가능
```

## 📊 출력 결과

### CSV 파일 구조

`game_reviews.csv` 파일에는 다음 컬럼이 포함됩니다:

- `review_text`: 리뷰 원문
- `recommended`: 추천 여부 (True/False)
- `playtime_at_review`: 리뷰 작성 시 플레이 시간
- `date_posted`: 리뷰 작성 날짜
- `review_length`: 리뷰 길이
- `cleaned_text`: 정리된 리뷰 텍스트
- `compound_score`: VADER 감정 점수 (-1 ~ 1)
- `positive_score`: 긍정 점수
- `neutral_score`: 중립 점수
- `negative_score`: 부정 점수
- `sentiment_label`: 감정 레이블 (positive/negative/neutral)

### 시각화

프로젝트는 다음 시각화를 생성합니다:

1. **추천 분포** - 추천/비추천 리뷰의 비율
2. **감정 점수 박스 플롯** - 추천 여부별 감정 점수 분포
3. **감정 레이블 분포** - 긍정/부정/중립 리뷰의 개수
4. **감정 분포 파이 차트** - 감정 비율을 파이 차트로 표시
5. **워드 클라우드** - 리뷰에서 가장 많이 사용된 단어들
6. **플레이 시간 vs 감정** - 플레이 시간과 감정 점수의 관계
7. **리뷰 길이 분포** - 리뷰 길이의 분포 히스토그램
8. **감정 점수 히스토그램** - 감정 점수 분포 비교
9. **플레이 시간 분포** - 추천/비추천별 플레이 시간 분포
10. **날짜별 감정 추이** - 시간에 따른 감정 변화

## ⚠️ 주의사항

### 웹 스크래핑 윤리

이 프로젝트는 교육 및 연구 목적으로 제작되었습니다. 웹 스크래핑을 수행할 때는 다음 사항을 준수하세요:

1. **서버 부하 최소화**: 적절한 딜레이를 설정하여 서버에 부담을 주지 않습니다
2. **이용 약관 확인**: Steam의 이용 약관을 확인하고 준수합니다
3. **데이터 사용**: 수집한 데이터는 개인적인 분석 목적으로만 사용합니다
4. **상업적 사용 금지**: 수집한 데이터를 상업적으로 사용하지 않습니다

### SSL 인증서 경고

NLTK 데이터를 다운로드할 때 SSL 인증서 경고가 발생할 수 있습니다. 이는 NLTK 데이터 다운로드를 위한 임시 설정이며, 프로덕션 환경에서는 적절한 SSL 인증서를 사용하는 것을 권장합니다.

## 🐛 문제 해결

### ChromeDriver 오류

ChromeDriver 관련 오류가 발생하면:

1. Chrome 브라우저가 최신 버전인지 확인
2. `webdriver-manager`가 최신 버전인지 확인: `pip install --upgrade webdriver-manager`

### NLTK 데이터 다운로드 실패

NLTK 데이터 다운로드가 실패하면:

1. 인터넷 연결 확인
2. 방화벽 설정 확인
3. 수동으로 다운로드:
   ```python
   import nltk
   import ssl
   ssl._create_default_https_context = ssl._create_unverified_context
   nltk.download('stopwords')
   nltk.download('punkt')
   nltk.download('punkt_tab')
   nltk.download('vader_lexicon')
   ```

### 워드 클라우드 설치

워드 클라우드가 설치되지 않은 경우:

- **대체 방법**: `wordcloud_simple.png` 파일이 자동으로 생성됩니다 (단어 빈도 그래프)
- **실제 워드 클라우드**: Microsoft C++ Build Tools 설치 후 `pip install wordcloud`

### 스크래핑 실패

Steam 웹사이트 구조가 변경되어 스크래핑이 실패할 수 있습니다. 이 경우:

1. 샘플 데이터로 자동 전환됩니다
2. Selenium 셀렉터 업데이트가 필요할 수 있습니다

### 웹 서버 접속 문제

웹 서버에 접속할 수 없는 경우:

1. 서버가 실행 중인지 확인 (`python app.py`)
2. 올바른 주소 사용: `http://localhost:5000` (https 아님)
3. 포트가 사용 중이면 `app.py`에서 포트 번호 변경

## 📝 라이선스

이 프로젝트는 MIT 라이선스를 따릅니다.

## 🙏 감사의 말

- [Steam](https://store.steampowered.com/) - 게임 리뷰 데이터 제공
- [NLTK](https://www.nltk.org/) - 자연어 처리 라이브러리
- [Selenium](https://www.selenium.dev/) - 웹 자동화 도구
- [Flask](https://flask.palletsprojects.com/) - 웹 프레임워크

## 📧 문의

프로젝트에 대한 질문이나 제안사항이 있으시면 이슈를 등록해주세요.

---

**면책 조항**: 이 프로젝트는 교육 목적으로 제작되었습니다. 웹 스크래핑을 수행할 때는 해당 웹사이트의 이용 약관과 로봇 배제 표준(robots.txt)을 준수해야 합니다.
