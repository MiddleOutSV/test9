# Stock Lineup Visualizer - Streamlit Edition

축구 라인업처럼 주식 포트폴리오를 구성하는 Streamlit 웹앱입니다!

## Features

- ⚽ **축구장 레이아웃**: 실제 축구장처럼 보이는 초록 잔디 + 하얀 라인
- 🎯 **클릭 방식 배치**: 티커를 선택한 후 원하는 위치를 클릭
- 📊 **실시간 주식 데이터**: yfinance로 기업명과 수익률 조회
- 🎨 **성과별 색상**: 수익률에 따라 자동으로 색상 변경
- 📅 **다양한 기간**: 1주일, 1개월, 6개월, 1년
- 🏴 **거래소 국기**: 각 티커의 거래소 국기 표시
- 💯 **최대 11개**: 축구팀처럼 11명까지

## 로컬 실행 방법

### 1. 의존성 설치

```bash
cd streamlit_app
pip install -r requirements.txt
```

### 2. 앱 실행

```bash
streamlit run app.py
```

브라우저가 자동으로 열립니다! (보통 http://localhost:8501)

## 사용 방법

1. **티커 입력**: 좌측 사이드바에서 티커 심볼 입력 (예: AAPL)
2. **"Select Position" 클릭**: 티커 데이터를 불러옵니다
3. **축구장 클릭**: 원하는 위치를 클릭하여 티커 배치
4. **반복**: 최대 11개까지 추가
5. **기간 변경**: 상단 드롭다운에서 수익률 기간 선택

## 배포하기 (3분 안에!)

### Streamlit Community Cloud (완전 무료, 가장 쉬움!)

1. **Streamlit Cloud 접속**
   - https://streamlit.io/cloud 접속
   - GitHub으로 로그인

2. **앱 배포**
   - "New app" 클릭
   - Repository: 이 저장소 선택
   - Branch: `claude/stock-lineup-visualizer-011CUPf4kzhYdQ39asps1LBh` (또는 main)
   - Main file path: `streamlit_app/app.py`
   - "Deploy!" 클릭

3. **완료!**
   - 2-3분 기다리면 배포 완료
   - 제공되는 URL로 접속하면 바로 사용 가능!
   - 예: `https://your-app.streamlit.app`

**그게 전부입니다!** 환경 변수 설정도, 백엔드 배포도, 프론트엔드 빌드도 필요 없습니다.

### 배포 후 자동 업데이트

GitHub에 푸시하면 자동으로 재배포됩니다:

```bash
git add .
git commit -m "Update feature"
git push
```

→ Streamlit Cloud가 자동으로 감지하고 재배포!

## 색상 코드 (성과별)

| 수익률 | 색상 | 의미 |
|--------|------|------|
| > 10% | 🟢 Green | 탁월 |
| 5-10% | 🟡 Yellow-Green | 좋음 |
| 0-5% | 🔵 Blue | 긍정 |
| -5-0% | 🟠 Orange | 부정 |
| < -5% | 🔴 Red | 나쁨 |

## 추천 티커

### 기술주
- AAPL (Apple)
- GOOGL (Google)
- MSFT (Microsoft)
- TSLA (Tesla)
- NVDA (NVIDIA)
- META (Meta/Facebook)
- AMZN (Amazon)

### 금융주
- JPM (JPMorgan Chase)
- BAC (Bank of America)
- GS (Goldman Sachs)
- V (Visa)
- MA (Mastercard)

### 소비재
- WMT (Walmart)
- KO (Coca-Cola)
- PEP (PepsiCo)
- MCD (McDonald's)
- NKE (Nike)

### 헬스케어
- JNJ (Johnson & Johnson)
- PFE (Pfizer)
- UNH (UnitedHealth)
- ABBV (AbbVie)

## Flask/React 버전과의 차이점

| 기능 | Flask/React | Streamlit |
|------|-------------|-----------|
| **드래그앤드롭** | ✅ 지원 | ❌ 클릭 방식 |
| **배포 난이도** | 중간 (Backend + Frontend 별도) | 매우 쉬움 (클릭 3번) |
| **배포 시간** | ~8분 | ~3분 |
| **커스터마이징** | 자유로움 | 제한적 |
| **축구장 디자인** | 매우 정교 | 단순화 |
| **실시간 데이터** | ✅ | ✅ |
| **수익률 표시** | ✅ | ✅ |
| **국기 표시** | ✅ | ✅ |
| **무료 호스팅** | ✅ | ✅ |

## 문제 해결

### 티커 데이터를 불러올 수 없음

**원인:** 유효하지 않은 티커 심볼이거나 네트워크 문제

**해결:**
- 올바른 티커 심볼인지 확인 (대문자로 입력)
- 인터넷 연결 확인
- 다른 티커로 시도

### 클릭이 작동하지 않음

**원인:** `streamlit-plotly-events` 설치 문제

**해결:**
```bash
pip install --upgrade streamlit-plotly-events
streamlit run app.py
```

### Streamlit Cloud 배포 실패

**원인:** requirements.txt 경로 문제

**해결:**
- Main file path가 `streamlit_app/app.py`로 정확히 설정되었는지 확인
- requirements.txt가 같은 폴더에 있는지 확인

## 로컬 개발 팁

### 핫 리로드

Streamlit은 파일을 저장하면 자동으로 "Rerun" 버튼이 표시됩니다. 클릭하면 변경사항이 즉시 반영됩니다.

### 디버깅

```python
st.write(st.session_state)  # 세션 상태 확인
st.write(players)  # 변수 확인
```

### 캐싱으로 성능 향상

자주 호출되는 함수에 `@st.cache_data` 추가:

```python
@st.cache_data(ttl=3600)  # 1시간 캐시
def get_ticker_info(symbol, timeframe):
    # ...
```

## 기술 스택

- **Streamlit**: 웹 프레임워크
- **Plotly**: 인터랙티브 그래픽
- **yfinance**: 주식 데이터
- **streamlit-plotly-events**: 클릭 이벤트 처리
- **Pandas**: 데이터 처리

## 프로젝트 구조

```
streamlit_app/
├── app.py              # 메인 애플리케이션
├── requirements.txt    # Python 의존성
└── README.md          # 이 파일
```

## 향후 개선 사항

- [ ] 포메이션 프리셋 (4-4-2, 4-3-3 등)
- [ ] 라인업 저장/불러오기
- [ ] 이미지로 내보내기
- [ ] 섹터/산업 정보 추가
- [ ] 여러 라인업 비교
- [ ] 히스토리 성과 추적

## 라이센스

MIT License - 자유롭게 사용하세요!

## 도움말

- Streamlit 문서: https://docs.streamlit.io/
- yfinance 문서: https://pypi.org/project/yfinance/
- 이슈 제보: GitHub Issues

---

Built with ⚽ and 📈 using Streamlit
