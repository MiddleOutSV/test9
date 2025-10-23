# 배포 가이드 (Deployment Guide)

이 문서는 Stock Lineup Visualizer를 무료로 웹에 배포하는 상세한 가이드입니다.

## 빠른 시작 (5분 안에 배포하기)

### 방법 1: Railway + Vercel (가장 추천!)

**장점:**
- 완전 무료
- GitHub 계정만 있으면 됨
- 자동 배포 (코드 푸시하면 자동 재배포)
- HTTPS 자동 설정
- 가장 빠르고 안정적

#### Step 1: Backend를 Railway에 배포

1. **Railway 접속 및 로그인**
   - https://railway.app/ 접속
   - "Start a New Project" 클릭
   - GitHub으로 로그인

2. **프로젝트 생성**
   - "Deploy from GitHub repo" 선택
   - 이 저장소(test9) 선택
   - "Deploy Now" 클릭

3. **서비스 설정**
   - 생성된 서비스 클릭
   - Settings 탭에서:
     - **Root Directory**: `backend` 입력
     - **Start Command**: `python app.py` 입력
   - Deploy 탭으로 가서 자동 배포 시작 확인

4. **URL 확인 및 복사**
   - Settings 탭에서 "Generate Domain" 클릭
   - 생성된 URL 복사 (예: `https://stock-lineup-backend.railway.app`)
   - `/api/health` 를 URL 뒤에 붙여서 접속해 `{"status":"healthy"}` 확인

#### Step 2: Frontend를 Vercel에 배포

1. **Vercel 접속 및 로그인**
   - https://vercel.com/ 접속
   - "Start Deploying" 클릭
   - GitHub으로 로그인

2. **프로젝트 Import**
   - "Import Git Repository" 클릭
   - 이 저장소(test9) 선택

3. **프로젝트 설정**
   - **Framework Preset**: Create React App 선택
   - **Root Directory**: `frontend` 선택 (Edit 클릭해서 변경)
   - **Environment Variables** 추가:
     ```
     Name: REACT_APP_API_URL
     Value: https://your-railway-backend-url.railway.app
     ```
     (Step 1에서 복사한 Railway URL을 붙여넣기)

4. **배포**
   - "Deploy" 클릭
   - 2-3분 기다리면 배포 완료!
   - Vercel이 제공하는 URL로 접속 (예: `https://your-app.vercel.app`)

**완료! 🎉**

---

## 방법 2: Render (모든 것을 한 곳에서)

**장점:**
- Frontend와 Backend를 한 곳에서 관리
- 무료 플랜 제공
- 간단한 설정

**단점:**
- 무료 플랜은 15분간 요청이 없으면 sleep (재시작에 30초~1분 소요)

#### Backend 배포

1. **Render 가입**
   - https://render.com/ 접속
   - GitHub으로 로그인

2. **New Web Service 생성**
   - Dashboard에서 "New +" → "Web Service" 클릭
   - GitHub 저장소 연결

3. **설정**
   ```
   Name: stock-lineup-backend
   Region: Oregon (US West)
   Branch: main (또는 현재 브랜치 이름)
   Root Directory: backend
   Runtime: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: python app.py
   Instance Type: Free
   ```

4. **배포 및 URL 확인**
   - "Create Web Service" 클릭
   - 배포 완료 후 상단에 URL 표시됨
   - URL 복사 (예: `https://stock-lineup-backend.onrender.com`)

#### Frontend 배포

1. **New Static Site 생성**
   - Dashboard에서 "New +" → "Static Site" 클릭
   - 같은 저장소 선택

2. **설정**
   ```
   Name: stock-lineup-frontend
   Branch: main
   Root Directory: frontend
   Build Command: npm install && npm run build
   Publish Directory: build
   ```

3. **Environment Variables 추가**
   - "Advanced" 클릭
   - 환경 변수 추가:
     ```
     Key: REACT_APP_API_URL
     Value: https://stock-lineup-backend.onrender.com
     ```
     (위에서 복사한 Backend URL)

4. **배포**
   - "Create Static Site" 클릭
   - 배포 완료 후 제공되는 URL로 접속!

---

## 방법 3: Netlify (Frontend) + Railway (Backend)

Railway는 위와 동일하게 진행하고, Frontend만 Netlify 사용:

1. **Netlify 가입**
   - https://netlify.com/ 접속
   - GitHub으로 로그인

