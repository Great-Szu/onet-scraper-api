from flask import Flask, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


app = Flask(__name__)

def create_driver():
    """Create a WebDriver instance with headless Chromium."""
    options = Options()
    options.add_argument('--headless')  # Run in headless mode
    options.add_argument('--no-sandbox')  # Avoid some potential errors in headless mode
    options.add_argument('--disable-dev-shm-usage')  # Solve issues with memory on Docker/Cloud environments
    options.add_argument('--disable-gpu')  # Disable GPU hardware acceleration for headless mode

    # Use the Chromium binary location if necessary
    options.binary_location = "/usr/bin/chromium-browser"  # This is common in cloud environments

    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def scrape_news():
    """Scrape news articles and return as a list of dictionaries."""
    url = "https://wiadomosci.onet.pl/wroclaw"
    driver = create_driver()
    driver.get(url)

    # Wait for articles to load
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a.itemBox.itemBoxNormal')))

    articles = driver.find_elements(By.CSS_SELECTOR, 'a.itemBox.itemBoxNormal')

    article_list = []
    for article in articles:
        title_elem = article.find_element(By.CSS_SELECTOR, '.title span')
        if title_elem:
            article_list.append({
                'title': title_elem.text,
                'link': article.get_attribute('href')
            })

    driver.quit()
    return article_list

@app.route('/news', methods=['GET'])
def get_news():
    """API endpoint to get scraped news articles."""
    return jsonify(scrape_news())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)