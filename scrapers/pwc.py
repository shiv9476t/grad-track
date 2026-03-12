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
        if soup is None:
            return []
        scheme_url_status = self.extract_grad_scheme_links(soup)
        for url, status in scheme_url_status:
            scheme_soup = self.get_parsed_html(url)
            if scheme_soup is None:
                continue
            grad_scheme = self.parse_grad_scheme_page(scheme_soup, url, status)
            grad_scheme_list.append(grad_scheme)
        return grad_scheme_list
    
    def extract_grad_scheme_links(self, soup):
        scheme_url_status = []
        
        for card in soup.find_all("div", class_="hl-article"):
            a = card.find("a", href=True)
            p = card.find("p", class_="link-read-more")
            if a is None or p is None:
                continue
            url = urljoin(self.base_url, a["href"])
            status = p.get_text(strip=True)
            scheme_url_status.append((url, status))
            
        return scheme_url_status
    
    def parse_grad_scheme_page(self, soup, url, status):
        scheme_name = soup.find("h1").get_text(strip=True) if soup.find("h1") else "Unknown"
        
        location = None
        start_date = "Unknown"
        
        for item in soup.find_all("div", class_="case-study__items"):
            heading_tag = item.find("p", class_="case-study__item-heading")
            value_tag = item.find("p", class_="case-study__item-sub-heading")
            if heading_tag is None or value_tag is None:
                continue
            heading = heading_tag.get_text(strip=True)
            value = value_tag.get_text(strip=True)
            if heading == "Location":
                location = value
            elif heading == "Start date":
                start_date = value
                
        status = self.normalise_status(status)
                
        grad_scheme = GradScheme(
            company=self.company_name,
            scheme_name=scheme_name,
            location=location,
            salary="Unknown",
            status=status,
            start_date=start_date,
            url=url
        )
        
        return grad_scheme


            
