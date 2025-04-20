import React from 'react';
import '../style.css';

function Recommendation({ text }) {
  if (!text) return null;
  return <div className="recommendation-box">{text}</div>;
}

export default Recommendation;