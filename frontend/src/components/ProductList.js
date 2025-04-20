import React from 'react';
import '../style.css';

function ProductList({ products }) {
  return (
    <div className="product-list">
      {products.map((product, idx) => (
        <div className="product-card" key={idx}>
          <div className="product-title">{product.name}</div>
          <div className="product-brand">{product.brand}</div>
          <div className="product-meta">
            ${product.price} • {product.rating}★ • {product.reviews} reviews
          </div>
          {product.description && <div className="product-description">{product.description}</div>}
        </div>
      ))}
    </div>
  );
}

export default ProductList;