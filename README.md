# 한국-일본 검색어 트렌드 비교 웹앱

pytrends를 이용하여 한국과 일본의 실시간 검색어 트렌드를 비교하는 웹 애플리케이션입니다.

## 🎯 두 가지 버전 제공!

이 프로젝트는 **두 가지 버전**으로 제공됩니다 - 필요에 맞게 선택하세요:

### 1. **Flask + HTML 버전** (이 README)
- ✅ 완전한 커스터마이징 가능
- ✅ 프로페셔널한 UI/UX
- ✅ 백엔드/프론트엔드 분리 구조
- ⚠️ 백엔드 + 프론트엔드 각각 배포 필요
- 📂 코드: `backend/` 폴더 + `index.html`

### 2. **Streamlit 버전** ([STREAMLIT_DEPLOYMENT.md](STREAMLIT_DEPLOYMENT.md) 참고)
- ✅ **3분만에 배포!** (가장 쉬움)
- ✅ 단일 Python 파일
- ✅ 자동 리로드 & 캐싱 내장
- ⚠️ 커스터마이징 제약
- 📂 코드: `streamlit_app/trends_app.py`

**빠른 추천:**
- 빠르게 배포하고 싶다면? → **Streamlit 버전** ✅
- 완전한 커스터마이징이 필요하다면? → **Flask + HTML 버전** ✅

---

## 기능

- **실시간 트렌드 비교**: 한국과 일본의 인기 검색어를 좌우로 나란히 표시
- **기간 선택**: 오늘, 지난 1주일, 지난 1달 중 선택 가능
- **반응형 디자인**: 모바일과 데스크톱 모두에서 최적화된 UI
- **자동 새로고침**: 기간 변경 시 자동으로 데이터 갱신

## 기술 스택

### 백엔드
- Python 3.x
- Flask (웹 프레임워크)
- pytrends (Google Trends API)
- Flask-CORS (CORS 지원)

### 프론트엔드
- HTML5
- CSS3
- Vanilla JavaScript

## 설치 및 실행

### 1. 필수 패키지 설치

```bash
cd backend
pip install -r requirements.txt
```

### 2. 백엔드 서버 실행

```bash
cd backend
python app.py
```

서버가 http://localhost:5000 에서 실행됩니다.

### 3. 프론트엔드 실행

간단한 HTTP 서버로 index.html을 서빙합니다:

```bash
# 프로젝트 루트 디렉토리에서
# Python 3 사용
python -m http.server 8000

# 또는 Node.js의 http-server 사용
npx http-server -p 8000
```

브라우저에서 http://localhost:8000 을 열면 웹앱을 사용할 수 있습니다.

## API 엔드포인트

### GET /api/trends

한국과 일본의 트렌딩 검색어를 가져옵니다.

**Parameters:**
- `timeframe` (optional): 1, 7, 또는 30 (기본값: 1)
  - 1: 오늘
  - 7: 지난 1주일
  - 30: 지난 1달

**Response:**
```json
{
  "korea": ["검색어1", "검색어2", ...],
  "japan": ["検索ワード1", "検索ワード2", ...],
  "timeframe": 1,
  "timestamp": "2025-10-26T12:00:00"
}
```

### GET /api/health

서버 상태 확인

**Response:**
```json
{
  "status": "healthy"
}
```

## 사용 방법

1. 웹 페이지에 접속합니다
2. 상단의 기간 버튼(오늘/지난 1주일/지난 1달)을 클릭합니다
3. 한국과 일본의 인기 검색어가 좌우로 표시됩니다
4. 검색어는 순위와 함께 표시됩니다

## 프로젝트 구조

```
pytrends-trend-comparison/
├── backend/
│   ├── app.py              # Flask API 서버
│   └── requirements.txt    # Python 의존성 패키지
├── index.html              # 프론트엔드 페이지
└── README.md               # 프로젝트 문서
```

## 주의사항

- Google Trends API는 요청 제한이 있을 수 있습니다
- 너무 자주 요청하면 일시적으로 차단될 수 있습니다
- 프로덕션 환경에서는 캐싱을 구현하는 것을 권장합니다
- `trending_searches()` API는 실시간 데이터를 제공하므로 timeframe 파라미터는 현재 구현에서 참고용입니다

## 배포

### Flask + HTML 버전 배포
상세한 배포 방법은 [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) 참고

**요약**:
- **백엔드**: Render, Railway 등 (무료)
- **프론트엔드**: Netlify, Vercel, GitHub Pages 등 (무료)
- `index.html`의 `API_URL`을 백엔드 URL로 변경 필요

### Streamlit 버전 배포 (3분 완성!)
상세한 배포 방법은 [STREAMLIT_DEPLOYMENT.md](STREAMLIT_DEPLOYMENT.md) 참고

**초간단 배포**:
1. https://streamlit.io/cloud 접속
2. GitHub 연결
3. `streamlit_app/trends_app.py` 선택
4. Deploy 클릭
5. 완료!

**Streamlit이 가장 쉬운 배포 방법입니다!** 처음 배포하시는 분들께 강력 추천합니다.

## 트러블슈팅

### CORS 에러 발생 시
- Flask-CORS가 올바르게 설치되어 있는지 확인
- 백엔드 서버가 정상적으로 실행 중인지 확인

### 데이터가 로드되지 않을 때
- 백엔드 서버가 실행 중인지 확인 (http://localhost:5000/api/health 접속)
- 브라우저 콘솔에서 에러 메시지 확인
- 인터넷 연결 상태 확인

## 라이선스

MIT License
