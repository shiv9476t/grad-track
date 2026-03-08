from scrapers.grant_thornton import GrantThorntonScraper

s = GrantThorntonScraper()
grad_schemes = s.scrape_grad_schemes()
for scheme in grad_schemes:
    print(scheme.scheme_name, scheme.location, scheme.salary, scheme.status, scheme.url)