2. **New site from Git**
   - "Add new site" → "Import an existing project" 클릭
   - GitHub 저장소 선택

3. **Build Settings**
   ```
   Base directory: frontend
   Build command: npm run build
   Publish directory: frontend/build
   ```

4. **Environment Variables**
   - "Site settings" → "Environment variables" 클릭
   - 추가:
     ```
     Key: REACT_APP_API_URL
     Value: https://your-railway-url.railway.app
     ```

5. **Deploy**
   - 저장하면 자동 배포 시작
   - 완료되면 제공되는 URL로 접속

---

## 배포 후 확인 사항

### 1. Backend 테스트
브라우저에서 Backend URL + `/api/health` 접속:
```
https://your-backend-url.com/api/health
```
응답:
```json
{"status": "healthy"}
```

### 2. 티커 API 테스트
```
https://your-backend-url.com/api/ticker/AAPL?timeframe=1M
```
응답 예시:
```json
{
  "symbol": "AAPL",
  "name": "Apple Inc.",
  "exchange": "NMS",
  "countryCode": "US",
  "returns": 5.23,
  "timeframe": "1M"
}
```

### 3. Frontend 테스트
1. Frontend URL 접속
2. 티커 입력 (예: AAPL)
3. "Add Ticker" 클릭
4. 데이터가 로드되는지 확인
5. 드래그가 작동하는지 확인

---

## 문제 해결

### CORS 에러
```
Access to fetch at 'https://backend...' from origin 'https://frontend...' has been blocked by CORS policy
```

**해결:**
- Backend의 `app.py`에 CORS가 활성화되어 있는지 확인 (이미 설정됨)
- Frontend의 환경 변수 확인

### Backend 연결 안 됨
```
Failed to fetch
```

**해결:**
1. Backend URL이 올바른지 확인
2. Backend가 정상 작동하는지 `/api/health` 확인
3. Frontend 환경 변수 `REACT_APP_API_URL` 확인
4. 환경 변수 변경 후에는 Frontend 재배포 필요!

### 티커 데이터가 로드되지 않음

**해결:**
1. 유효한 티커 심볼인지 확인
2. 인터넷 연결 확인
3. Backend 로그 확인 (Railway/Render 대시보드에서)
4. 일부 티커는 데이터가 제한적일 수 있음

### Render 무료 플랜 - 느린 첫 로딩

**원인:** 15분간 요청이 없으면 서버가 sleep 모드

**해결:** 없음 (무료 플랜의 한계). 유료 플랜($7/월)으로 업그레이드하면 해결됨.

**완화 방법:**
- UptimeRobot 같은 서비스로 5분마다 ping 보내기 (sleep 방지)
- 사용자에게 첫 로딩이 느릴 수 있다고 안내

---

## 커스텀 도메인 연결 (선택사항)

### Vercel
1. Dashboard → Settings → Domains
2. 도메인 입력 및 DNS 설정 안내 따라하기

### Netlify
1. Site settings → Domain management → Add custom domain
2. DNS 설정 안내 따라하기

### Railway
1. Settings → Domains → Custom Domain
2. DNS CNAME 레코드 추가

---

## 비용

모든 추천 방법은 **완전 무료**입니다!

| 서비스 | 무료 플랜 제한 |
|--------|---------------|
| **Railway** | $5 무료 크레딧/월 (충분함) |
| **Vercel** | 100GB 대역폭/월, 무제한 배포 |
| **Netlify** | 100GB 대역폭/월, 300분 빌드/월 |
| **Render** | 750시간/월 (무료, sleep 있음) |

---

## 자동 배포 설정

GitHub에 푸시하면 자동으로 재배포되도록 이미 설정되어 있습니다!

```bash
git add .
git commit -m "Update feature"
git push
```

→ Railway, Vercel, Netlify 모두 자동으로 감지하고 재배포합니다.

---

## 추가 도움말

- Railway 문서: https://docs.railway.app/
- Vercel 문서: https://vercel.com/docs
- Render 문서: https://render.com/docs
- Netlify 문서: https://docs.netlify.com/

**질문이 있다면:**
1. 각 플랫폼의 로그 확인
2. 브라우저 개발자 도구(F12) Console 탭 확인
3. GitHub Issues에 질문 남기기

행운을 빕니다! 🚀⚽📈
