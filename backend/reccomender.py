import os
import math
import logging
from openai import OpenAI

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def score(product):
    """
    Calculate a value score for a product based on rating, reviews, and price.
    
    Args:
        product (dict): Product dictionary with rating, reviews, and price
        
    Returns:
        float: Value score
    """
    # Avoid division by zero
    if product["price"] <= 0:
        return 0
        
    # Use log scale for reviews to prevent products with many reviews from dominating
    # Higher rating, more reviews, and lower price result in a higher score
    return (product["rating"] * math.log(product["reviews"] + 1)) / product["price"]

def get_best_products(products, category):
    """
    Get the best value products from a list of products using OpenAI's recommendation.
    
    Args:
        products (list): List of product dictionaries
        category (str): Product category
        
    Returns:
        dict: Dictionary with top products and GPT recommendation
    """
    if not products:
        logging.warning(f"No products found for category: {category}")
        return {
            "top_products": [],
            "gpt_recommendation": f"No products found for {category}. Please try a different category."
        }
    
    # Sort products by value score
    top_products = sorted(products, key=score, reverse=True)[:10]
    
    logging.info(f"Found {len(top_products)} top products for category: {category}")
    
    # Create a detailed prompt for OpenAI
    prompt = f"These are the top-rated {category} products from Sephora based on price, reviews, and rating:\n\n"
    
    for i, p in enumerate(top_products, 1):
        value_score = score(p)
        prompt += f"{i}. {p['name']}\n"
        prompt += f"   Price: ${p['price']:.2f}, Rating: {p['rating']}/5, Reviews: {p['reviews']}\n"
        prompt += f"   Value Score: {value_score:.2f}\n"
        if p.get('url'):
            prompt += f"   URL: {p['url']}\n"
        prompt += "\n"
    
    prompt += f"\nBased on the above data, which 3-5 {category} products provide the best value for money? "
    prompt += "Consider the balance between price, rating, and number of reviews. "
    prompt += "Explain why each product is a good value, and provide a brief summary of what makes these products stand out. "
    prompt += "Format your response with clear headings and bullet points for each product's pros and cons."
    
    try:
        # Call OpenAI API
        response = client.chat.completions.create(
            model="gpt-4",  # Use GPT-4 for better analysis
            messages=[
                {"role": "system", "content": "You are a beauty expert specializing in makeup product analysis. You help users find the best value makeup products based on price, ratings, and reviews."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        
        recommendation = response.choices[0].message.content
        logging.info("Successfully generated recommendation from OpenAI")
        
        return {
            "top_products": top_products,
            "gpt_recommendation": recommendation
        }
        
    except Exception as e:
        logging.error(f"Error calling OpenAI API: {str(e)}")
        return {
            "top_products": top_products,
            "gpt_recommendation": "Sorry, there was an error generating recommendations. Please try again later."
        }
