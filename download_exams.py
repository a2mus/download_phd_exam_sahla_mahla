import os
import re
import requests
import urllib.parse
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
import uuid
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

class PhDExamDownloader:
    def __init__(self, base_url, destination_folder, use_selenium=True):
        """
        Initialize the downloader with base URL and destination folder
        
        Args:
            base_url (str): The main URL containing links to exam pages
            destination_folder (str): Path to save downloaded PDFs
            use_selenium (bool): Whether to use Selenium for handling lazy-loaded content
        """
        self.base_url = base_url
        self.destination_folder = destination_folder
        self.use_selenium = use_selenium
        self.driver = None
        
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # Initialize Selenium WebDriver if requested
        if self.use_selenium:
            self._init_selenium_driver()
        
        # Create destination folder if it doesn't exist
        os.makedirs(self.destination_folder, exist_ok=True)
        
    def _init_selenium_driver(self):
        """
        Initialize Selenium WebDriver with Chrome options
        """
        try:
            chrome_options = Options()
            chrome_options.add_argument('--headless')  # Run in background
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--window-size=1920,1080')
            chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')
            
            # Use ChromeDriverManager to automatically download and manage ChromeDriver
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.driver.implicitly_wait(10)  # Wait up to 10 seconds for elements to appear
            print("Selenium WebDriver initialized successfully")
            
        except Exception as e:
            print(f"Warning: Could not initialize Selenium WebDriver: {e}")
            print("Falling back to requests-only mode")
            self.use_selenium = False
            self.driver = None
    
    def _close_selenium_driver(self):
        """
        Close Selenium WebDriver
        """
        if self.driver:
            try:
                self.driver.quit()
                print("Selenium WebDriver closed")
            except Exception as e:
                print(f"Error closing Selenium WebDriver: {e}")
    
    def extract_content_with_selenium(self, page_url):
        """
        Extract content from a page using Selenium to handle lazy-loaded content
        
        Args:
            page_url (str): URL of the page to extract content from
            
        Returns:
            dict: Dictionary with 'type' (pdf or images) and 'urls' (list of URLs)
        """
        if not self.driver:
            return None
            
        try:
            print(f"Loading page with Selenium: {page_url}")
            self.driver.get(page_url)
            
            # Wait for the page to load and scroll to trigger lazy loading
            time.sleep(3)
            
            # Scroll down to trigger lazy loading
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            
            # Scroll back up
            self.driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(2)
            
            # Wait for iframes to load
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.TAG_NAME, "iframe"))
                )
                print("Iframes detected, waiting for content to load...")
                time.sleep(3)
            except TimeoutException:
                print("No iframes found or timeout waiting for iframes")
            
            # Get the page source after JavaScript execution
            page_source = self.driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')
            
            result = {'type': None, 'urls': []}
            
            # Find iframe with Google Docs viewer (PDF) - updated to include 'viewer'
            iframes = soup.find_all('iframe', src=lambda s: s and ('docs.google.com/gview' in s or 'docs.google.com/viewer' in s or 'drive.google.com' in s))
            if not iframes:
                iframes = soup.find_all('iframe', attrs={'data-src': lambda s: s and ('docs.google.com/gview' in s or 'docs.google.com/viewer' in s or 'drive.google.com' in s)})
            
            # Process PDF iframes
            for iframe in iframes:
                iframe_src = iframe.get('src') or iframe.get('data-src')
                
                # Handle gview links
                url_param = re.search(r'url=([^&]+)', iframe_src)
                if url_param:
                    pdf_url = urllib.parse.unquote(url_param.group(1))
                    if pdf_url not in result['urls']:
                        result['type'] = 'pdf'
                        result['urls'].append(pdf_url)
                    continue

                # Handle Google Docs viewer with srcid parameter
                if 'docs.google.com/viewer' in iframe_src and 'srcid=' in iframe_src:
                    file_id = iframe_src.split('srcid=')[1].split('&')[0]
                    pdf_url = f'https://drive.google.com/uc?export=download&id={file_id}'
                    if pdf_url not in result['urls']:
                        result['type'] = 'pdf'
                        result['urls'].append(pdf_url)
                    continue

                # Handle drive.google.com links
                drive_match = re.search(r'drive\.google\.com/file/d/([a-zA-Z0-9_-]+)', iframe_src)
                if drive_match:
                    file_id = drive_match.group(1)
                    pdf_url = f'https://drive.google.com/uc?export=download&id={file_id}'
                    if pdf_url not in result['urls']:
                        result['type'] = 'pdf'
                        result['urls'].append(pdf_url)
            
            # If PDF iframes found, return them
            if result['urls']:
                print(f"Found {len(result['urls'])} PDF(s) using Selenium")
                return result
                
            # Check for embedded images in iframes or divs
            image_containers = soup.find_all(['iframe', 'div'], class_=lambda c: c and ('ndfHFb-c4YZDc-cYSp0e-DARUcf-PLDbbf' in c))
            
            # Also look for images directly
            images = soup.find_all('img', src=True)
            
            if image_containers or images:
                result['type'] = 'images'
                
                # Extract images from containers
                for container in image_containers:
                    container_images = container.find_all('img', src=True)
                    for img in container_images:
                        img_url = urljoin(page_url, img['src'])
                        if img_url not in result['urls']:
                            result['urls'].append(img_url)
                
                # Add direct images
                for img in images:
                    # Only include images that might be exam content (filter out small icons, etc.)
                    width = img.get('width')
                    height = img.get('height')
                    try:
                        if (width and int(width) > 200) or (height and int(height) > 200):
                            img_url = urljoin(page_url, img['src'])
                            if img_url not in result['urls']:
                                result['urls'].append(img_url)
                    except (ValueError, TypeError):
                        # If width/height can't be converted to int, include the image anyway
                        img_url = urljoin(page_url, img['src'])
                        if img_url not in result['urls']:
                            result['urls'].append(img_url)
            
            # If we found images, return them
            if result['urls']:
                print(f"Found {len(result['urls'])} image(s) using Selenium")
                return result
            
            print("No content found using Selenium")
            return None
            
        except Exception as e:
            print(f"Error extracting content with Selenium from {page_url}: {e}")
            return None
        
    def get_exam_page_links(self):
        """
        Scrape the main page to find links to individual exam pages
        
        Returns:
            list: List of URLs to individual exam pages
        """
        try:
            response = self.session.get(self.base_url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            links = []
            
            # Find all links that might lead to exam pages
            for a_tag in soup.find_all('a', href=True):
                href = a_tag['href']
                # Check if the link might be an exam page
                if 'sujets' in href.lower() or 'doctorat' in href.lower() or 'concours' in href.lower():
                    full_url = urljoin(self.base_url, href)
                    links.append(full_url)
            
            # If no exam page links found, treat the base URL itself as an exam page
            if not links:
                print("No exam page links found. Treating base URL as exam page.")
                links.append(self.base_url)
            
            print(f"Found {len(links)} potential exam page links")
            return links
            
        except Exception as e:
            print(f"Error getting exam page links: {e}")
            return []
    
    def extract_pdf_url_from_iframe(self, page_url):
        """
        Extract PDF URL from iframe on the exam page
        
        Args:
            page_url (str): URL of the exam page
            
        Returns:
            dict: Dictionary with 'type' (pdf or images) and 'urls' (list of URLs)
        """
        try:
            response = self.session.get(page_url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            result = {'type': None, 'urls': []}
            
            # Find iframe with Google Docs viewer (PDF)
            iframes = soup.find_all('iframe', src=lambda s: s and ('docs.google.com/gview' in s or 'drive.google.com' in s))
            if not iframes:
                iframes = soup.find_all('iframe', attrs={'data-src': lambda s: s and ('docs.google.com/gview' in s or 'drive.google.com' in s)})
            
            # Process PDF iframes
            for iframe in iframes:
                iframe_src = iframe.get('src') or iframe.get('data-src')
                
                # Handle gview links
                url_param = re.search(r'url=([^&]+)', iframe_src)
                if url_param:
                    pdf_url = urllib.parse.unquote(url_param.group(1))
                    if pdf_url not in result['urls']:
                        result['type'] = 'pdf'
                        result['urls'].append(pdf_url)
                    continue

                # Handle drive.google.com links
                drive_match = re.search(r'drive\.google\.com/file/d/([a-zA-Z0-9_-]+)', iframe_src)
                if drive_match:
                    file_id = drive_match.group(1)
                    pdf_url = f'https://drive.google.com/uc?export=download&id={file_id}'
                    if pdf_url not in result['urls']:
                        result['type'] = 'pdf'
                        result['urls'].append(pdf_url)
            
            # If PDF iframes found, return them
            if result['urls']:
                return result
                
            # Check for embedded images in iframes or divs
            image_containers = soup.find_all(['iframe', 'div'], class_=lambda c: c and ('ndfHFb-c4YZDc-cYSp0e-DARUcf-PLDbbf' in c))
            
            # Also look for images directly
            images = soup.find_all('img', src=True)
            
            if image_containers or images:
                result['type'] = 'images'
                
                # Extract images from containers
                for container in image_containers:
                    container_images = container.find_all('img', src=True)
                    for img in container_images:
                        img_url = urljoin(page_url, img['src'])
                        if img_url not in result['urls']:
                            result['urls'].append(img_url)
                
                # Add direct images
                for img in images:
                    # Only include images that might be exam content (filter out small icons, etc.)
                    if img.get('width') and int(img['width']) > 200 or img.get('height') and int(img['height']) > 200:
                        img_url = urljoin(page_url, img['src'])
                        if img_url not in result['urls']:
                            result['urls'].append(img_url)
            
            # If we found images, return them
            if result['urls']:
                return result
            
            # If no iframes with images, try looking for direct download buttons
            download_btn = soup.find('button', string=re.compile(r'Download', re.IGNORECASE))
            if download_btn and download_btn.parent and download_btn.parent.name == 'a' and download_btn.parent.has_attr('href'):
                pdf_url = urljoin(page_url, download_btn.parent['href'])
                result['type'] = 'pdf'
                result['urls'].append(pdf_url)
                return result
            
            # Try to find any link that might be a PDF
            pdf_links = soup.find_all('a', href=lambda href: href and href.lower().endswith('.pdf'))
            if pdf_links:
                pdf_url = urljoin(page_url, pdf_links[0]['href'])
                result['type'] = 'pdf'
                result['urls'].append(pdf_url)
                return result
                
            return None
            
        except Exception as e:
            print(f"Error extracting content from {page_url}: {e}")
            return None
    
    def download_pdf(self, pdf_url, page_url):
        """
        Download PDF from the given URL
        
        Args:
            pdf_url (str): URL of the PDF to download
            page_url (str): Original page URL (for generating filename)
            
        Returns:
            bool: True if download was successful, False otherwise
        """
        try:
            # Download the file
            print(f"Downloading {pdf_url}")
            response = self.session.get(pdf_url, stream=True)
            response.raise_for_status()

            filename = None
            # 1. Try to get filename from Content-Disposition header
            content_disposition = response.headers.get('Content-Disposition')
            if content_disposition:
                fname_match = re.search(r'filename\*?=([^;]+)', content_disposition)
                if fname_match:
                    try:
                        # Decode filename according to RFC 5987
                        header_filename = urllib.parse.unquote(fname_match.group(1).strip().strip("'\""))
                        if header_filename.lower().endswith('.pdf'):
                            filename = header_filename
                    except Exception as e:
                        print(f"Warning: Could not decode Content-Disposition filename: {e}")

            # 2. If not found in header, try to extract from PDF URL
            if not filename:
                url_path = urllib.parse.urlparse(pdf_url).path
                url_filename = os.path.basename(url_path)
                if url_filename and url_filename.lower().endswith('.pdf'):
                    filename = url_filename
                
            # 3. Fallback to generating from page URL
            if not filename:
                page_name = os.path.basename(page_url).replace('.html', '').replace('/', '-')
                filename = f"{page_name}.pdf"
            
            # 4. Sanitize filename
            # Remove invalid characters for Windows filenames
            filename = re.sub(r'[\\/:*?"<>|]', '-', filename)
            # Replace multiple dashes with a single one
            filename = re.sub(r'-+', '-', filename)
            # Remove leading/trailing dashes
            filename = filename.strip('-')
            # Ensure it ends with .pdf
            if not filename.lower().endswith('.pdf'):
                filename = f"{filename}.pdf"

            # 5. Ensure filename is not empty or just ".pdf"
            if not filename or filename.lower() == '.pdf':
                filename = f"{str(uuid.uuid4())}.pdf" # Use UUID as a fallback

            # Full path to save the file
            filepath = os.path.join(self.destination_folder, filename)
            
            print(f"Saving to {filepath}")
            
            # Check if it's actually a PDF
            content_type = response.headers.get('Content-Type', '')
            if 'application/pdf' not in content_type and not pdf_url.lower().endswith('.pdf'):
                print(f"Warning: The URL might not be a PDF (Content-Type: {content_type})")
            
            # Save the file
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            
            print(f"Successfully downloaded {filename}")
            return True
            
        except Exception as e:
            print(f"Error downloading PDF from {pdf_url}: {e}")
            return False
            
    def download_images(self, image_urls, page_url):
        """
        Download images from the given URLs into a dedicated folder
        
        Args:
            image_urls (list): List of image URLs to download
            page_url (str): Original page URL (for generating folder name)
            
        Returns:
            bool: True if at least one image was downloaded successfully, False otherwise
        """
        try:
            # Generate folder name from the page URL
            page_name = os.path.basename(page_url).replace('.html', '').replace('/', '-')
            page_name = re.sub(r'[\\/:*?"<>|]', '-', page_name)  # Remove invalid folder name characters
            
            # Create a unique folder name if the page name is too generic
            if len(page_name) < 5:  # If the page name is too short, add a unique identifier
                page_name = f"{page_name}-{str(uuid.uuid4())[:8]}"
                
            # Full path to the folder
            folder_path = os.path.join(self.destination_folder, page_name)
            os.makedirs(folder_path, exist_ok=True)
            
            successful_downloads = 0
            for i, img_url in enumerate(image_urls):
                try:
                    # Generate a unique filename for each image
                    extension = os.path.splitext(img_url)[1]
                    if not extension or len(extension) <= 1:
                        extension = '.jpg'  # Default extension
                    
                    filename = f"image_{i+1}{extension}"
                    filepath = os.path.join(folder_path, filename)
                    
                    # Check if file already exists, if so, add a unique identifier
                    if os.path.exists(filepath):
                        unique_id = str(uuid.uuid4())[:8]
                        filename = f"image_{i+1}_{unique_id}{extension}"
                        filepath = os.path.join(folder_path, filename)
                    
                    # Download the image
                    print(f"Downloading image {i+1}/{len(image_urls)}: {img_url} to {filepath}")
                    response = self.session.get(img_url, stream=True)
                    response.raise_for_status()
                    
                    # Save the image
                    with open(filepath, 'wb') as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            if chunk:
                                f.write(chunk)
                    
                    successful_downloads += 1
                    print(f"Successfully downloaded image {i+1}/{len(image_urls)}")
                    
                    # Add a small delay to avoid overwhelming the server
                    time.sleep(0.5)
                    
                except Exception as e:
                    print(f"Error downloading image {i+1}/{len(image_urls)} from {img_url}: {e}")
            
            print(f"Downloaded {successful_downloads} out of {len(image_urls)} images to {folder_path}")
            return successful_downloads > 0
            
        except Exception as e:
            print(f"Error downloading images for {page_url}: {e}")
            return False
    
    def run(self):
        """
        Main method to run the downloader
        """
        # Get initial links to exam pages
        initial_links = self.get_exam_page_links()
        
        if not initial_links:
            print("No exam page links found. Exiting.")
            return
            
        pages_to_process = list(initial_links)
        processed_pages = set()
        successful_downloads = 0
        
        while pages_to_process:
            page_url = pages_to_process.pop(0)
            if page_url in processed_pages:
                continue
            
            processed_pages.add(page_url)
            
            print(f"\nProcessing page: {page_url}")
            
            # Extract content URLs from the page
            # Try Selenium first for lazy-loaded content, then fall back to requests
            content_info = None
            if self.use_selenium and self.driver:
                content_info = self.extract_content_with_selenium(page_url)
            
            # If Selenium didn't find content or isn't available, try the traditional method
            if not content_info:
                content_info = self.extract_pdf_url_from_iframe(page_url)
            
            if content_info and content_info['urls']:
                if content_info['type'] == 'pdf':
                    # Handle PDF downloads
                    for pdf_url in content_info['urls']:
                        print(f"Found PDF URL: {pdf_url}")
                        if self.download_pdf(pdf_url, page_url):
                            successful_downloads += 1
                elif content_info['type'] == 'images':
                    # Handle image downloads
                    print(f"Found {len(content_info['urls'])} images")
                    if self.download_images(content_info['urls'], page_url):
                        successful_downloads += 1
            else:
                print(f"No direct content found on {page_url}. Looking for sub-links.")
                try:
                    response = self.session.get(page_url)
                    response.raise_for_status()
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    # Look for links within the main content area
                    content_area = soup.find('div', class_='td-post-content')
                    if content_area:
                        sub_links = content_area.find_all('a', href=True)
                        new_links_found = 0
                        for link in sub_links:
                            full_url = urljoin(page_url, link['href'])
                            # Check if it's a valid, new link
                            if 'sahla-dz.com' in full_url and full_url not in processed_pages and full_url not in pages_to_process:
                                # Check if it looks like an exam page
                                if 'sujet' in full_url.lower() or 'doctorat' in full_url.lower() or 'concour' in full_url.lower():
                                    pages_to_process.append(full_url)
                                    new_links_found += 1
                        if new_links_found > 0:
                            print(f"Found {new_links_found} new links to process.")
                        else:
                            print(f"No new sub-links found on {page_url}")
                    else:
                        print(f"Could not find content area on {page_url}")
                except Exception as e:
                    print(f"Error while looking for sub-links on {page_url}: {e}")

            # Add a small delay to avoid overwhelming the server
            time.sleep(1)
        
        print(f"\nDownload complete. Processed {len(processed_pages)} pages and successfully downloaded content from {successful_downloads} of them.")
        
        # Clean up Selenium WebDriver
        if self.use_selenium:
            self._close_selenium_driver()


def main():
    # Base URL containing links to exam pages
    base_url = "https://lmd.sahla-dz.com/sujets-concours-doctorat-informatique/"
    
    # Destination folder to save PDFs and images
    destination_folder = "d:/Developpement/Projets/Side_Projects/download_phd_exam_sahla_mahla/exams/"
    
    # Create and run the downloader
    downloader = PhDExamDownloader(base_url, destination_folder)
    downloader.run()


if __name__ == "__main__":
    main()