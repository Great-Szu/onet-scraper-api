from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode (no browser window)
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

service = Service("C:/Users/panmi/Documents/OperdaDriver/chromedriver-win64/chromedriver-win64/chromedriver.exe")  # Update this path to your ChromeDriver

# Use Chrome with the updated path
driver = webdriver.Chrome(service=service, options=chrome_options)

def scrape_with_selenium(url):
    """Scrape the fully rendered page using Selenium."""
    driver.get(url)

    # Wait for the images to load (adjust the selector as needed)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a.itemBoxBig picture img')))

    html = driver.page_source
    return html

if __name__ == "__main__":
    source = scrape_with_selenium("https://wiadomosci.onet.pl/wroclaw")

    with open("source_selenium.html", "w", encoding="utf-8") as f:
        f.write(source)

    print("HTML saved from Selenium to source_selenium.html. Check if images are there.")
    driver.quit()  # Close the browser