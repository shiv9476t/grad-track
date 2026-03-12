from bs4 import BeautifulSoup
from scrapers.lloyds import LloydsScraper

def load_fixture(filename):
    with open(f"tests/fixtures/{filename}", "r", encoding="utf-8") as f:
        return BeautifulSoup(f.read(), "html.parser")

def test_lloyds_parse_scheme_page():
    scraper = LloydsScraper()
    soup = load_fixture("lloyds_scheme.html")
    url = "https://www.lloydsbankinggrouptalent.com/our-opportunities/graduates/data-science-and-ai-graduate-scheme/"
    
    scheme = scraper.parse_grad_scheme_page(soup, url)
    
    assert scheme.scheme_name == "Data Science and AI Graduate Scheme"
    assert scheme.salary == "£45,000 + fantastic benefits"
    assert "Bristol" in scheme.location
    assert scheme.status == "Closed"