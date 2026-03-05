import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time

class Scraper:
    
    def __init__(self, name, base_url):
        self.name = name
        self.base_url = base_url
        self.visited = set()
        self.delay = 1
        
    def scrape_company(self):
        queue = [self.base_url]
        
        while queue:
            url = queue.pop(0)
            if url in self.visited:
                continue
            self.visited.add(url)
            soup = self.get_soup(url)

            if self.is_scheme_page(soup):
                self.parse_scheme_page(soup, url)
            else:
                links = self.extract_relevant_links(soup, url)
                queue.extend(links)
            
    def get_soup(self, url):
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "html.parser")
        time.sleep(self.delay)
        return soup

    #rule-based classifier
    #needs iproving by implementing a keyword list of roles, and checking if h1 text is in the list
    def is_scheme_page(self, soup):
#        text = soup.get_text().lower()
#        if "requirements" in text and "location" in text:
#            return True
#        else:
#            return False
        GRAD_SCHEME_KEYWORDS = {
            "software", "developer", "data", "analyst", "engineer", "consulting",
            "finance", "auditor", "marketing", "business", "actuarial", "legal",
            "law", "technology", "operations", "risk", "strategy", "sales",
            "design", "product", "research", "analytics", "cybersecurity",
            "accounting", "hr", "human", "resources", "engineering", "mechanical",
            "electrical", "civil", "chemical", "environmental", "pharmacy",
            "biomedical", "investment", "trading", "economics"
        }
    
        h1 = soup.find("h1")
        if not h1:
            return False
        
        words = h1.get_text(strip=True).lower().split()
        
        return any(word in GRAD_SCHEME_KEYWORDS for word in words)
            
    def extract_relevant_links(self, soup, current_url):
        filtered_links = []
        for link in soup.find_all("a", href=True):
            full_url = urljoin(current_url, link["href"])
            normalised_link = self.base_url.replace(".html", "").rstrip("/")
            if normalised_link in full_url and self.base_url != full_url:
                filtered_links.append(full_url)
        return filtered_links

    def parse_scheme_page(self, soup, url):
        title = soup.find("h1").get_text(strip=True)
        print(title, url)
    
    