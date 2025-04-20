import requests
from bs4 import BeautifulSoup
import logging
import time
import random

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def scrape_sephora(category):
    """
    Scrape Sephora website for products in a given category.
    
    Args:
        category (str): Product category to scrape (e.g., 'makeup', 'lipstick', 'foundation')
        
    Returns:
        list: List of product dictionaries with name, price, rating, reviews, and url
    """
    # Format category for URL (replace spaces with hyphens, lowercase)
    formatted_category = category.lower().replace(' ', '-')
    base_url = "https://www.sephora.com/shop"
    url = f"{base_url}/{formatted_category}"
    
    # Rotate user agents to avoid detection
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"
    ]
    
    headers = {
        "User-Agent": random.choice(user_agents),
        "Accept-Language": "en-US,en;q=0.9",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
    }
    
    logging.info(f"Scraping products from category: {category}")
    logging.info(f"URL: {url}")
    
    try:
        # Add a small delay to be respectful to the server
        time.sleep(1.5)
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Raise exception for 4XX/5XX responses
        
        soup = BeautifulSoup(response.text, "html.parser")
        products = []
        
        # These selectors will need to be updated based on Sephora's current HTML structure
        # The current selectors are placeholders and will need to be adjusted
        product_containers = soup.select("div[data-comp='ProductGrid'] div[data-comp='ProductTile']")
        
        if not product_containers:
            logging.warning(f"No product containers found. Sephora may have changed their HTML structure or blocked the request.")
            return []
            
        logging.info(f"Found {len(product_containers)} product containers")
        
        for item in product_containers:
            try:
                # Extract product details
                name_element = item.select_one("span[data-at='sku_item_name']")
                price_element = item.select_one("span[data-at='price']")
                rating_element = item.select_one("div[data-comp='StarRating']")
                reviews_element = item.select_one("span[data-at='number_of_reviews']")
                url_element = item.select_one("a[data-comp='ProductTile-link']")
                
                # Skip if essential elements are missing
                if not (name_element and price_element):
                    continue
                    
                name = name_element.text.strip()
                # Clean price text and convert to float
                price_text = price_element.text.strip().replace('$', '').replace(',', '')
                price = float(price_text)
                
                # Handle optional elements
                rating = 0
                if rating_element:
                    aria_label = rating_element.get('aria-label', '')
                    if 'stars' in aria_label:
                        try:
                            rating = float(aria_label.split('stars')[0].strip())
                        except ValueError:
                            rating = 0
                
                reviews = 0
                if reviews_element:
                    reviews_text = reviews_element.text.strip().replace('(', '').replace(')', '').replace(',', '')
                    try:
                        reviews = int(reviews_text)
                    except ValueError:
                        reviews = 0
                
                product_url = ""
                if url_element and url_element.has_attr('href'):
                    product_url = "https://www.sephora.com" + url_element['href']
                
                # Add product to list
                products.append({
                    "name": name,
                    "price": price,
                    "rating": rating,
                    "reviews": reviews,
                    "url": product_url
                })
                
            except Exception as e:
                logging.error(f"Error extracting product details: {str(e)}")
                continue
        
        logging.info(f"Successfully scraped {len(products)} products")
        return products
        
    except requests.exceptions.RequestException as e:
        logging.error(f"Request failed: {str(e)}")
        return []
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        return []

def get_available_categories():
    """
    Returns a list of available makeup categories on Sephora.
    
    Returns:
        list: List of category names
    """
    return [
        "makeup", "foundation", "concealer", "face primer", 
        "powder", "blush", "bronzer", "highlighter", 
        "eyeshadow", "eyeliner", "mascara", "eyebrow", 
        "lipstick", "lip gloss", "lip liner"
    ]
