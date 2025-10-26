# Streamlit 버전 배포 가이드

## 🎯 Streamlit이란?

Streamlit은 Python으로 데이터 앱을 쉽게 만들 수 있는 프레임워크입니다. **별도의 백엔드/프론트엔드 분리 없이 단일 Python 파일로 전체 웹앱을 만들 수 있습니다!**

## ⚡ 왜 Streamlit을 사용하나요?

### 장점
- ✅ **초간단 배포**: 3분이면 배포 완료!
- ✅ **완전 무료**: Streamlit Cloud 무료 플랜
- ✅ **코드 간결**: 한 파일에 모든 로직
- ✅ **자동 리로드**: 코드 변경 시 자동 업데이트
- ✅ **캐싱 내장**: `@st.cache_data` 데코레이터로 쉽게 캐싱

### 단점
- ⚠️ 커스터마이징 제약: HTML/CSS 자유도가 Flask+React보다 낮음
- ⚠️ 고급 인터랙션: 복잡한 UI는 구현이 어려움

## 🚀 배포 방법 (3분 완성!)

### 방법 1: Streamlit Cloud (가장 추천!)

#### 1단계: 파일 확인

프로젝트에 다음 파일이 있는지 확인:
```
streamlit_app/
├── trends_app.py          # 메인 앱 파일
└── requirements.txt       # 패키지 목록
```

#### 2단계: GitHub에 푸시

```bash
git add streamlit_app/
git commit -m "Add Streamlit trends app"
git push
```

#### 3단계: Streamlit Cloud 배포

1. **Streamlit Cloud 접속**
   - https://streamlit.io/cloud 접속
   - GitHub 계정으로 로그인

2. **New app 클릭**
   - "New app" 버튼 클릭

3. **설정**
   ```
   Repository: your-username/your-repo
   Branch: main
   Main file path: streamlit_app/trends_app.py
   ```

4. **Deploy!**
   - "Deploy!" 버튼 클릭
   - 약 2-3분 후 배포 완료!

5. **완료!**
   - `https://your-app-name.streamlit.app` 형태의 URL 생성
   - 친구들과 공유 가능!

---

### 방법 2: 로컬에서 실행

배포 전 로컬에서 테스트하기:

```bash
# streamlit_app 디렉토리로 이동
cd streamlit_app

# 패키지 설치
pip install -r requirements.txt

# 앱 실행
streamlit run trends_app.py
```

브라우저가 자동으로 열리며 `http://localhost:8501`에서 확인 가능!

---

## 🎨 Streamlit vs Flask+React 비교

### Streamlit 버전 (streamlit_app/trends_app.py)
```python
# 한 파일에 모든 것
import streamlit as st
from pytrends.request import TrendReq

@st.cache_data(ttl=600)  # 캐싱 내장!
def get_trends():
    # 로직
    pass

st.title("트렌드 비교")  # UI가 간단!
```

### Flask+React 버전 (backend/ + index.html)
```python
# backend/app.py
from flask import Flask
# 백엔드 로직

# index.html
# 프론트엔드 로직 (별도 파일)
```

---

## 📊 두 버전 중 어떤 것을 선택할까?

| 기준 | Flask+React | Streamlit |
|------|-------------|-----------|
| 배포 난이도 | ⭐⭐⭐ (백엔드+프론트엔드 2곳) | ⭐ (한 곳만) |
| 배포 시간 | ~10분 | ~3분 |
| 커스터마이징 | ⭐⭐⭐⭐⭐ (완전 자유) | ⭐⭐⭐ (제한적) |
| UI 퀄리티 | ⭐⭐⭐⭐⭐ (완전 커스텀) | ⭐⭐⭐⭐ (깔끔하지만 제한적) |
| 코드 간결성 | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| 유지보수 | ⭐⭐⭐ (2개 파일) | ⭐⭐⭐⭐⭐ (1개 파일) |

### 추천
- **빠르게 배포하고 싶다** → **Streamlit** ✅
- **완전히 커스터마이징하고 싶다** → **Flask+React** ✅
- **데이터 분석/대시보드** → **Streamlit** ✅
- **복잡한 인터랙션** → **Flask+React** ✅

---

## 🔧 Streamlit 앱 커스터마이징

### 색상 변경
`.streamlit/config.toml` 파일 생성:

```toml
[theme]
primaryColor = "#667eea"
backgroundColor = "#764ba2"
secondaryBackgroundColor = "#8b5cf6"
textColor = "#ffffff"
font = "sans serif"
```

### 사이드바 추가 기능

`trends_app.py`에 추가:

```python
with st.sidebar:
    st.header("추가 설정")

    # 검색어 개수 조절
    max_items = st.slider("표시할 검색어 수", 5, 30, 20)

    # 새로고침 간격
    auto_refresh = st.checkbox("자동 새로고침")
    if auto_refresh:
        refresh_interval = st.slider("새로고침 간격 (초)", 30, 300, 60)
```

---

## 📱 Streamlit Cloud 무료 플랜 제약

- **앱 개수**: 1개 무료 (Public 앱)
- **리소스**: 1GB RAM, 공유 CPU
- **대역폭**: 무제한
- **슬립 모드**: 7일간 미사용 시 자동 중지 (재접속 시 자동 시작)

**충분한 리소스**: 이 앱은 무료 플랜으로 충분합니다!

---

## 🎯 배포 후 체크리스트

- [ ] Streamlit Cloud에 앱 배포 완료
- [ ] URL 접속 확인 (`https://your-app.streamlit.app`)
- [ ] 한국/일본 트렌드 데이터 로딩 확인
- [ ] 기간 선택 버튼 작동 확인
- [ ] 새로고침 버튼 작동 확인
- [ ] 모바일에서 접속 테스트
- [ ] 친구들과 URL 공유!

---

## 💡 팁

### 1. 자동 배포
GitHub에 코드를 푸시하면 Streamlit Cloud가 자동으로 재배포합니다!

```bash
# 코드 수정 후
git add .
git commit -m "Update trends app"
git push

# Streamlit Cloud가 자동으로 재배포! (약 1-2분)
```

### 2. 로그 확인
Streamlit Cloud 대시보드에서 실시간 로그 확인 가능

### 3. 비밀번호 보호
Settings → Secrets에서 환경 변수 추가 가능

---

## 🐛 트러블슈팅

### 문제: 앱이 로딩되지 않음
**해결**:
- Streamlit Cloud 로그 확인
- requirements.txt에 모든 패키지가 있는지 확인
- Python 버전 호환성 확인 (3.8 이상 권장)

### 문제: Google Trends API 에러
**해결**:
- 캐싱이 작동하고 있는지 확인 (`@st.cache_data(ttl=600)`)
- 너무 자주 새로고침하지 않기 (10분 간격 권장)
- 로그에서 에러 메시지 확인

### 문제: 앱이 느림
**해결**:
- 캐싱 활용 (`@st.cache_data`)
- 불필요한 API 호출 최소화
- Streamlit의 `st.spinner()`로 로딩 표시

---

## 🎉 완료!

이제 Streamlit으로 초간단 배포를 즐기세요!

**Streamlit Cloud URL**: `https://your-app.streamlit.app`

친구들과 공유하고, 실시간 트렌드를 확인해보세요! 🚀
