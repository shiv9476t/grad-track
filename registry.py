from scrapers.pwc import PwCScraper
from scrapers.lloyds import LloydsScraper
from scrapers.mi5 import MI5Scraper
from scrapers.civil_service import CivilServiceScraper
from scrapers.network_rail import NetworkRailScraper
from scrapers.grant_thornton import GrantThorntonScraper
from scrapers.mod import MODScraper
from database import GradSchemeDB

import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
    }
    
SCRAPERS = [PwCScraper, LloydsScraper, MI5Scraper, CivilServiceScraper, NetworkRailScraper, GrantThorntonScraper, MODScraper]

db = GradSchemeDB()

def run_all():
    for ScraperClass in SCRAPERS:
        scraper = ScraperClass()
        try:
            schemes = scraper.scrape_grad_schemes()
            logging.info(f"Scraped {len(schemes)} schemes from {scraper.company_name}")
            for scheme in schemes:
                db.upsert_grad_scheme(scheme)
        except Exception as e:
            logging.error(f"Scraper for {scraper.company_name} failed: {e}")
    
