#from scrapers.pwc import PWCScraper
#from scrapers.lloyds import LloydsScraper
#from scrapers.mi5 import MI5Scraper
#
#scraper = MI5Scraper()
#schemes = scraper.scrape_grad_schemes()
#for scheme in schemes:
#    print(scheme.scheme_name, scheme.status, scheme.location, scheme.salary)

from grad_scheme_database import GradSchemeDB

schemes = GradSchemeDB().get_schemes()

for scheme in schemes:
    print(scheme["company"], scheme["scheme_name"])