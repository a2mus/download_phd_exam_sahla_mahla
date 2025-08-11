import requests
from bs4 import BeautifulSoup

url = 'https://lmd.sahla-dz.com/2sujets-des-concours-dacces-au-doctorat-en-informatique-option-ia-intelligence-artificielle/'

print(f"Analyzing page: {url}")
print("=" * 50)

try:
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'html.parser')
    
    print("=== PAGE TITLE ===")
    print(soup.title.text if soup.title else 'No title')
    
    print("\n=== IFRAMES ===")
    iframes = soup.find_all('iframe')
    print(f"Found {len(iframes)} iframes")
    for i, iframe in enumerate(iframes):
        src = iframe.get('src', 'No src')
        data_src = iframe.get('data-src', 'No data-src')
        print(f"Iframe {i+1}: src={src}, data-src={data_src}")
    
    print("\n=== POTENTIAL EXAM LINKS ===")
    links = soup.find_all('a', href=True)
    exam_links = [link for link in links if any(keyword in link.get('href', '').lower() for keyword in ['sujet', 'exam', 'concours', 'doctorat'])]
    print(f"Found {len(exam_links)} potential exam links")
    for i, link in enumerate(exam_links[:10]):
        href = link.get('href')
        text = link.text.strip()[:50]
        print(f"Link {i+1}: {href} - {text}")
    
    print("\n=== CONTENT DIVS ===")
    content_divs = soup.find_all('div', class_=lambda x: x and ('content' in x.lower() or 'post' in x.lower() or 'entry' in x.lower()))
    print(f"Found {len(content_divs)} content divs")
    for i, div in enumerate(content_divs[:3]):
        classes = div.get('class', [])
        print(f"Div {i+1}: classes={classes}")
        
except Exception as e:
    print(f"Error: {e}")