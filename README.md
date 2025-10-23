# Stock Lineup Visualizer

Build your stock portfolio like a soccer team! This web application allows you to visualize your favorite stock tickers as players on a soccer field, complete with performance metrics similar to FotMob's lineup builder.

## Features

- **Soccer Field Layout**: Arrange up to 11 stock tickers on a beautiful soccer field background
- **Drag & Drop**: Freely position each ticker anywhere on the field
- **Real-time Stock Data**: Fetches company names and returns using Yahoo Finance API (yfinance)
- **Performance Visualization**: Color-coded circles show stock performance at a glance
- **Multiple Timeframes**: View returns over 1 Week, 1 Month, 6 Months, or 1 Year
- **Exchange Flags**: Each ticker displays the flag of its stock exchange
- **Responsive Design**: Works on desktop and mobile devices

## Tech Stack

### Backend
- **Flask**: Python web framework
- **yfinance**: Yahoo Finance API for stock data
- **Flask-CORS**: Enable cross-origin requests

### Frontend
- **React**: UI framework
- **react-draggable**: Drag and drop functionality
- **Axios**: HTTP client for API requests

## Installation & Setup

### Prerequisites
- Python 3.8+
- Node.js 14+
- npm or yarn

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the Flask server:
```bash
python app.py
```

The backend server will start at `http://localhost:5000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm start
```

The app will open at `http://localhost:3000`

## Deployment (웹에서 실행하기)

### 추천 방법: Railway + Vercel (완전 무료)

이 방법이 가장 쉽고 빠릅니다!

#### 1. Backend 배포 (Railway)

