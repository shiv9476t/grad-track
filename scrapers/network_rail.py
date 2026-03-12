from scrapers.base import BaseScraper
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from models.grad_scheme import GradScheme

class NetworkRailScraper(BaseScraper):
    def __init__(self):
        super().__init__(
        company_name = "Network Rail",
        base_url = "https://www.earlycareers.networkrail.co.uk"
        )
        self.index_url = "https://www.earlycareers.networkrail.co.uk/programme/graduate"
    
    def scrape_grad_schemes(self):
        grad_scheme_list = []
        soup = self.get_parsed_html(self.index_url)
        if soup is None:
            return []
        scheme_urls = self.extract_grad_scheme_links(soup)
        
        for url in scheme_urls:
            scheme_soup = self.get_parsed_html(url)
            if scheme_soup is None:
                continue
            grad_scheme = self.parse_grad_scheme_page(scheme_soup, url)
            grad_scheme_list.append(grad_scheme)
            
        return grad_scheme_list
    
    def extract_grad_scheme_links(self, soup):
        scheme_urls = []
        
        for section in soup.find_all("section", class_="schemes"):
            divs = section.find_all("div", class_="scheme-block")
            for div in divs:
                url = div.find("a", href=True)["href"]
                scheme_urls.append(url)
        return scheme_urls
    
    def parse_grad_scheme_page(self, soup, url):
        scheme_name = soup.find("h1").get_text(strip=True)

        location = "Across the UK"
        salary = "Unknown"
        status = "Unknown"
        start_date = "Unknown"

        for section in soup.find_all("section", class_="text-and-image"):
            text = section.get_text(" ", strip=True)

            # salary
            salary_match = re.search(r"Salary:\s*(£[\d,]+[^\n.]*)", text)
            if salary_match:
                salary = salary_match.group(1).strip()

            # start date
            start_match = re.search(r"Start date:\s*([A-Za-z]+ \d{4})", text)
            if start_match:
                start_date = start_match.group(1).strip()

            # status
            if "closed for applications" in text.lower():
                status = "Closed"
            elif "now open" in text.lower():
                status = "Open"
                
        status = self.normalise_status(status)

        return GradScheme(
            company=self.company_name,
            scheme_name=scheme_name,
            location=location,
            salary=salary,
            status=status,
            start_date=start_date,
            url=url
        )

