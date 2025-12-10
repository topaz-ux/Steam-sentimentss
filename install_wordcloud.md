# Wordcloud 설치 가이드

Wordcloud는 C++ 컴파일러가 필요합니다. 다음 방법 중 하나를 선택하세요.

## 방법 1: Microsoft C++ Build Tools 설치 (권장)

1. [Microsoft C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/) 다운로드
2. 설치 시 "C++ build tools" 워크로드 선택
3. 설치 완료 후 재부팅
4. 다음 명령어 실행:
   ```bash
   pip install wordcloud
   ```

## 방법 2: Conda 사용 (대안)

Conda를 사용하면 사전 컴파일된 패키지를 설치할 수 있습니다:

```bash
conda install -c conda-forge wordcloud
```

## 방법 3: Wordcloud 없이 사용

Wordcloud는 **선택 사항**입니다. 워드 클라우드 기능만 사용할 수 없고, 나머지 모든 기능은 정상 작동합니다:
- ✅ Steam 리뷰 스크래핑
- ✅ 감정 분석 (NLTK VADER)
- ✅ 모든 시각화 (워드 클라우드 제외)
- ✅ Flask 웹 애플리케이션

현재 프로젝트는 wordcloud 없이도 완전히 작동합니다!


