# 빠른 시작 가이드 🚀

## 설치 완료! ✅

모든 필수 패키지가 설치되었습니다:
- ✅ Flask (웹 서버)
- ✅ NLTK + VADER (감정 분석)
- ✅ Selenium (웹 스크래핑)
- ✅ Pandas, Matplotlib, Plotly (데이터 처리 및 시각화)
- ⚠️ Wordcloud (선택 사항 - C++ 컴파일러 필요)

## 서버 실행 방법

### 방법 1: 배치 파일 사용 (Windows)
```bash
START_SERVER.bat
```

### 방법 2: 직접 실행
```bash
python app.py
```

## 접속 방법

서버가 시작되면 브라우저에서 다음 주소로 접속하세요:
```
http://localhost:5000
```

## 사용 방법

1. **게임 검색**: 게임 ID 또는 게임 이름 입력
2. **리뷰 수집**: 수집할 리뷰 수 설정 (10-500개)
3. **분석 시작**: "리뷰 분석 시작" 버튼 클릭
4. **결과 확인**: 
   - 통계 카드 확인
   - 시각화 차트 확인
   - 리뷰 데이터 샘플 확인

## 기능

### ✅ CORS 제한 해결
- Flask 서버를 통해 Steam API 호출
- 브라우저 CORS 정책 우회

### ✅ 정확한 감정 분석
- 서버 사이드에서 NLTK VADER 사용
- 클라이언트 사이드보다 훨씬 정확한 분석

### ✅ 다양한 시각화
- 추천 분포
- 감정 레이블 분포
- 파이 차트
- 박스 플롯
- 워드 클라우드 (wordcloud 설치 시)

## 문제 해결

### 포트 5000이 사용 중일 때
`app.py` 파일의 마지막 줄을 수정:
```python
app.run(debug=True, host='0.0.0.0', port=8000)  # 포트 변경
```

### 서버가 시작되지 않을 때
1. Python이 설치되어 있는지 확인: `python --version`
2. 필요한 패키지가 설치되어 있는지 확인: `python test_project.py`
3. 다른 터미널에서 실행 중인지 확인

## Wordcloud 설치 (선택 사항)

워드 클라우드 기능을 사용하려면:
1. [Microsoft C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/) 설치
2. `pip install wordcloud` 실행

Wordcloud 없이도 모든 기능이 정상 작동합니다!


