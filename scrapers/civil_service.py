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
        scheme_urls = self.extract_grad_scheme_links(data)
        salary = self.get_salary()
        status = self.get_status()
        for url in scheme_urls:
            scheme_soup = self.get_parsed_html(url)
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
        div_list = soup.find_all("div", class_="card-item__content")
        for div in div_list:
            h3 = div.find("h3")
            if "starting salary" in h3.get_text(strip=True).lower():
                p = div.find("p").get_text(strip=True)
                salary = re.search(r"£[\d,]+", p).group()
        return salary
    
    def get_status(self):
        status = "Unknown"
        soup = self.get_parsed_html(self.status_page_url)
        h3 = soup.find("h3", class_="wp-block-heading").get_text(strip=True)
        if "closed" in h3.lower():
            status = "Closed"
        else:
            status = "Open"
        
        return status
    
    def parse_grad_scheme_page(self, soup, url, salary, status):
        scheme_name = soup.find("title").get_text(strip=True).replace(" | Civil Service Careers", "")
        
        location = None
        status = status
        start_date = "September"
        
        h3_list = soup.find_all("h3", class_="wp-block-heading")
        for h3 in h3_list:
            if h3.get_text(strip=True) == "Location":
                p = h3.find_next()
                location = p.get_text(strip=True).split(".")[0]
                
        h2_list = soup.find_all("h2", class_="wp-block-heading")
        for h2 in h2_list:
            if h2.get_text(strip=True) == "Location":
                p = h2.find_next()
                location = p.get_text(strip=True).split(".")[0]
                
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

