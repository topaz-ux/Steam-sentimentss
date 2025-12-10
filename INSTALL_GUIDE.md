# 설치 가이드

CORS 제한 해결 및 정확한 감정 분석을 위한 설치 가이드입니다.

## 빠른 설치 (자동)

### Windows 사용자
1. `install.bat` 파일을 더블클릭하거나
2. 명령 프롬프트에서 실행:
   ```cmd
   install.bat
   ```

### Linux/Mac 사용자
1. 터미널에서 실행:
   ```bash
   chmod +x install.sh
   ./install.sh
   ```

## 수동 설치 (단계별)

### 1단계: Python 설치 확인
```bash
python --version
# 또는
python3 --version
```
Python 3.8 이상이 필요합니다. 설치되어 있지 않다면 [Python 공식 사이트](https://www.python.org/downloads/)에서 다운로드하세요.

### 2단계: pip 업그레이드
```bash
python -m pip install --upgrade pip
```

### 3단계: 필요한 패키지 설치
```bash
pip install -r requirements.txt
```

설치되는 패키지:
- `selenium` - 웹 스크래핑
- `pandas` - 데이터 처리
- `nltk` - 자연어 처리
- `flask` - 웹 서버
- `matplotlib`, `seaborn`, `plotly` - 시각화
- `webdriver-manager` - Chrome 드라이버 자동 관리
- 기타 필수 패키지들

### 4단계: NLTK 데이터 다운로드
```bash
python setup_nltk.py
```

또는 Python에서 직접:
```python
python -c "import nltk; import ssl; ssl._create_default_https_context = ssl._create_unverified_context; nltk.download('stopwords'); nltk.download('punkt'); nltk.download('punkt_tab'); nltk.download('vader_lexicon'); nltk.download('averaged_perceptron_tagger')"
```

## Flask 앱 실행

설치가 완료되면:

```bash
python app.py
```

터미널에 다음과 같은 메시지가 표시됩니다:
```
Running on http://127.0.0.1:5000
```

그 후 브라우저에서 `http://localhost:5000`으로 접속하세요.

## 문제 해결

### 패키지 설치 오류
- Python 버전 확인 (3.8 이상 필요)
- pip 업그레이드: `python -m pip install --upgrade pip`
- 가상 환경 사용 권장

### NLTK 데이터 다운로드 실패
- 인터넷 연결 확인
- 방화벽 설정 확인
- `setup_nltk.py` 스크립트 사용

### ChromeDriver 오류
- Chrome 브라우저 최신 버전 설치
- `webdriver-manager`가 자동으로 관리합니다

### 포트 5000이 이미 사용 중
- `app.py` 파일에서 포트 번호 변경 가능
- 또는 다른 프로그램 종료

## 설치 확인

설치가 제대로 되었는지 확인:
```bash
python test_project.py
```

모든 테스트가 통과하면 설치가 완료된 것입니다!


