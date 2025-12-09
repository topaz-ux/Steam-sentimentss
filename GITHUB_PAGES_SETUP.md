# 🌐 GitHub Pages 설정 가이드

## 📋 설정 방법

### 1단계: Static HTML 워크플로우 선택

1. **"Static HTML"** 카드에서 **"Configure"** 버튼 클릭
2. 자동으로 워크플로우 파일이 생성됩니다

### 2단계: 워크플로우 파일 커밋

1. 생성된 워크플로우 파일을 확인
2. 커밋 메시지 입력 (예: "Add GitHub Pages workflow")
3. **"Commit new file"** 클릭

### 3단계: 배포 완료 대기

1. **Actions** 탭으로 이동
2. 워크플로우가 실행되는 것을 확인
3. 완료되면 (약 1-2분) 사이트가 배포됩니다

### 4단계: 사이트 접속

배포가 완료되면 다음 주소로 접속할 수 있습니다:
```
https://topaz-ux.github.io/Steam-sentiment/
```

---

## ✅ 이미 생성된 파일

프로젝트에 다음 파일들이 이미 포함되어 있습니다:

- ✅ `.github/workflows/pages.yml` - GitHub Pages 워크플로우
- ✅ `index.html` - 메인 페이지 (results_demo.html과 동일한 내용)

---

## 🚀 빠른 설정 (이미 파일이 있는 경우)

### 방법 1: Static HTML 워크플로우 사용

1. **"Static HTML"** 카드에서 **"Configure"** 클릭
2. 생성된 파일 확인 후 커밋

### 방법 2: 이미 생성된 워크플로우 사용

이미 `.github/workflows/pages.yml` 파일이 있으므로:

1. 파일을 커밋하고 푸시
2. GitHub Pages 설정에서 **"GitHub Actions"**가 선택되어 있는지 확인
3. 자동으로 배포가 시작됩니다

---

## 📝 설정 확인

### Source 설정
- **Source**: `GitHub Actions` (또는 `Deploy from a branch`)
- 워크플로우가 자동으로 실행됩니다

### Enforce HTTPS
- ✅ 체크되어 있어야 합니다 (기본 도메인 사용 시 필수)

---

## 🔍 문제 해결

### 워크플로우가 실행되지 않는 경우

1. **Actions** 탭에서 워크플로우 확인
2. 오류 메시지 확인
3. 브랜치 이름 확인 (`main` 또는 `master`)

### 사이트가 표시되지 않는 경우

1. 배포가 완료될 때까지 대기 (1-2분)
2. 브라우저 캐시 지우기
3. 올바른 URL 확인: `https://yourusername.github.io/Steam-sentiment/`

---

## 💡 팁

- 워크플로우는 `main` 브랜치에 푸시할 때마다 자동으로 실행됩니다
- `index.html` 파일이 루트 디렉토리에 있어야 합니다
- 배포는 보통 1-2분 정도 소요됩니다

---

**"Static HTML"의 "Configure" 버튼을 클릭하면 자동으로 설정됩니다!** 🚀

