# 배포 가이드

한국-일본 검색어 트렌드 비교 웹앱을 온라인으로 배포하는 방법입니다.

## 🚀 방법 1: Render (가장 추천! - 완전 무료)

### 백엔드 배포

1. **Render 계정 생성**
   - https://render.com 접속
   - GitHub 계정으로 로그인

2. **새 Web Service 생성**
   - Dashboard에서 "New +" 버튼 클릭
   - "Web Service" 선택
   - GitHub 저장소 연결 (이 저장소 선택)

3. **설정**
   ```
   Name: trends-backend (원하는 이름)
   Region: Oregon (또는 Singapore - 한국과 가까움)
   Branch: main
   Root Directory: backend
   Runtime: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: python app.py
   Plan: Free
   ```

4. **환경 변수 설정**
   - Environment Variables 섹션에서 추가:
   ```
   PYTHON_VERSION = 3.11.0
   ```

5. **Deploy** 버튼 클릭
   - 배포 완료 후 URL 복사 (예: `https://trends-backend.onrender.com`)

### 프론트엔드 배포

#### 옵션 A: Netlify (추천)

1. **index.html 파일 수정**
   - 백엔드 URL을 Render에서 받은 URL로 변경해야 합니다
   - 아래에서 자동으로 수정해드리겠습니다

2. **Netlify 배포**
   - https://netlify.com 접속
   - GitHub 계정으로 로그인
   - "Add new site" → "Import an existing project"
   - GitHub 저장소 선택

3. **설정**
   ```
   Branch to deploy: main
   Base directory: (비워두기)
   Build command: (비워두기)
   Publish directory: .
   ```

4. **Deploy** 클릭
   - 완료!

#### 옵션 B: Vercel

1. **Vercel 배포**
   - https://vercel.com 접속
   - GitHub 계정으로 로그인
   - "New Project" 클릭
   - 이 저장소 선택

2. **설정**
   ```
   Framework Preset: Other
   Root Directory: (비워두기)
   Build Command: (비워두기)
   Output Directory: .
   ```

3. **Deploy** 클릭

#### 옵션 C: GitHub Pages

1. **GitHub Settings**
   - 저장소 → Settings → Pages
   - Source: Deploy from a branch
   - Branch: main, / (root)
   - Save

2. **Actions 탭에서 배포 확인**
   - 몇 분 후 `https://yourusername.github.io/repository-name` 에서 접속 가능

---

## 🚀 방법 2: Railway (백엔드) + Netlify (프론트엔드)

### 백엔드: Railway

1. **Railway 계정 생성**
   - https://railway.app 접속
   - GitHub 계정으로 로그인

2. **새 프로젝트**
   - "New Project" → "Deploy from GitHub repo"
   - 이 저장소 선택

3. **설정**
   - Root Directory: `backend`
   - Start Command: `python app.py`
   - 자동으로 requirements.txt 인식

4. **도메인 설정**
   - Settings → Generate Domain
   - URL 복사 (예: `https://your-app.railway.app`)

### 프론트엔드: Netlify (위와 동일)

---

## 🚀 방법 3: PythonAnywhere (올인원 - 가장 쉬움!)

백엔드와 프론트엔드를 한 곳에서 모두 호스팅할 수 있습니다.

1. **PythonAnywhere 계정 생성**
   - https://www.pythonanywhere.com 접속
   - 무료 계정 생성 (Beginner)

2. **새 Web App 생성**
   - Web 탭 → "Add a new web app"
   - Flask 선택
   - Python 3.10 선택

3. **파일 업로드**
   - Files 탭에서 코드 업로드
   - 또는 GitHub에서 clone:
   ```bash
   git clone https://github.com/yourusername/your-repo.git
   ```

4. **패키지 설치**
   - Consoles 탭 → Bash console
   ```bash
   cd your-repo/backend
   pip install -r requirements.txt
   ```

5. **WSGI 설정**
   - Web 탭 → WSGI configuration file 클릭
   - 파일 내용을 다음과 같이 수정:
   ```python
   import sys
   path = '/home/yourusername/your-repo/backend'
   if path not in sys.path:
       sys.path.append(path)

   from app import app as application
   ```

6. **Static Files 설정**
   - Web 탭 → Static files 섹션
   - URL: `/`, Directory: `/home/yourusername/your-repo/`

7. **Reload** 버튼 클릭
   - `http://yourusername.pythonanywhere.com` 에서 접속!

---

## 📝 중요: 프론트엔드 API URL 수정

배포 후 index.html의 API URL을 수정해야 합니다:

```javascript
// 현재 (로컬 개발용)
const API_URL = window.location.hostname === 'localhost'
    ? 'http://localhost:5000'
    : 'https://your-backend-url.com';

// 배포 후 (실제 백엔드 URL로 변경)
const API_URL = 'https://trends-backend.onrender.com';  // 실제 백엔드 URL
```

---

## 🔍 배포 후 체크리스트

- [ ] 백엔드 health check 확인: `https://your-backend-url/api/health`
- [ ] 프론트엔드에서 데이터 로딩 확인
- [ ] 기간 변경 버튼 작동 확인
- [ ] 모바일에서 접속 테스트

---

## ⚠️ 주의사항

### Google Trends API 제한
- pytrends는 Google의 비공식 API를 사용합니다
- 너무 많은 요청을 보내면 일시적으로 차단될 수 있습니다
- **권장**: 캐싱 구현 (5-10분마다 한 번만 API 호출)

### 무료 플랜 제한
- **Render**: 15분간 요청이 없으면 슬립 모드 (첫 요청 시 느림)
- **Railway**: 월 500시간 무료 (약 20일)
- **PythonAnywhere**: 1개 웹앱만 무료

---

## 💡 캐싱 추가 (선택사항)

API 호출을 줄이기 위해 캐싱을 추가하는 것을 권장합니다:

```python
# backend/app.py에 추가
from datetime import datetime, timedelta
import json

cache = {}
CACHE_DURATION = timedelta(minutes=10)

def get_cached_trends(timeframe):
    cache_key = f"trends_{timeframe}"

    if cache_key in cache:
        cached_data, cached_time = cache[cache_key]
        if datetime.now() - cached_time < CACHE_DURATION:
            return cached_data

    # 새로운 데이터 가져오기
    kr_trends = get_trending_searches('KR', timeframe)
    jp_trends = get_trending_searches('JP', timeframe)

    data = {
        'korea': kr_trends,
        'japan': jp_trends,
        'timeframe': timeframe
    }

    cache[cache_key] = (data, datetime.now())
    return data
```

---

## 🎉 완료!

배포가 완료되면 친구들과 링크를 공유할 수 있습니다!
