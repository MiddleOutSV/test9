import streamlit as st
from pytrends.request import TrendReq
from datetime import datetime
import pandas as pd
import time

# 페이지 설정
st.set_page_config(
    page_title="한국-일본 검색어 트렌드 비교",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 커스텀 CSS
st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    h1 {
        color: white;
        text-align: center;
        padding: 20px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    .subtitle {
        color: white;
        text-align: center;
        opacity: 0.9;
        margin-bottom: 30px;
    }
    .trend-card {
        background: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        margin: 10px 0;
    }
    .rank-number {
        font-size: 1.5rem;
        font-weight: bold;
        color: #667eea;
    }
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 10px 30px;
        font-weight: 600;
    }
    </style>
""", unsafe_allow_html=True)

# 캐시를 사용한 트렌드 데이터 가져오기
@st.cache_data(ttl=600)  # 10분간 캐시
def get_trending_searches(country_code, timeframe_days):
    """
    Get trending searches for a specific country
    country_code: 'KR' for Korea, 'JP' for Japan
    timeframe_days: 1, 7, or 30 (참고용)
    """
    try:
        pytrends = TrendReq(hl='ko' if country_code == 'KR' else 'ja', tz=540)

        # Get trending searches for the country
        trending_searches_df = pytrends.trending_searches(pn=country_code.lower())

        # Convert to list and limit to top 20
        trends = trending_searches_df[0].head(20).tolist()

        return trends
    except Exception as e:
        st.error(f"Error getting trends for {country_code}: {e}")
        return []

def main():
    # 헤더
    st.markdown("<h1>🇰🇷 한국-일본 검색어 트렌드 비교 🇯🇵</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>실시간으로 양국의 인기 검색어를 확인하세요</p>", unsafe_allow_html=True)

    # 사이드바 설정
    with st.sidebar:
        st.header("⚙️ 설정")

        timeframe = st.radio(
            "기간 선택",
            options=[1, 7, 30],
            format_func=lambda x: {1: "오늘", 7: "지난 1주일", 30: "지난 1달"}[x],
            help="참고: Google Trends는 실시간 트렌드를 제공합니다"
        )

        st.markdown("---")

        if st.button("🔄 새로고침", use_container_width=True):
            st.cache_data.clear()
            st.rerun()

        st.markdown("---")
        st.markdown("""
        ### 📊 사용 방법
        1. 기간을 선택하세요
        2. 한국과 일본의 인기 검색어가 표시됩니다
        3. 새로고침 버튼으로 최신 데이터를 가져올 수 있습니다

        ### ⏱️ 캐싱
        - 데이터는 10분간 캐시됩니다
        - API 호출 제한을 방지합니다
        """)

    # 데이터 로딩
    with st.spinner('트렌드 데이터를 불러오는 중...'):
        col1, col2 = st.columns(2)

        # 한국 트렌드
        with col1:
            st.markdown("### 🇰🇷 한국 인기 검색어")
            kr_trends = get_trending_searches('KR', timeframe)

            if kr_trends:
                # DataFrame 생성
                kr_df = pd.DataFrame({
                    '순위': range(1, len(kr_trends) + 1),
                    '검색어': kr_trends
                })

                # 스타일 적용
                st.dataframe(
                    kr_df,
                    hide_index=True,
                    use_container_width=True,
                    height=600
                )
            else:
                st.warning("한국 트렌드 데이터를 불러올 수 없습니다.")

        # 일본 트렌드
        with col2:
            st.markdown("### 🇯🇵 일본 인기 검색어")
            jp_trends = get_trending_searches('JP', timeframe)

            if jp_trends:
                # DataFrame 생성
                jp_df = pd.DataFrame({
                    '順位': range(1, len(jp_trends) + 1),
                    '検索ワード': jp_trends
                })

                # 스타일 적용
                st.dataframe(
                    jp_df,
                    hide_index=True,
                    use_container_width=True,
                    height=600
                )
            else:
                st.warning("일본 트렌드 데이터를 불러올 수 없습니다.")

    # 하단 정보
    st.markdown("---")
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    st.markdown(f"""
    <div style='text-align: center; color: white; opacity: 0.8;'>
        <p>마지막 업데이트: {current_time} |
        데이터 출처: Google Trends |
        Made with Streamlit ❤️</p>
    </div>
    """, unsafe_allow_html=True)

    # 추가 정보
    with st.expander("ℹ️ 주의사항"):
        st.markdown("""
        - **Google Trends API 제한**: 너무 자주 요청하면 일시적으로 차단될 수 있습니다
        - **실시간 데이터**: trending_searches() API는 실시간 트렌드를 제공합니다
        - **캐싱**: 10분마다 한 번씩 API를 호출하여 안정적으로 운영됩니다
        - **timeframe 파라미터**: 현재 구현에서는 참고용이며, 실제로는 실시간 트렌드를 보여줍니다
        """)

if __name__ == "__main__":
    main()
