from scrapers.network_rail import NetworkRailScraper

s = NetworkRailScraper()
grad_schemes = s.scrape_grad_schemes()
for scheme in grad_schemes:
    print(scheme.scheme_name, scheme.location, scheme.salary, scheme.status, scheme.url)