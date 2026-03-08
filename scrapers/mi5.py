from scrapers.base import BaseScraper
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from models.grad_scheme import GradScheme

class MI5Scraper(BaseScraper):
    def __init__(self):
        super().__init__(
        company_name = "MI5",
        base_url = "https://www.mi5.gov.uk"
        )
        self.index_url = "https://www.mi5.gov.uk/careers/opportunities/graduates"
    
    def scrape_grad_schemes(self):
        grad_scheme_list = []
        soup = self.get_parsed_html_playwright(self.index_url, cookie_selector="#ccc-notify-accept")
        scheme_urls = self.extract_grad_scheme_links(soup)
        
        for url in scheme_urls:
            scheme_soup = self.get_parsed_html_playwright(url, cookie_selector="#ccc-notify-accept")
            grad_scheme = self.parse_grad_scheme_page(scheme_soup, url)
            grad_scheme_list.append(grad_scheme)
            
        return grad_scheme_list
    
    def extract_grad_scheme_links(self, soup):
        scheme_urls = []
        section = soup.find("section", class_="big-image-cross-link dark-block")
        for link in section.find_all("a"):
            href = link["href"]
            url = urljoin(self.base_url, href)
            scheme_urls.append(url)
        return scheme_urls
    
    def parse_grad_scheme_page(self, soup, url):
        scheme_name = soup.find("h1").get_text(strip=True)
        
        location = "Unknown"
        salary = "Unknown"
        status = None
        start_date = "Unknown"
        
        for item in soup.find_all("div", class_="grid-4"):
            p_tags = item.find_all("p")
            if "starting salary" in p_tags[0].get_text(strip=True).lower():
                salary = p_tags[1].get_text(strip=True)
            if p_tags[0].get_text(strip=True) == "Location":
                location = p_tags[1].get_text(strip=True)
                
        main = soup.find("main")
        apply_button = main.find("a", string=lambda text: text and "apply" in text.lower())
        if apply_button:
            status = "Open"
        else:
            status = "Closed"
            
        status = self.normalise_status(status)
                      
        grad_scheme = GradScheme(
            company=self.company_name,
            scheme_name=scheme_name,
            location=location,
            salary=salary,
            status=status,
            start_date=start_date,
            url=url
        )
        
        return grad_scheme

   