1. [Railway](https://railway.app/) 가입 (GitHub 계정으로 로그인)
2. "New Project" 클릭
3. "Deploy from GitHub repo" 선택
4. 이 저장소 선택
5. "Add variables" 클릭하여 환경 변수 추가:
   - `PORT`: 자동 설정됨 (건드릴 필요 없음)
6. Root directory를 `backend`로 설정
7. 배포 완료되면 URL을 복사 (예: `https://your-app.railway.app`)

#### 2. Frontend 배포 (Vercel)

1. [Vercel](https://vercel.com/) 가입 (GitHub 계정으로 로그인)
2. "New Project" 클릭
3. 이 저장소 선택
4. "Root Directory"를 `frontend`로 설정
5. Environment Variables 추가:
   - Name: `REACT_APP_API_URL`
   - Value: Railway에서 받은 백엔드 URL (예: `https://your-app.railway.app`)
6. "Deploy" 클릭
7. 배포 완료! Vercel이 제공하는 URL로 접속하면 됩니다

### 대안 방법 1: Render (Backend + Frontend 모두)

#### Backend 배포
1. [Render](https://render.com/) 가입
2. "New Web Service" 클릭
3. GitHub 저장소 연결
4. 설정:
   - **Name**: stock-lineup-backend
   - **Root Directory**: `backend`
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python app.py`
   - **Plan**: Free
5. 배포 후 URL 복사

#### Frontend 배포
1. Render에서 "New Static Site" 클릭
2. 설정:
   - **Name**: stock-lineup-frontend
   - **Root Directory**: `frontend`
   - **Build Command**: `npm install && npm run build`
   - **Publish Directory**: `build`
3. Environment Variables:
   - `REACT_APP_API_URL`: 백엔드 URL
4. Deploy

### 대안 방법 2: Netlify (Frontend만)

1. [Netlify](https://netlify.com/) 가입
2. "New site from Git" 클릭
3. 저장소 연결
4. Build settings:
   - **Base directory**: `frontend`
   - **Build command**: `npm run build`
   - **Publish directory**: `frontend/build`
5. Environment variables:
   - `REACT_APP_API_URL`: 백엔드 URL
6. Deploy

### 배포 체크리스트

- [ ] Backend가 정상 작동하는지 확인 (`/api/health` 엔드포인트 테스트)
- [ ] Frontend의 환경 변수에 올바른 Backend URL 설정
- [ ] CORS가 활성화되어 있는지 확인 (이미 설정되어 있음)
- [ ] 무료 플랜의 경우 일정 시간 후 sleep 모드로 전환될 수 있음 (첫 요청 시 약간 느릴 수 있음)

### 배포 후 테스트

배포된 웹사이트에서:
1. 티커 입력 (예: AAPL)
2. 데이터가 정상적으로 로드되는지 확인
3. 드래그 앤 드롭이 작동하는지 확인

문제가 있다면 브라우저 개발자 도구(F12)의 Console 탭에서 에러 확인!

## Usage

1. **Add Tickers**: Enter a stock ticker symbol (e.g., AAPL, GOOGL, MSFT) and click "Add Ticker"
2. **Select Timeframe**: Choose your preferred timeframe (1W, 1M, 6M, 1Y) from the top-right corner
3. **Drag Players**: Click and drag any ticker to position it on the field
4. **View Performance**:
   - Green = Excellent performance (>10%)
   - Light green = Good performance (5-10%)
   - Blue = Positive performance (0-5%)
   - Orange = Negative performance (-5-0%)
   - Red = Poor performance (<-5%)
5. **Remove Players**: Hover over a ticker and click the × button to remove it

## Popular Tickers to Try

- **Tech**: AAPL, GOOGL, MSFT, TSLA, NVDA, META, AMZN
- **Finance**: JPM, BAC, GS, V, MA
- **Consumer**: WMT, KO, PEP, MCD, NKE
- **Healthcare**: JNJ, PFE, UNH, ABBV

## API Endpoints

### GET /api/ticker/<symbol>
Fetch stock information for a ticker symbol.

**Parameters:**
- `timeframe` (optional): 1W, 1M, 6M, or 1Y (default: 1M)

**Response:**
```json
{
  "symbol": "AAPL",
  "name": "Apple Inc.",
  "exchange": "NMS",
  "countryCode": "US",
  "returns": 12.5,
  "timeframe": "1M"
}
```

### GET /api/health
Health check endpoint.

## Project Structure

```
stock-lineup-visualizer/
├── backend/
│   ├── app.py              # Flask application
│   └── requirements.txt    # Python dependencies
├── frontend/
│   ├── public/
│   │   └── index.html      # HTML template
│   ├── src/
│   │   ├── App.js          # Main application component
│   │   ├── App.css         # Main styles
│   │   ├── SoccerField.js  # Soccer field component
│   │   ├── SoccerField.css # Field styles
│   │   ├── index.js        # React entry point
│   │   └── index.css       # Global styles
│   ├── package.json        # NPM dependencies
│   └── .env               # Environment variables
├── .gitignore
└── README.md
```

## Performance Color Coding

| Returns | Color | Performance |
|---------|-------|-------------|
| > 10% | Green | Excellent |
| 5-10% | Light Green | Good |
| 0-5% | Blue | Positive |
| -5-0% | Orange | Negative |
| < -5% | Red | Poor |

## Troubleshooting

### Backend Issues

**Port already in use:**
```bash
# Change port in backend/app.py
app.run(debug=True, port=5001)  # Use different port
```

**yfinance data not loading:**
- Check your internet connection
- Some tickers may have limited historical data
- Try a different ticker symbol

### Frontend Issues

**CORS errors:**
- Ensure Flask-CORS is installed in the backend
- Check that the API_URL in `.env` matches your backend URL

**Cannot connect to backend:**
- Verify the backend is running on port 5000
- Check the `REACT_APP_API_URL` in `frontend/.env`

## Future Enhancements

- Save and load lineups
- Share lineups with others
- Add more formation presets (4-4-2, 4-3-3, etc.)
- Export lineup as image
- Compare multiple lineups
- Add sector/industry information
- Historical lineup performance tracking

## License

MIT License - feel free to use this project for personal or commercial purposes.

## Credits

Inspired by FotMob's lineup builder feature.

---

Built with ⚽ and 📈
