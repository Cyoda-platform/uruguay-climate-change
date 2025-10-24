import React, { useState } from 'react';
import './InfoCard.css';

const InfoCard = ({ icon, title, description, details, severity = 'info' }) => {
  const [isExpanded, setIsExpanded] = useState(false);

  return (
    <div className={`info-card ${severity} ${isExpanded ? 'expanded' : ''}`}>
      <div className="info-card-header" onClick={() => setIsExpanded(!isExpanded)}>
        <div className="info-card-icon">{icon}</div>
        <div className="info-card-title-section">
          <h3 className="info-card-title">{title}</h3>
          <p className="info-card-description">{description}</p>
        </div>
        <div className={`expand-icon ${isExpanded ? 'rotated' : ''}`}>
          {isExpanded ? '▼' : '▶'}
        </div>
      </div>
      
      {isExpanded && (
        <div className="info-card-details">
          {details}
        </div>
      )}
    </div>
  );
};

export default InfoCard;

