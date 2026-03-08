from scrapers.base import BaseScraper
import re
from urllib.parse import urljoin
from models.grad_scheme import GradScheme

class GrantThorntonScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            company_name="Grant Thornton",
            base_url="https://www.grantthornton.co.uk"
        )
        self.index_url = "https://www.grantthornton.co.uk/careers/early-careers-job-search/?jobPostingGrouping=Graduate"

    def scrape_grad_schemes(self):
        grad_scheme_list = []
        soup = self.get_parsed_html(self.index_url)
        schemes = self.extract_grad_scheme_links(soup)
        for url in schemes:
            scheme_soup = self.get_parsed_html(url)
            grad_scheme = self.parse_grad_scheme_page(scheme_soup, url)
            grad_scheme_list.append(grad_scheme)
        return grad_scheme_list

    def extract_grad_scheme_links(self, soup):
        schemes = []
        div = soup.find("div", class_="career-items")
        for a in div.find_all("a"):
            href = a["href"]
            url = urljoin(self.base_url, href)
            schemes.append(url)
    
        return schemes

    def parse_grad_scheme_page(self, soup, url):
        scheme_name = soup.find("h1").get_text(strip=True) if soup.find("h1") else "Unknown"

        location = None
        salary = "Competitive"
        status = "Unknown"
        start_date = "Unknown"

        location_match = re.search(r" - ([A-Za-z\s]+)$", scheme_name)
        location = location_match.group(1).strip() if location_match else "Unknown"

        # start date from scheme name e.g. "Autumn 2026"
        start_match = re.search(r"(Autumn|Spring|Summer|Winter)\s+\d{4}", scheme_name, re.I)
        start_date = start_match.group(0) if start_match else "Not published"

        # status - apply link in main content
        main = soup.find("main") or soup
        apply_link = main.find("a", href=re.compile(r"apply", re.I))
        status = "Open" if apply_link else "Closed"
        
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