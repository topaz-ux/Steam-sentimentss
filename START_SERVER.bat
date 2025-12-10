@echo off
chcp 65001 >nul
echo ========================================
echo Steam 감정 분석 Flask 서버 시작
echo ========================================
echo.
echo 서버를 시작합니다...
echo 브라우저에서 http://localhost:5000 으로 접속하세요!
echo.
echo 서버를 중지하려면 Ctrl+C를 누르세요.
echo ========================================
echo.

python app.py

pause

