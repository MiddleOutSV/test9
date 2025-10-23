import React, { useRef } from 'react';
import Draggable from 'react-draggable';
import './SoccerField.css';

const SoccerField = ({ players, onPlayerMove, onPlayerRemove }) => {
  const fieldRef = useRef(null);

  const handleDrag = (id, e, data) => {
    if (!fieldRef.current) return;

    const fieldRect = fieldRef.current.getBoundingClientRect();
    const x = ((data.x + 40) / fieldRect.width) * 100; // +40 to account for player circle radius
    const y = ((data.y + 40) / fieldRect.height) * 100;

    // Keep within bounds
    const boundedX = Math.max(5, Math.min(95, x));
    const boundedY = Math.max(5, Math.min(95, y));

    onPlayerMove(id, { x: boundedX, y: boundedY });
  };

  const getPositionInPixels = (position) => {
    if (!fieldRef.current) return { x: 0, y: 0 };

    const fieldRect = fieldRef.current.getBoundingClientRect();
    return {
      x: (position.x / 100) * fieldRect.width - 40, // -40 for circle radius
      y: (position.y / 100) * fieldRect.height - 40
    };
  };

  const getFlagEmoji = (countryCode) => {
    if (!countryCode) return '🇺🇸';

    // Convert country code to flag emoji
    const codePoints = countryCode
      .toUpperCase()
      .split('')
      .map(char => 127397 + char.charCodeAt());
    return String.fromCodePoint(...codePoints);
  };

  const getPerformanceClass = (returns) => {
    if (returns === null || returns === undefined) return 'neutral';
    if (returns > 10) return 'excellent';
    if (returns > 5) return 'good';
    if (returns > 0) return 'positive';
    if (returns > -5) return 'negative';
    return 'poor';
  };

  return (
    <div className="soccer-field-container">
      <div className="soccer-field" ref={fieldRef}>
        {/* Field markings */}
        <div className="field-markings">
          <div className="center-circle"></div>
          <div className="center-line"></div>
          <div className="penalty-box penalty-box-top"></div>
          <div className="penalty-box penalty-box-bottom"></div>
          <div className="goal-box goal-box-top"></div>
          <div className="goal-box goal-box-bottom"></div>
        </div>

        {/* Players */}
        {players.map((player) => {
          const pixelPosition = getPositionInPixels(player.position);
          const performanceClass = getPerformanceClass(player.returns);

          return (
            <Draggable
              key={player.id}
              position={pixelPosition}
              onStop={(e, data) => handleDrag(player.id, e, data)}
              bounds="parent"
            >
              <div className={`player ${performanceClass}`}>
                <button
                  className="remove-btn"
                  onClick={() => onPlayerRemove(player.id)}
                  title="Remove player"
                >
                  ×
                </button>
                <div className="flag">{getFlagEmoji(player.countryCode)}</div>
                <div className="player-info">
                  <div className="ticker">{player.symbol}</div>
                  <div className="company-name">{player.name}</div>
                  {player.returns !== null && player.returns !== undefined && (
                    <div className={`returns ${player.returns >= 0 ? 'positive' : 'negative'}`}>
                      {player.returns >= 0 ? '+' : ''}{player.returns}%
                    </div>
                  )}
                </div>
              </div>
            </Draggable>
          );
        })}
      </div>
    </div>
  );
};

export default SoccerField;
