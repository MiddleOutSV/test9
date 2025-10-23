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
