import React, { useState, useEffect } from 'react';
import SoccerField from './SoccerField';
import axios from 'axios';
import './App.css';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

function App() {
  const [players, setPlayers] = useState([]);
  const [timeframe, setTimeframe] = useState('1M');
  const [tickerInput, setTickerInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const timeframes = [
    { value: '1W', label: '1 Week' },
    { value: '1M', label: '1 Month' },
    { value: '6M', label: '6 Months' },
    { value: '1Y', label: '1 Year' }
  ];

  // Update returns when timeframe changes
  useEffect(() => {
    if (players.length > 0) {
      updateAllReturns();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [timeframe]);

  const updateAllReturns = async () => {
    const updatedPlayers = await Promise.all(
      players.map(async (player) => {
        try {
          const response = await axios.get(
            `${API_URL}/api/ticker/${player.symbol}?timeframe=${timeframe}`
          );
          return {
            ...player,
            returns: response.data.returns,
            timeframe: timeframe
          };
        } catch (err) {
          return player;
        }
      })
    );
    setPlayers(updatedPlayers);
  };

  const addTicker = async (e) => {
    e.preventDefault();

    if (players.length >= 11) {
      setError('Maximum 11 tickers allowed (like a soccer team!)');
      return;
    }

    if (!tickerInput.trim()) {
      setError('Please enter a ticker symbol');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const response = await axios.get(
        `${API_URL}/api/ticker/${tickerInput.toUpperCase()}?timeframe=${timeframe}`
      );

      const newPlayer = {
        id: Date.now(),
        symbol: response.data.symbol,
        name: response.data.name,
        countryCode: response.data.countryCode,
        returns: response.data.returns,
        // Default position in the center area
        position: {
          x: 50 + (Math.random() - 0.5) * 20,
          y: 50 + (Math.random() - 0.5) * 20
        }
      };

      setPlayers([...players, newPlayer]);
      setTickerInput('');
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to fetch ticker data');
    } finally {
      setLoading(false);
    }
  };

  const removePlayer = (id) => {
    setPlayers(players.filter(p => p.id !== id));
  };

  const updatePlayerPosition = (id, position) => {
    setPlayers(players.map(p =>
      p.id === id ? { ...p, position } : p
    ));
  };

  const clearAll = () => {
    if (window.confirm('Clear all tickers?')) {
      setPlayers([]);
    }
  };

  return (
    <div className="App">
      <header className="app-header">
        <div className="header-content">
          <h1>⚽ Stock Lineup Visualizer</h1>
          <div className="timeframe-selector">
            {timeframes.map(tf => (
              <button
                key={tf.value}
                className={`timeframe-btn ${timeframe === tf.value ? 'active' : ''}`}
                onClick={() => setTimeframe(tf.value)}
              >
                {tf.label}
              </button>
            ))}
          </div>
        </div>
      </header>

      <div className="controls">
        <form onSubmit={addTicker} className="ticker-form">
          <input
            type="text"
            value={tickerInput}
            onChange={(e) => setTickerInput(e.target.value.toUpperCase())}
            placeholder="Enter ticker symbol (e.g., AAPL)"
            className="ticker-input"
            disabled={loading}
          />
          <button type="submit" className="add-btn" disabled={loading || players.length >= 11}>
            {loading ? 'Loading...' : 'Add Ticker'}
          </button>
          {players.length > 0 && (
            <button type="button" onClick={clearAll} className="clear-btn">
              Clear All
            </button>
          )}
        </form>
        {error && <div className="error-message">{error}</div>}
        <div className="player-count">
          Players: {players.length}/11
        </div>
      </div>

      <SoccerField
        players={players}
        onPlayerMove={updatePlayerPosition}
        onPlayerRemove={removePlayer}
      />

      {players.length === 0 && (
        <div className="empty-state">
          <p>Add stock tickers to build your lineup!</p>
          <p className="empty-hint">Try popular tickers like AAPL, GOOGL, MSFT, TSLA, AMZN</p>
        </div>
      )}
    </div>
  );
}

export default App;
