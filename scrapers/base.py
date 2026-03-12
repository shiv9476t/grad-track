import requests
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, urlunparse
import time

class BaseScraper:
    
    def __init__(self, company_name, base_url, delay=1):
        self.company_name = company_name
        self.base_url = base_url
        self.delay = delay
    
    def scrape_grad_schemes(self):
        raise NotImplementedError
        
    def get_parsed_html(self, url):
        try:
            r = requests.get(url, timeout=10)
            r.raise_for_status()
            soup = BeautifulSoup(r.text, "html.parser")
            time.sleep(self.delay)
            return soup
        except requests.RequestException:
            return None

    def get_parsed_html_playwright(self, url, cookie_selector=None):
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=False)
                page = browser.new_page()
                page.goto(url)

                if cookie_selector:
                    try:
                        page.click(cookie_selector)
                    except Exception:
                        pass 

                page.wait_for_selector("h1")
                html = page.content()
                browser.close()
            soup = BeautifulSoup(html, "html.parser")
            time.sleep(self.delay)
            return soup
        except Exception:
            return None
    
    def get_json(self, url):
        try:
            r = requests.get(url, timeout=10)
            r.raise_for_status()
            data = r.json()
            return data
        except (requests.RequestException, ValueError):
            return None
    
    def normalise_url(self, url):
        # Parse the URL
        parsed = urlparse(url)

        # Remove query and fragment, normalize path
        path = parsed.path.replace(".html", "").rstrip("/")

        # Rebuild the URL without query or fragment
        normalised = urlunparse((
            parsed.scheme,
            parsed.netloc,
            path,
            "",  # params
            "",  # query
            ""   # fragment
        ))
        #print(normalised)
        return normalised
    
    @staticmethod
    def normalise_status(status):
        if status is None:
            return "Unknown"
        status_lower = status.lower()
        if "open" in status_lower:
            return "Open"
        elif "close" in status_lower or "not available" in status_lower:
            return "Closed"
        else:
            return "Unknown"