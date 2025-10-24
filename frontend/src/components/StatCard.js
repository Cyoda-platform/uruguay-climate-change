import React from 'react';
import './StatCard.css';

const StatCard = ({ title, value, unit, trend, changeRate }) => {
  const getTrendIcon = () => {
    if (trend === 'increasing') return '📈';
    if (trend === 'decreasing') return '📉';
    return '➡️';
  };

  const getTrendColor = () => {
    if (trend === 'increasing') return '#e74c3c';
    if (trend === 'decreasing') return '#3498db';
    return '#95a5a6';
  };

  return (
    <div className="stat-card">
      <div className="stat-header">
        <h3 className="stat-title">{title}</h3>
        <span className="trend-icon">{getTrendIcon()}</span>
      </div>
      <div className="stat-value">
        {value} <span className="stat-unit">{unit}</span>
      </div>
      {trend && (
        <div className="stat-trend" style={{ color: getTrendColor() }}>
          <span className="trend-label">{trend}</span>
          {changeRate && (
            <span className="change-rate">
              {changeRate > 0 ? '+' : ''}{changeRate} {unit}/decade
            </span>
          )}
        </div>
      )}
    </div>
  );
};

export default StatCard;
