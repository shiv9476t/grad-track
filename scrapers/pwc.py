from scrapers.base import BaseScraper
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from models.grad_scheme import GradScheme

class PwCScraper(BaseScraper):
    def __init__(self):
        super().__init__(
        company_name = "PWC",
        base_url = "https://www.pwc.co.uk"
        )
        self.index_url = "https://www.pwc.co.uk/careers/early-careers/graduate.html"
    
    def scrape_grad_schemes(self):
        grad_scheme_list = []
        soup = self.get_parsed_html(self.index_url)
        scheme_url_status = self.extract_grad_scheme_links(soup)
        for url, status in scheme_url_status:
            scheme_soup = self.get_parsed_html(url)
            grad_scheme = self.parse_grad_scheme_page(scheme_soup, url, status)
            grad_scheme_list.append(grad_scheme)
        return grad_scheme_list
    
    def extract_grad_scheme_links(self, soup):
        scheme_url_status = []
        for card in soup.find_all("div", class_="hl-article"):
            href = card.find("a", href=True)["href"]
            url = urljoin(self.base_url, href)
            status = card.find("p", class_="link-read-more").get_text(strip=True)
            scheme_url_status.append((url, status))

        return scheme_url_status
    
    def parse_grad_scheme_page(self, soup, url, status):
        scheme_name = soup.find("h1").get_text(strip=True)
        
        location = None
        start_date = None
        
        for item in soup.find_all("div", class_="case-study__items"):
            heading = item.find("p", class_="case-study__item-heading").get_text(strip=True)
            value = item.find("p", class_="case-study__item-sub-heading").get_text(strip=True)
            if heading == "Location":
                location = value
            elif heading == "Start date":
                start_date = value
                
        grad_scheme = GradScheme(
            company=self.company_name,
            scheme_name=scheme_name,
            location=location,
            salary="Not published",
            status=status,
            start_date=start_date,
            url=url
        )
        
        return grad_scheme


            
