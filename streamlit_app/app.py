import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from datetime import datetime
from streamlit_plotly_events import plotly_events

# Page configuration
st.set_page_config(
    page_title="Stock Lineup Visualizer",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
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
    }
    .stAlert {
        background-color: rgba(255, 255, 255, 0.9);
    }
    </style>
    """, unsafe_allow_html=True)

# Exchange to country code mapping
EXCHANGE_TO_COUNTRY = {
    'NMS': 'US', 'NYQ': 'US', 'PCX': 'US', 'BTS': 'US',
    'NGM': 'US', 'NCM': 'US', 'ASE': 'US',
    'LSE': 'GB', 'TSE': 'JP', 'HKG': 'HK',
    'FRA': 'DE', 'EPA': 'FR', 'TOR': 'CA',
}

def get_flag_emoji(country_code):
    """Convert country code to flag emoji"""
    if not country_code:
        return '🇺🇸'
    codepoints = [127397 + ord(char) for char in country_code.upper()]
    return ''.join(chr(cp) for cp in codepoints)

def get_period_for_timeframe(timeframe):
    """Convert timeframe to yfinance period"""
    periods = {'1W': '1mo', '1M': '3mo', '6M': '1y', '1Y': '2y'}
    return periods.get(timeframe, '1y')

def calculate_returns(ticker_symbol, timeframe):
    """Calculate returns for the given timeframe"""
    try:
        ticker = yf.Ticker(ticker_symbol)
        period = get_period_for_timeframe(timeframe)
        hist = ticker.history(period=period)

        if hist.empty:
            return None

        days_map = {'1W': 7, '1M': 30, '6M': 180, '1Y': 365}
        days_back = min(days_map.get(timeframe, 365), len(hist) - 1)

        if days_back < 1:
            return None

        start_price = hist['Close'].iloc[-days_back]
        current_price = hist['Close'].iloc[-1]
        returns = ((current_price - start_price) / start_price) * 100
        return round(returns, 2)
    except Exception as e:
        st.error(f"Error calculating returns for {ticker_symbol}: {e}")
        return None

def get_ticker_info(symbol, timeframe):
    """Get ticker information"""
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
        st.error(f"Error fetching data for {symbol}: {e}")
        return None

def get_performance_color(returns):
    """Get color based on performance"""
    if returns is None:
        return '#A0AEC0'  # Gray
    if returns > 10:
        return '#22C55E'  # Green - Excellent
    if returns > 5:
        return '#84CC16'  # Light Green - Good
    if returns > 0:
        return '#3B82F6'  # Blue - Positive
    if returns > -5:
        return '#F59E0B'  # Orange - Negative
    return '#EF4444'  # Red - Poor

def create_soccer_field(players):
    """Create soccer field visualization with Plotly"""

    # Create figure
    fig = go.Figure()

    # Field dimensions
    field_length = 105
    field_width = 68

    # Add grass background with striped pattern
    for i in range(0, int(field_length), 10):
        color = '#2D5016' if (i // 10) % 2 == 0 else '#3A6B1E'
        fig.add_shape(
            type="rect",
            x0=i, y0=0, x1=i+10, y1=field_width,
            fillcolor=color,
            line=dict(width=0),
            layer="below"
        )

    # Field outline
    fig.add_shape(type="rect", x0=0, y0=0, x1=field_length, y1=field_width,
                  line=dict(color="white", width=3), fillcolor="rgba(0,0,0,0)")

    # Center line
    fig.add_shape(type="line", x0=field_length/2, y0=0, x1=field_length/2, y1=field_width,
                  line=dict(color="white", width=2))

    # Center circle
    fig.add_shape(type="circle", x0=field_length/2-9.15, y0=field_width/2-9.15,
                  x1=field_length/2+9.15, y1=field_width/2+9.15,
                  line=dict(color="white", width=2), fillcolor="rgba(0,0,0,0)")

    # Center spot
    fig.add_shape(type="circle", x0=field_length/2-0.5, y0=field_width/2-0.5,
                  x1=field_length/2+0.5, y1=field_width/2+0.5,
                  fillcolor="white", line=dict(color="white", width=0))

    # Penalty boxes
    for x in [0, field_length]:
        direction = 1 if x == 0 else -1
        # Large penalty box
        fig.add_shape(type="rect",
                     x0=x, y0=field_width/2-20.16,
                     x1=x+direction*16.5, y1=field_width/2+20.16,
                     line=dict(color="white", width=2), fillcolor="rgba(0,0,0,0)")
        # Small penalty box (goal box)
        fig.add_shape(type="rect",
                     x0=x, y0=field_width/2-9.16,
                     x1=x+direction*5.5, y1=field_width/2+9.16,
                     line=dict(color="white", width=2), fillcolor="rgba(0,0,0,0)")
        # Penalty spot
        spot_x = 11 if x == 0 else field_length - 11
        fig.add_shape(type="circle",
                     x0=spot_x-0.5, y0=field_width/2-0.5,
                     x1=spot_x+0.5, y1=field_width/2+0.5,
                     fillcolor="white", line=dict(color="white", width=0))

    # Add players
    if players:
        x_coords = [p['x'] for p in players]
        y_coords = [p['y'] for p in players]
        colors = [get_performance_color(p.get('returns')) for p in players]

        # Create hover text
        hover_texts = []
        for p in players:
            flag = get_flag_emoji(p.get('countryCode', 'US'))
            returns_str = f"+{p['returns']}%" if p.get('returns', 0) >= 0 else f"{p['returns']}%"
            text = f"{flag} <b>{p['symbol']}</b><br>{p['name']}<br><b>{returns_str}</b>"
            hover_texts.append(text)

        # Add player markers
        fig.add_trace(go.Scatter(
            x=x_coords,
            y=y_coords,
            mode='markers+text',
            marker=dict(
                size=30,
                color=colors,
                line=dict(color='white', width=3),
                symbol='circle'
            ),
            text=[p['symbol'] for p in players],
            textposition="middle center",
            textfont=dict(color='white', size=10, family='Arial Black'),
            hovertext=hover_texts,
            hoverinfo='text',
            showlegend=False
        ))

    # Update layout
    fig.update_layout(
        width=1000,
        height=650,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(
            range=[-2, field_length+2],
            showgrid=False,
            zeroline=False,
            showticklabels=False,
        ),
        yaxis=dict(
            range=[-2, field_width+2],
            showgrid=False,
            zeroline=False,
            showticklabels=False,
            scaleanchor="x",
            scaleratio=1,
        ),
        margin=dict(l=20, r=20, t=20, b=20),
        hovermode='closest',
        dragmode='pan'
    )

    return fig

# Initialize session state
if 'players' not in st.session_state:
    st.session_state.players = []
if 'selected_ticker' not in st.session_state:
    st.session_state.selected_ticker = None
if 'waiting_for_click' not in st.session_state:
    st.session_state.waiting_for_click = False

# Main title
st.markdown("<h1>⚽ Stock Lineup Visualizer (Streamlit Edition)</h1>", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("📊 Controls")

    # Timeframe selector
    timeframe = st.selectbox(
        "Select Timeframe",
        options=['1W', '1M', '6M', '1Y'],
        index=1,
        format_func=lambda x: {'1W': '1 Week', '1M': '1 Month', '6M': '6 Months', '1Y': '1 Year'}[x]
    )

    st.divider()

    # Ticker input
    st.subheader("Add Ticker")
    ticker_input = st.text_input("Enter ticker symbol", placeholder="e.g., AAPL", key="ticker_input").upper()

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🎯 Select Position", use_container_width=True,
                    disabled=len(st.session_state.players) >= 11 or not ticker_input):
            # Fetch ticker data
            ticker_data = get_ticker_info(ticker_input, timeframe)
            if ticker_data:
                st.session_state.selected_ticker = ticker_data
                st.session_state.waiting_for_click = True
                st.info("👆 Click on the field to place the ticker!")
            else:
                st.error("Failed to fetch ticker data")

    with col2:
        if st.button("🗑️ Clear All", use_container_width=True):
            st.session_state.players = []
            st.session_state.selected_ticker = None
            st.session_state.waiting_for_click = False
            st.rerun()

    # Show current status
    if st.session_state.waiting_for_click and st.session_state.selected_ticker:
        st.success(f"✅ Ready to place: **{st.session_state.selected_ticker['symbol']}**")
        st.caption("Click anywhere on the field to place this ticker")

    st.divider()

    # Player count
    st.metric("Players on Field", f"{len(st.session_state.players)}/11")

    # Current lineup
    if st.session_state.players:
        st.subheader("Current Lineup")
        for idx, player in enumerate(st.session_state.players):
            col1, col2 = st.columns([4, 1])
            with col1:
                flag = get_flag_emoji(player.get('countryCode', 'US'))
                returns = player.get('returns', 0)
                returns_str = f"+{returns}%" if returns >= 0 else f"{returns}%"
                st.caption(f"{flag} **{player['symbol']}** {returns_str}")
            with col2:
                if st.button("❌", key=f"remove_{idx}"):
                    st.session_state.players.pop(idx)
                    st.rerun()

    st.divider()

    # Instructions
    with st.expander("📖 How to Use"):
        st.markdown("""
        1. Enter a ticker symbol (e.g., AAPL)
        2. Click "Select Position"
        3. Click on the field where you want to place it
        4. Repeat for up to 11 tickers
        5. Change timeframe to update all returns

        **Color Legend:**
        - 🟢 Green: >10% returns
        - 🟡 Yellow: 5-10% returns
        - 🔵 Blue: 0-5% returns
        - 🟠 Orange: -5-0% returns
        - 🔴 Red: <-5% returns
        """)

    # Popular tickers
    with st.expander("💡 Popular Tickers"):
        st.caption("**Tech:** AAPL, GOOGL, MSFT, TSLA, NVDA")
        st.caption("**Finance:** JPM, BAC, V, MA")
        st.caption("**Consumer:** WMT, KO, PEP, MCD")

# Main content - Soccer field
st.markdown("---")

# Create and display soccer field
fig = create_soccer_field(st.session_state.players)

# Use plotly_events to capture clicks
selected_points = plotly_events(
    fig,
    click_event=True,
    hover_event=False,
    select_event=False,
    override_height=650,
    override_width=1000
)

# Handle click events
if selected_points and st.session_state.waiting_for_click and st.session_state.selected_ticker:
    # Get click coordinates
    click_x = selected_points[0]['x']
    click_y = selected_points[0]['y']

    # Add player at clicked position
    new_player = {
        **st.session_state.selected_ticker,
        'x': click_x,
        'y': click_y
    }

    st.session_state.players.append(new_player)
    st.session_state.selected_ticker = None
    st.session_state.waiting_for_click = False
    st.rerun()

# Update returns when timeframe changes
if 'last_timeframe' not in st.session_state:
    st.session_state.last_timeframe = timeframe

if st.session_state.last_timeframe != timeframe:
    # Update all players' returns
    for player in st.session_state.players:
        updated_info = get_ticker_info(player['symbol'], timeframe)
        if updated_info:
            player['returns'] = updated_info['returns']
    st.session_state.last_timeframe = timeframe
    st.rerun()

# Footer
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: white;'>Built with ⚽ and 📈 | "
    "Powered by yfinance & Streamlit</p>",
    unsafe_allow_html=True
)
