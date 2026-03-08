from scrapers.civil_service import CivilServiceScraper

CVscraper = CivilServiceScraper()
grad_schemes = CVscraper.scrape_grad_schemes()
for scheme in grad_schemes:
    print(scheme.scheme_name, scheme.location, scheme.salary, scheme.status, scheme.url)