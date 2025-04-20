import React from 'react';
import '../style.css';

function CategorySelector({ categories, selected, onChange }) {
  return (
    <div className="category-selector">
      {categories.map(category => (
        <button
          key={category}
          className={`category-pill${selected === category ? ' selected' : ''}`}
          onClick={() => onChange(category)}
        >
          {category}
        </button>
      ))}
    </div>
  );
}

export default CategorySelector;