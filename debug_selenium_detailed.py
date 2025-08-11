from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import re

url = 'https://lmd.sahla-dz.com/2sujets-des-concours-dacces-au-doctorat-en-informatique-option-ia-intelligence-artificielle/'

print(f"Debugging Selenium extraction with: {url}")
print("=" * 60)

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
    
    print("\n=== STEP 1: All iframes ===")
    all_iframes = soup.find_all('iframe')
    print(f"Total iframes found: {len(all_iframes)}")
    
    for i, iframe in enumerate(all_iframes):
        src = iframe.get('src', '')
        data_src = iframe.get('data-src', '')
        print(f"Iframe {i+1}:")
        print(f"  src: {src}")
        print(f"  data-src: {data_src}")
    
    print("\n=== STEP 2: Filtering for Google Docs iframes ===")
    
    # Method 1: Check src attribute
    iframes_src = soup.find_all('iframe', src=lambda s: s and ('docs.google.com/gview' in s or 'docs.google.com/viewer' in s or 'drive.google.com' in s))
    print(f"Iframes with matching src: {len(iframes_src)}")
    
    # Method 2: Check data-src attribute
    iframes_data_src = soup.find_all('iframe', attrs={'data-src': lambda s: s and ('docs.google.com/gview' in s or 'docs.google.com/viewer' in s or 'drive.google.com' in s)})
    print(f"Iframes with matching data-src: {len(iframes_data_src)}")
    
    # Combine both
    target_iframes = iframes_src + iframes_data_src
    print(f"Total target iframes: {len(target_iframes)}")
    
    print("\n=== STEP 3: Processing target iframes ===")
    result = {'type': None, 'urls': []}
    
    for i, iframe in enumerate(target_iframes):
        iframe_src = iframe.get('src') or iframe.get('data-src')
        print(f"\nProcessing iframe {i+1}: {iframe_src}")
        
        # Handle gview links
        url_param = re.search(r'url=([^&]+)', iframe_src)
        if url_param:
            import urllib.parse
            pdf_url = urllib.parse.unquote(url_param.group(1))
            print(f"  -> Found gview URL: {pdf_url}")
            if pdf_url not in result['urls']:
                result['type'] = 'pdf'
                result['urls'].append(pdf_url)
            continue

        # Handle Google Docs viewer with srcid parameter
        if 'docs.google.com/viewer' in iframe_src and 'srcid=' in iframe_src:
            file_id = iframe_src.split('srcid=')[1].split('&')[0]
            pdf_url = f'https://drive.google.com/uc?export=download&id={file_id}'
            print(f"  -> Found srcid, extracted file_id: {file_id}")
            print(f"  -> Generated download URL: {pdf_url}")
            if pdf_url not in result['urls']:
                result['type'] = 'pdf'
                result['urls'].append(pdf_url)
            continue

        # Handle drive.google.com links
        drive_match = re.search(r'drive\.google\.com/file/d/([a-zA-Z0-9_-]+)', iframe_src)
        if drive_match:
            file_id = drive_match.group(1)
            pdf_url = f'https://drive.google.com/uc?export=download&id={file_id}'
            print(f"  -> Found drive.google.com, file_id: {file_id}")
            print(f"  -> Generated download URL: {pdf_url}")
            if pdf_url not in result['urls']:
                result['type'] = 'pdf'
                result['urls'].append(pdf_url)
    
    print(f"\n=== FINAL RESULT ===")
    print(f"Type: {result['type']}")
    print(f"URLs found: {len(result['urls'])}")
    for url in result['urls']:
        print(f"  - {url}")
        
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
finally:
    if 'driver' in locals():
        driver.quit()
        print("\nSelenium driver closed")