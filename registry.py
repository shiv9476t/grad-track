from scrapers.pwc import PwCScraper
from scrapers.lloyds import LloydsScraper
from scrapers.mi5 import MI5Scraper
from scrapers.civil_service import CivilServiceScraper
from scrapers.network_rail import NetworkRailScraper
from scrapers.grant_thornton import GrantThorntonScraper
from database import GradSchemeDB

SCRAPERS = [PwCScraper, LloydsScraper, MI5Scraper, CivilServiceScraper, NetworkRailScraper, GrantThorntonScraper]

db = GradSchemeDB()

def run_all():

    for ScraperClass in SCRAPERS:
        scraper = ScraperClass()
        schemes = scraper.scrape_grad_schemes()
        for scheme in schemes:
            db.upsert_grad_scheme(scheme)
    
