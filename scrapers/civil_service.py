from scrapers.base import BaseScraper
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from models.grad_scheme import GradScheme

class CivilServiceScraper(BaseScraper):
    def __init__(self):
        super().__init__(
        company_name = "Civil Service",
        base_url = "https://www.civil-service-careers.gov.uk"
        )
        self.index_url = "https://www.civil-service-careers.gov.uk/fast-stream/fs-all-schemes/"
        self.API_endpoint = "https://www.civil-service-careers.gov.uk/wp-json/wp/v2/scheme?context=view&per_page=100&orderby=title&order=asc&include=&_locale=user"
        self.salary_page_url = "https://www.civil-service-careers.gov.uk/fast-stream/"
        self.status_page_url = "https://www.civil-service-careers.gov.uk/fast-stream/fs-all-schemes/"
    
    def scrape_grad_schemes(self):
        grad_scheme_list = []
        data = self.get_json(self.API_endpoint)
        if data is None:
            return []
        scheme_urls = self.extract_grad_scheme_links(data)
        salary = self.get_salary()
        status = self.get_status()
        for url in scheme_urls:
            scheme_soup = self.get_parsed_html(url)
            if scheme_soup is None:
                continue
            grad_scheme = self.parse_grad_scheme_page(scheme_soup, url, salary, status)
            grad_scheme_list.append(grad_scheme)
        return grad_scheme_list
    
    def extract_grad_scheme_links(self, data):
        scheme_urls = []
        for scheme in data:
            url = scheme["link"]
            scheme_urls.append(url)
        return scheme_urls
    
    def get_salary(self):
        salary = "Unknown"
        soup = self.get_parsed_html(self.salary_page_url)
        if soup is None:
            return salary
        for div in soup.find_all("div", class_="card-item__content"):
            h3 = div.find("h3")
            if h3 and "starting salary" in h3.get_text(strip=True).lower():
                p = div.find("p")
                if p:
                    salary_match = re.search(r"£[\d,]+", p.get_text(strip=True))
                    if salary_match:
                        salary = salary_match.group()
        return salary
    
    def get_status(self):
        status = "Unknown"
        soup = self.get_parsed_html(self.status_page_url)
        if soup is None:
            return status
        h3 = soup.find("h3", class_="wp-block-heading")
        if h3:
            if "closed" in h3.get_text(strip=True).lower():
                status = "Closed"
            else:
                status = "Open"
        return status
    
    def parse_grad_scheme_page(self, soup, url, salary, status):
        title = soup.find("title")
        scheme_name = title.get_text(strip=True).replace(" | Civil Service Careers", "") if title else "Unknown"
        
        location = None
        start_date = "September"
        
        for h3 in soup.find_all("h3", class_="wp-block-heading"):
            if h3.get_text(strip=True) == "Location":
                p = h3.find_next()
                if p:
                    location = p.get_text(strip=True).split(".")[0]
                
        for h2 in soup.find_all("h2", class_="wp-block-heading"):
            if h2.get_text(strip=True) == "Location":
                p = h2.find_next()
                if p:
                    location = p.get_text(strip=True).split(".")[0]
                
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
