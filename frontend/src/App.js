import React, { useEffect, useState } from 'react';
import CategorySelector from './components/CategorySelector';
import ProductList from './components/ProductList';
import Recommendation from './components/Reccomendation';
import './style.css';

function App() {
  const [categories, setCategories] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState('');
  const [products, setProducts] = useState([]);
  const [recommendation, setRecommendation] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    fetch('/api/categories')
      .then(res => res.json())
      .then(data => setCategories(data))
      .catch(() => setError('Failed to load categories'));
  }, []);

  const handleCategoryChange = (category) => {
    setSelectedCategory(category);
    setLoading(true);
    setError('');
    setProducts([]);
    setRecommendation('');
    fetch('/api/recommend', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ category })
    })
      .then(res => res.json())
      .then(data => {
        setProducts(data.top_products || []);
        setRecommendation(data.gpt_recommendation || '');
        setLoading(false);
      })
      .catch(() => {
        setError('Failed to fetch recommendations');
        setLoading(false);
      });
  };

  return (
    <div className="app-container">
      <header className="header">
        <h1>Beauty Bot</h1>
        <p className="subtitle">Personalized beauty recommendations, powered by AI</p>
      </header>
      <section className="hero">
        <div className="hero-title">Find Your Glow</div>
        <div className="hero-desc">Discover top-rated beauty products curated just for you. Select a category and let our AI do the rest.</div>
      </section>
      <main>
        <CategorySelector 
          categories={categories} 
          selected={selectedCategory} 
          onChange={handleCategoryChange} 
        />
        {loading && <div className="loader">Loading...</div>}
        {error && <div className="error">{error}</div>}
        {!loading && !error && products.length > 0 && (
          <>
            <ProductList products={products} />
            <Recommendation text={recommendation} />
          </>
        )}
      </main>
      <footer className="footer">
        <span>By Gayatri Kondabathini • &copy; {new Date().getFullYear()} Beauty Bot</span>
      </footer>
    </div>
  );
}

export default App;