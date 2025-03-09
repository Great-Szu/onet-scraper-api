from flask import Flask, jsonify, Response
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

app = Flask(__name__)

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
    url = "https://wiadomosci.onet.pl/wroclaw"
    driver = create_driver()
    driver.get(url)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a.itemBox.itemBoxNormal')))

    articles = driver.find_elements(By.CSS_SELECTOR, 'a.itemBox.itemBoxNormal')
    article_list = [{'title': a.find_element(By.CSS_SELECTOR, '.title span').text, 'link': a.get_attribute('href')} for a in articles if a.find_element(By.CSS_SELECTOR, '.title span')]

    driver.quit()
    return article_list

@app.route('/news', methods=['GET'])
def get_news():
    """API endpoint to get scraped news articles."""
    # Return response with explicit encoding
    response = jsonify(scrape_news())
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)