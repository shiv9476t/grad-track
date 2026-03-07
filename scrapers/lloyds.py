from scrapers.base import BaseScraper
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from grad_scheme import GradScheme

class LloydsScraper(BaseScraper):
    def __init__(self):
        super().__init__(
        company_name = "Lloyds",
        base_url = "https://www.lloydsbankinggrouptalent.com"
        )
        self.index_url = "https://www.lloydsbankinggrouptalent.com/our-opportunities/graduates/"
    
    def scrape_grad_schemes(self):
        grad_scheme_list = []
        soup = self.get_parsed_html(self.index_url)
        scheme_urls = self.extract_grad_scheme_links(soup)
        
        for url in scheme_urls:
            scheme_soup = self.get_parsed_html(url)
            grad_scheme = self.parse_grad_scheme_page(scheme_soup, url)
            grad_scheme_list.append(grad_scheme)
            
        return grad_scheme_list
    
    def extract_grad_scheme_links(self, soup):
        scheme_urls = []
        for card in soup.find_all("div", class_="card-team"):
            href = card.find("a", href=True)["href"]
            url = urljoin(self.base_url, href)
            scheme_urls.append(url)
        return scheme_urls
    
    def parse_grad_scheme_page(self, soup, url):
        scheme_name = soup.find("h1").get_text(strip=True)
        
        location = None
        salary = None
        status = None
        start_date = None
        
        for item in soup.find_all("div", class_="col-12"):
            h3 = item.find("h3")
            card_text = item.find("div", class_="card-text")
            if h3 and card_text:  # only proceed if both exist
                heading = h3.get_text(strip=True)
                value = card_text.get_text(strip=True)
                if heading == "Locations":
                    location = value
                elif heading == "Salary":
                    salary = value

        for item in soup.find_all("div", class_="accordion-item"):
            h3 = item.find("h3")
            p = item.find("p")
            if h3 and p:
                heading = h3.get_text(strip=True)
                value = p.get_text(strip=True)
                if "closing date" in heading.lower():
                    if "closed" in value.lower():
                        status = "Closed"
                    else:
                        status = "Open"
                
        grad_scheme = GradScheme(
            company=self.company_name,
            scheme_name=scheme_name,
            location=location,
            salary=salary,
            status=status,
            start_date="Not published",
            url=url
        )
        
        return grad_scheme

