#python3 main.py
import json
from scraper import Scraper

with open("companies.json", "r") as file:
    companies_data = json.load(file)
    
for company in companies_data:
    Scraper(company["name"], company["url"]).scrape_company()