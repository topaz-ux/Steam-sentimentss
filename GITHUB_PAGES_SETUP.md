# GitHub Pages 배포 가이드

이 프로젝트는 GitHub Pages에서 서버 없이 바로 실행할 수 있습니다!

## 배포 방법

### 1단계: GitHub 저장소에 코드 푸시

```bash
git add .
git commit -m "GitHub Pages 배포 준비"
git push origin main
```

### 2단계: GitHub Pages 활성화

1. GitHub 저장소 페이지로 이동
2. **Settings** → **Pages** 메뉴 클릭
3. **Source**에서 **"GitHub Actions"** 선택
4. **Save** 클릭

### 3단계: 자동 배포

- `main` 또는 `master` 브랜치에 푸시하면 자동으로 배포됩니다
- **Actions** 탭에서 배포 상태 확인 가능
- 배포 완료 후 `https://사용자명.github.io/저장소명/`에서 접속 가능

## 접속 주소

배포가 완료되면 다음 주소로 접속할 수 있습니다:
```
https://사용자명.github.io/저장소명/
```

예: `https://yourusername.github.io/Steam-sentiment/`

## 기능

### ✅ 클라이언트 사이드 실행
- 서버 없이 브라우저에서 직접 실행
- Steam API 호출 (CORS 프록시 사용)
- 클라이언트 사이드 감정 분석
- 실시간 시각화 생성

### ⚠️ CORS 제한
일부 브라우저에서는 CORS 정책으로 인해 작동하지 않을 수 있습니다:
- **해결 방법**: 로컬 Flask 앱 실행 (`python app.py`)
- GitHub Pages에서는 여러 CORS 프록시를 자동으로 시도합니다

## 배포 확인

1. **Actions 탭**에서 배포 상태 확인
2. 배포 완료 후 페이지 접속
3. 게임 검색 및 리뷰 분석 테스트

## 문제 해결

### 페이지가 표시되지 않을 때
- GitHub Pages 설정에서 "GitHub Actions"가 선택되어 있는지 확인
- Actions 탭에서 배포 오류 확인
- `.nojekyll` 파일이 있는지 확인

### CORS 오류가 발생할 때
- 여러 프록시를 자동으로 시도하지만 실패할 수 있음
- 로컬 Flask 앱 사용 권장 (`python app.py`)

### 배포가 실패할 때
- Actions 탭에서 오류 로그 확인
- `index.html`이 루트에 있는지 확인
- `.github/workflows/pages.yml` 파일 확인

## 파일 구조

GitHub Pages에 배포되는 파일:
- ✅ `index.html` - 메인 페이지
- ✅ `.nojekyll` - Jekyll 비활성화
- ✅ `.github/workflows/pages.yml` - 배포 워크플로우

제외되는 파일:
- Python 파일들 (`.py`)
- 데이터 파일들 (`.csv`, `.png`)
- 문서 파일들 (`.md`)
- 기타 개발 파일들

## 완료! 🎉

이제 GitHub Pages에서 서버 없이 바로 실행할 수 있습니다!


