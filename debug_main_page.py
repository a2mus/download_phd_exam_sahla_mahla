import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

url = "https://sahla-mahla.com/phd-exam/phd-exam-2024-2025/"

try:
    response = requests.get(url)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    print(f"Page title: {soup.title.string if soup.title else 'No title'}")
    print("\n=== ALL LINKS ON THE PAGE ===")
    
    links = soup.find_all('a', href=True)
    print(f"Total links found: {len(links)}")
    
    for i, a_tag in enumerate(links[:20]):  # Show first 20 links
        href = a_tag['href']
        text = a_tag.get_text(strip=True)
        full_url = urljoin(url, href)
        print(f"{i+1}. Text: '{text}' -> URL: {full_url}")
    
    if len(links) > 20:
        print(f"... and {len(links) - 20} more links")
    
    print("\n=== LINKS CONTAINING EXAM-RELATED KEYWORDS ===")
    exam_links = []
    for a_tag in links:
        href = a_tag['href']
        text = a_tag.get_text(strip=True).lower()
        href_lower = href.lower()
        
        if any(keyword in href_lower or keyword in text for keyword in ['sujets', 'doctorat', 'concours', 'exam', 'phd']):
            full_url = urljoin(url, href)
            exam_links.append((text, full_url))
    
    print(f"Found {len(exam_links)} exam-related links:")
    for text, link in exam_links:
        print(f"- '{text}' -> {link}")
        
except Exception as e:
    print(f"Error: {e}")