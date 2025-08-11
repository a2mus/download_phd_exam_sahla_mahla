from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

url = 'https://lmd.sahla-dz.com/2sujets-des-concours-dacces-au-doctorat-en-informatique-option-ia-intelligence-artificielle/'

print(f"Testing Selenium with: {url}")
print("=" * 50)

try:
    # Setup Chrome options
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')
    
    # Initialize driver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    print("Loading page...")
    driver.get(url)
    
    # Wait a bit for initial load
    time.sleep(3)
    
    print("Scrolling to trigger lazy loading...")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    driver.execute_script("window.scrollTo(0, 0);")
    time.sleep(2)
    
    print("Looking for iframes...")
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "iframe"))
        )
        print("Iframes found!")
    except:
        print("No iframes found within timeout")
    
    # Get page source and parse
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    
    print("\n=== IFRAMES AFTER SELENIUM ===")
    iframes = soup.find_all('iframe')
    print(f"Found {len(iframes)} iframes")
    
    pdf_urls = []
    for i, iframe in enumerate(iframes):
        src = iframe.get('src', '')
        data_src = iframe.get('data-src', '')
        print(f"Iframe {i+1}:")
        print(f"  src: {src}")
        print(f"  data-src: {data_src}")
        
        # Check for Google Docs viewer
        for url_attr in [src, data_src]:
            if url_attr and 'docs.google.com/viewer' in url_attr:
                print(f"  -> Found Google Docs viewer: {url_attr}")
                if 'srcid=' in url_attr:
                    file_id = url_attr.split('srcid=')[1].split('&')[0]
                    download_url = f"https://drive.google.com/uc?export=download&id={file_id}"
                    pdf_urls.append(download_url)
                    print(f"  -> Extracted download URL: {download_url}")
    
    print(f"\nTotal PDF URLs found: {len(pdf_urls)}")
    for url in pdf_urls:
        print(f"  - {url}")
        
except Exception as e:
    print(f"Error: {e}")
finally:
    if 'driver' in locals():
        driver.quit()
        print("\nSelenium driver closed")