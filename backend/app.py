from dotenv import load_dotenv
load_dotenv()

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import logging
from scraper import scrape_sephora, get_available_categories
from reccomender import get_best_products

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route("/api/recommend", methods=["POST"])
def recommend():
    """
    Endpoint to get product recommendations for a specific category.
    
    Expected JSON payload: {"category": "category_name"}
    Returns: JSON with top products and GPT recommendation
    """
    try:
        data = request.get_json()
        
        if not data or "category" not in data:
            return jsonify({"error": "Missing category parameter"}), 400
            
        category = data["category"]
        logging.info("Received recommendation request for category: {}".format(category))
        
        # Scrape products
        products = scrape_sephora(category)
        
        if not products:
            return jsonify({
                "top_products": [],
                "gpt_recommendation": "No products found for {}. Please try a different category.".format(category)
            })
        
        # Get recommendations
        recommendations = get_best_products(products, category)
        return jsonify(recommendations)
        
    except Exception as e:
        logging.error("Error processing recommendation request: {}".format(str(e)))
        return jsonify({"error": "An error occurred processing your request"}), 500

@app.route("/api/categories", methods=["GET"])
def categories():
    """
    Endpoint to get available makeup categories.
    
    Returns: JSON list of available categories
    """
    try:
        return jsonify(get_available_categories())
    except Exception as e:
        logging.error("Error fetching categories: {}".format(str(e)))
        return jsonify({"error": "An error occurred fetching categories"}), 500

@app.route("/api/health", methods=["GET"])
def health_check():
    """
    Health check endpoint.
    
    Returns: JSON with status
    """
    return jsonify({"status": "ok"})

@app.route("/", methods=["GET"])
def index():
    """
    Root endpoint.
    
    Returns: Simple welcome message
    """
    return jsonify({
        "message": "Welcome to the Beauty Bot API",
        "endpoints": {
            "/api/categories": "GET - List available makeup categories",
            "/api/recommend": "POST - Get product recommendations for a category"
        }
    })

if __name__ == "__main__":
    # Check if OpenAI API key is set
    if not os.getenv("OPENAI_API_KEY"):
        logging.warning("OPENAI_API_KEY environment variable is not set. Recommendations will not work.")
    
    # Run the Flask app
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
