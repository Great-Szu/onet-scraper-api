from flask import Flask, jsonify
from flask_cors import CORS
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import threading
import time

app = Flask(__name__)
CORS(app)  # Allow all origins (for testing)

# Global variable to store last scraped data
cached_news = []
last_updated = None  # Stores the last update timestamp

def create_driver():
    """Create a WebDriver instance with headless Chromium."""
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def scrape_news():
    """Scrape news articles and return as a list of dictionaries."""
    global cached_news, last_updated
    try:
        url = "https://wiadomosci.onet.pl/wroclaw"
        driver = create_driver()
        driver.get(url)

        # Wait for the normal article boxes
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a.itemBox.itemBoxNormal')))

        # Scrape the larger article first
        try:
            big_article = driver.find_element(By.CSS_SELECTOR, 'a.itemBox.itemBoxBig.itemBoxLast')
            big_article_data = {
                'title': big_article.find_element(By.CSS_SELECTOR, '.title span').text,
                'link': big_article.get_attribute('href')
            }
        except Exception:
            big_article_data = None  # If the big article is missing, continue

        # Scrape the normal articles
        articles = driver.find_elements(By.CSS_SELECTOR, 'a.itemBox.itemBoxNormal')
        article_list = [
            {'title': a.find_element(By.CSS_SELECTOR, '.title span').text, 'link': a.get_attribute('href')}
            for a in articles if a.find_element(By.CSS_SELECTOR, '.title span')
        ]

        # Add the big article at the beginning of the list
        if big_article_data:
            article_list.insert(0, big_article_data)

        driver.quit()

        # Store the scraped data in memory
        cached_news = article_list
        last_updated = time.strftime('%Y-%m-%d %H:%M:%S')  # Save timestamp

    except Exception as e:
        print(f"Scraping error: {e}")

def update_news_periodically():
    """Runs in the background and updates news every 10 minutes."""
    while True:
        scrape_news()
        print(f"News updated at {last_updated}")
        time.sleep(300)  # Update every 5 minutes

@app.route('/news', methods=['GET'])
def get_news():
    """API endpoint to get cached news articles."""
    if cached_news:
        return jsonify({"last_updated": last_updated, "articles": cached_news})
    else:
        return jsonify({"error": "No news data available"}), 503  # 503 = Service Unavailable

if __name__ == '__main__':
    # Start the background thread to update news
    threading.Thread(target=update_news_periodically, daemon=True).start()

    # Run Flask app
    app.run(host='0.0.0.0', port=5000, debug=True)