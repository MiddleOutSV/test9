import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime

# 페이지 설정
st.set_page_config(
    page_title="올에셋 라인업 빌더",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 커스텀 CSS
st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    .stSelectbox, .stTextInput {
        background-color: white;
    }
    h1 {
        color: white;
        text-align: center;
        font-size: 1.8rem;
    }
    .stAlert {
        background-color: rgba(255, 255, 255, 0.9);
    }
    /* 모바일 최적화 */
    @media (max-width: 768px) {
        h1 {
            font-size: 1.3rem;
        }
        .stButton button {
            width: 100%;
            font-size: 0.9rem;
        }
    }
    </style>
    """, unsafe_allow_html=True)

# 거래소 매핑
EXCHANGE_TO_COUNTRY = {
    'NMS': 'US', 'NYQ': 'US', 'PCX': 'US', 'BTS': 'US',
    'NGM': 'US', 'NCM': 'US', 'ASE': 'US',
    'LSE': 'GB', 'TSE': 'JP', 'HKG': 'HK',
    'FRA': 'DE', 'EPA': 'FR', 'TOR': 'CA',
}

# 포지션 정의 (4-3-3 포메이션, 세로 방향)
POSITIONS = {
    'GK': {'name': '골키퍼', 'x': 34, 'y': 95},
    'DF1': {'name': '오른쪽 풀백', 'x': 14, 'y': 75},
    'DF2': {'name': '중앙 수비수 1', 'x': 28, 'y': 75},
    'DF3': {'name': '중앙 수비수 2', 'x': 40, 'y': 75},
    'DF4': {'name': '왼쪽 풀백', 'x': 54, 'y': 75},
    'MF1': {'name': '오른쪽 미드필더', 'x': 15, 'y': 50},
    'MF2': {'name': '중앙 미드필더', 'x': 34, 'y': 50},
    'MF3': {'name': '왼쪽 미드필더', 'x': 53, 'y': 50},
    'FW1': {'name': '오른쪽 공격수', 'x': 20, 'y': 25},
    'FW2': {'name': '중앙 공격수', 'x': 34, 'y': 20},
    'FW3': {'name': '왼쪽 공격수', 'x': 48, 'y': 25},
}

def get_flag_emoji(country_code):
    """국가 코드를 국기 이모지로 변환"""
    if not country_code:
        return '🇺🇸'
    codepoints = [127397 + ord(char) for char in country_code.upper()]
    return ''.join(chr(cp) for cp in codepoints)

def get_period_for_timeframe(timeframe):
    """타임프레임을 yfinance period로 변환"""
    periods = {'1주일': '1mo', '1개월': '3mo', '6개월': '1y', '1년': '2y'}
    return periods.get(timeframe, '1y')

def calculate_returns(ticker_symbol, timeframe):
    """수익률 계산"""
    try:
        ticker = yf.Ticker(ticker_symbol)
        period = get_period_for_timeframe(timeframe)
        hist = ticker.history(period=period)

        if hist.empty:
            return None

        days_map = {'1주일': 7, '1개월': 30, '6개월': 180, '1년': 365}
        days_back = min(days_map.get(timeframe, 365), len(hist) - 1)

        if days_back < 1:
            return None

        start_price = hist['Close'].iloc[-days_back]
        current_price = hist['Close'].iloc[-1]
        returns = ((current_price - start_price) / start_price) * 100
        return round(returns, 2)
    except Exception as e:
        return None

def get_ticker_info(symbol, timeframe):
    """티커 정보 가져오기"""
    try:
        ticker = yf.Ticker(symbol.upper())
        info = ticker.info

        company_name = info.get('longName') or info.get('shortName') or symbol
        exchange = info.get('exchange', 'NMS')
        country_code = EXCHANGE_TO_COUNTRY.get(exchange, 'US')
        returns = calculate_returns(symbol.upper(), timeframe)

        return {
            'symbol': symbol.upper(),
            'name': company_name,
            'exchange': exchange,
            'countryCode': country_code,
            'returns': returns,
        }
    except Exception as e:
        st.error(f"❌ 티커 데이터를 가져오는데 실패했습니다: {symbol}")
        return None

def get_performance_color(returns):
    """성과에 따른 색상 반환 (빨강-파랑 그라데이션)"""
    if returns is None:
        return '#A0AEC0'  # 회색

    if returns >= 0:
        # 플러스 수익률: 연한 빨강 → 진한 빨강
        # 0% = 연한 빨강, 30% 이상 = 진한 빨강
        ratio = min(returns / 30.0, 1.0)  # 0.0 ~ 1.0
        # 연한 빨강 #FFB3B3 (255, 179, 179) → 진한 빨강 #CC0000 (204, 0, 0)
        r = int(255 - (51 * ratio))  # 255 → 204
        g = int(179 - (179 * ratio))  # 179 → 0
        b = int(179 - (179 * ratio))  # 179 → 0
        return f'#{r:02X}{g:02X}{b:02X}'
    else:
        # 마이너스 수익률: 연한 파랑 → 진한 파랑
        # 0% = 연한 파랑, -30% 이하 = 진한 파랑
        ratio = min(abs(returns) / 30.0, 1.0)  # 0.0 ~ 1.0
        # 연한 파랑 #B3D9FF (179, 217, 255) → 진한 파랑 #0066CC (0, 102, 204)
        r = int(179 - (179 * ratio))  # 179 → 0
        g = int(217 - (115 * ratio))  # 217 → 102
        b = int(255 - (51 * ratio))   # 255 → 204
        return f'#{r:02X}{g:02X}{b:02X}'

def create_soccer_field(players):
    """축구장 시각화 생성 (세로 방향)"""
    fig = go.Figure()

    # 축구장 크기 (세로 방향)
    field_width = 68
    field_length = 105

    # 잔디 배경 (세로 줄무늬)
    for i in range(0, int(field_width), 10):
        color = '#2D5016' if (i // 10) % 2 == 0 else '#3A6B1E'
        fig.add_shape(
            type="rect",
            x0=i, y0=0, x1=i+10, y1=field_length,
            fillcolor=color,
            line=dict(width=0),
            layer="below"
        )

    # 필드 외곽선
    fig.add_shape(type="rect", x0=0, y0=0, x1=field_width, y1=field_length,
                  line=dict(color="white", width=3), fillcolor="rgba(0,0,0,0)")

    # 중앙선
    fig.add_shape(type="line", x0=0, y0=field_length/2, x1=field_width, y1=field_length/2,
                  line=dict(color="white", width=2))

    # 센터 서클
    fig.add_shape(type="circle",
                  x0=field_width/2-9.15, y0=field_length/2-9.15,
                  x1=field_width/2+9.15, y1=field_length/2+9.15,
                  line=dict(color="white", width=2), fillcolor="rgba(0,0,0,0)")

    # 센터 스팟
    fig.add_shape(type="circle",
                  x0=field_width/2-0.5, y0=field_length/2-0.5,
                  x1=field_width/2+0.5, y1=field_length/2+0.5,
                  fillcolor="white", line=dict(color="white", width=0))

    # 페널티 박스 (상단과 하단)
    for y in [0, field_length]:
        direction = 1 if y == 0 else -1
        # 큰 페널티 박스
        fig.add_shape(type="rect",
                     x0=field_width/2-20.16, y0=y,
                     x1=field_width/2+20.16, y1=y+direction*16.5,
                     line=dict(color="white", width=2), fillcolor="rgba(0,0,0,0)")
        # 골 박스
        fig.add_shape(type="rect",
                     x0=field_width/2-9.16, y0=y,
                     x1=field_width/2+9.16, y1=y+direction*5.5,
                     line=dict(color="white", width=2), fillcolor="rgba(0,0,0,0)")
        # 페널티 스팟
        spot_y = 11 if y == 0 else field_length - 11
        fig.add_shape(type="circle",
                     x0=field_width/2-0.5, y0=spot_y-0.5,
                     x1=field_width/2+0.5, y1=spot_y+0.5,
                     fillcolor="white", line=dict(color="white", width=0))

    # 선수 추가
    if players:
        x_coords = [p['x'] for p in players]
        y_coords = [p['y'] for p in players]
        colors = [get_performance_color(p.get('returns')) for p in players]

        hover_texts = []
        for p in players:
            flag = get_flag_emoji(p.get('countryCode', 'US'))
            returns = p.get('returns')
            if returns is not None:
                returns_str = f"+{returns}%" if returns >= 0 else f"{returns}%"
            else:
                returns_str = "N/A"
            text = f"{flag} <b>{p['symbol']}</b><br>{p['name']}<br><b>{returns_str}</b><br>포지션: {p.get('position_name', '')}"
            hover_texts.append(text)

        fig.add_trace(go.Scatter(
            x=x_coords,
            y=y_coords,
            mode='markers+text',
            marker=dict(
                size=35,
                color=colors,
                line=dict(color='white', width=2.4),
                symbol='circle'
            ),
            text=[p['symbol'] for p in players],
            textposition="middle center",
            textfont=dict(color='white', size=11, family='Arial Black'),
            hovertext=hover_texts,
            hoverinfo='text',
            showlegend=False
        ))

    # 레이아웃 업데이트
    fig.update_layout(
        width=400,  # 모바일 최적화
        height=600,  # 세로로 긴 레이아웃
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(
            range=[-2, field_width+2],
            showgrid=False,
            zeroline=False,
            showticklabels=False,
        ),
        yaxis=dict(
            range=[-2, field_length+2],
            showgrid=False,
            zeroline=False,
            showticklabels=False,
            scaleanchor="x",
            scaleratio=1,
        ),
        margin=dict(l=10, r=10, t=10, b=10),
        hovermode='closest',
    )

    return fig

# 세션 상태 초기화
if 'players' not in st.session_state:
    st.session_state.players = []

# 메인 타이틀
st.markdown("<h1>⚽ 올에셋 라인업 빌더</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: white;'>축구 라인업처럼 나만의 주식 포트폴리오를 만들어보세요!</p>", unsafe_allow_html=True)

# 사이드바
with st.sidebar:
    st.header("📊 설정")

    # 타임프레임 선택
    timeframe = st.selectbox(
        "수익률 기간 선택",
        options=['1주일', '1개월', '6개월', '1년'],
        index=1
    )

    st.divider()

    # 티커 추가
    st.subheader("⚽ 선수 추가")

    # 사용 가능한 포지션 확인
    occupied_positions = [p['position'] for p in st.session_state.players]
    available_positions = {k: v for k, v in POSITIONS.items() if k not in occupied_positions}

    if len(st.session_state.players) >= 11:
        st.warning("⚠️ 최대 11명의 선수를 배치할 수 있습니다!")
    elif not available_positions:
        st.warning("⚠️ 모든 포지션이 채워졌습니다!")
    else:
        ticker_input = st.text_input(
            "티커 심볼 입력",
            placeholder="예: AAPL, GOOGL, TSLA",
            key="ticker_input"
        ).upper()

        # 포지션 선택
        position_key = st.selectbox(
            "포지션 선택",
            options=list(available_positions.keys()),
            format_func=lambda x: f"{available_positions[x]['name']} ({x})",
            key="position_select"
        )

        if st.button("➕ 선수 추가", use_container_width=True, type="primary"):
            if not ticker_input:
                st.error("❌ 티커를 입력해주세요!")
            else:
                with st.spinner(f'{ticker_input} 데이터 불러오는 중...'):
                    ticker_data = get_ticker_info(ticker_input, timeframe)
                    if ticker_data:
                        position_data = POSITIONS[position_key]
                        new_player = {
                            **ticker_data,
                            'position': position_key,
                            'position_name': position_data['name'],
                            'x': position_data['x'],
                            'y': position_data['y']
                        }
                        st.session_state.players.append(new_player)
                        st.success(f"✅ {ticker_input}를 {position_data['name']}에 배치했습니다!")
                        st.rerun()

    st.divider()

    # 전체 삭제
    if st.session_state.players:
        if st.button("🗑️ 전체 삭제", use_container_width=True):
            st.session_state.players = []
            st.rerun()

    # 선수 현황
    st.metric("현재 선수", f"{len(st.session_state.players)}/11")

    # 현재 라인업
    if st.session_state.players:
        st.subheader("📋 현재 라인업")
        for idx, player in enumerate(st.session_state.players):
            with st.container():
                col1, col2 = st.columns([4, 1])
                with col1:
                    flag = get_flag_emoji(player.get('countryCode', 'US'))
                    returns = player.get('returns')
                    if returns is not None:
                        returns_str = f"+{returns}%" if returns >= 0 else f"{returns}%"
                        st.caption(f"{flag} **{player['symbol']}** {returns_str}")
                    else:
                        st.caption(f"{flag} **{player['symbol']}**")
                    st.caption(f"└ {player.get('position_name', '')}")
                with col2:
                    if st.button("❌", key=f"remove_{idx}"):
                        st.session_state.players.pop(idx)
                        st.rerun()

    st.divider()

    # 도움말
    with st.expander("📖 사용 방법"):
        st.markdown("""
        **1단계:** 티커 심볼 입력 (예: AAPL)

        **2단계:** 포지션 선택

        **3단계:** "선수 추가" 클릭

        **4단계:** 최대 11명까지 추가

        **색상 의미:**
        - 🔴 빨강: 플러스 수익률 (높을수록 진함)
        - 🔵 파랑: 마이너스 수익률 (낮을수록 진함)
        - ⚪ 회색: 데이터 없음
        """)

    # 추천 티커
    with st.expander("💡 인기 종목"):
        st.caption("**테크:** AAPL, GOOGL, MSFT, TSLA, NVDA, META")
        st.caption("**금융:** JPM, BAC, V, MA, GS")
        st.caption("**소비재:** WMT, KO, PEP, MCD, NKE")
        st.caption("**헬스케어:** JNJ, PFE, UNH, ABBV")

# 메인 콘텐츠 - 축구장
st.markdown("---")

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    fig = create_soccer_field(st.session_state.players)
    st.plotly_chart(fig, use_container_width=True)

# 안내 메시지
if len(st.session_state.players) == 0:
    st.info("👈 왼쪽 사이드바에서 티커를 추가하여 라인업을 구성하세요!")
elif len(st.session_state.players) < 11:
    st.info(f"💡 {11 - len(st.session_state.players)}명의 선수를 더 추가할 수 있습니다!")
else:
    st.success("🎉 완벽한 라인업입니다! 11명의 선수가 모두 배치되었습니다!")

# 타임프레임 변경 시 수익률 업데이트
if 'last_timeframe' not in st.session_state:
    st.session_state.last_timeframe = timeframe

if st.session_state.last_timeframe != timeframe:
    with st.spinner('수익률 업데이트 중...'):
        for player in st.session_state.players:
            updated_info = get_ticker_info(player['symbol'], timeframe)
            if updated_info:
                player['returns'] = updated_info['returns']
        st.session_state.last_timeframe = timeframe
        st.rerun()

# 푸터
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: white;'>⚽ + 📈 = 💰 | "
    "Powered by yfinance & Streamlit</p>",
    unsafe_allow_html=True
)
