@echo off
chcp 65001 >nul
echo ========================================
echo Steam 감정 분석 프로젝트 설치 스크립트
echo ========================================
echo.

echo [1/4] Python 버전 확인 중...
python --version
if errorlevel 1 (
    echo [오류] Python이 설치되어 있지 않습니다.
    echo Python 3.8 이상을 설치해주세요: https://www.python.org/downloads/
    pause
    exit /b 1
)
echo.

echo [2/4] pip 업그레이드 중...
python -m pip install --upgrade pip
echo.

echo [3/4] 필요한 패키지 설치 중...
echo 이 작업은 몇 분이 걸릴 수 있습니다...
python -m pip install -r requirements.txt
if errorlevel 1 (
    echo [오류] 패키지 설치 중 오류가 발생했습니다.
    pause
    exit /b 1
)
echo.

echo [4/4] NLTK 데이터 다운로드 중...
python -c "import nltk; import ssl; ssl._create_default_https_context = ssl._create_unverified_context; nltk.download('stopwords', quiet=True); nltk.download('punkt', quiet=True); nltk.download('punkt_tab', quiet=True); nltk.download('vader_lexicon', quiet=True); nltk.download('averaged_perceptron_tagger', quiet=True); print('NLTK 데이터 다운로드 완료!')"
if errorlevel 1 (
    echo [경고] NLTK 데이터 다운로드 중 오류가 발생했습니다.
    echo 수동으로 다운로드할 수 있습니다.
)
echo.

echo ========================================
echo 설치가 완료되었습니다!
echo ========================================
echo.
echo 다음 명령어로 Flask 앱을 실행하세요:
echo   python app.py
echo.
echo 그 후 브라우저에서 http://localhost:5000 으로 접속하세요.
echo.
pause


