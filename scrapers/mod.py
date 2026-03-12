from scrapers.base import BaseScraper
import re
from urllib.parse import urljoin
from models.grad_scheme import GradScheme

class MODScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            company_name="Ministry of Defence",
            base_url="https://des.mod.uk"
        )
        self.index_url = "https://des.mod.uk/careers/graduates-1/"

    def scrape_grad_schemes(self):
        grad_scheme_list = []
        soup = self.get_parsed_html(self.index_url)
        if soup is None:
            return []
        schemes = self.extract_grad_scheme_links(soup)
        for url, status in schemes:
            scheme_soup = self.get_parsed_html(url)
            if scheme_soup is None:
                 return []
            grad_scheme = self.parse_grad_scheme_page(scheme_soup, url, status)
            grad_scheme_list.append(grad_scheme)
        return grad_scheme_list

    def extract_grad_scheme_links(self, soup):
        schemes = []
        
        for div in soup.find_all("div", class_="fusion-layout-column"):
            if div.find("h3") == None:
                continue
            elif "Graduate Scheme" in div.find("h3").get_text():
                href = div.find("a", href=True)["href"]
                url = urljoin(self.base_url, href)
                status_p = div.find("p")
                if status_p and "not available" in status_p.get_text(strip=True).lower():
                    status = "Closed"
                else:
                    status = "Open"
                schemes.append((url, status))
        return schemes

    def parse_grad_scheme_page(self, soup, url, status):
        scheme_name = soup.find("h1").get_text(strip=True) if soup.find("h1") else "Unknown"

        location = None
        salary = None
        start_date = "Unknown"

        for h3 in soup.find_all("h3"):
            text = h3.get_text(strip=True).lower()
            next_p = h3.find_next("p")
            if not next_p:
                continue
            if "what" in text:
                salary_match = re.search(r"£[\d,]+", next_p.get_text())
                if salary_match:
                    salary = salary_match.group(0)
            if "where" in text:
                location = next_p.get_text(strip=True).split("\n")[0]

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