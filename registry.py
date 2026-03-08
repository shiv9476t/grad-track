from scrapers.pwc import PwCScraper
from scrapers.lloyds import LloydsScraper
from scrapers.mi5 import MI5Scraper
from scrapers.civil_service import CivilServiceScraper
from database import GradSchemeDB

SCRAPERS = [PwCScraper, LloydsScraper, MI5Scraper, CivilServiceScraper]

db = GradSchemeDB()

for ScraperClass in SCRAPERS:
    scraper = ScraperClass()
    schemes = scraper.scrape_grad_schemes()
    for scheme in schemes:
        db.save_grad_scheme(scheme)
    
