What it is:

GradTrack is a platform that connects UK uni students with grad schemes. Its aim is to aggregate all UK graduate schemes in one place, providing accurate, up-to-date information.

Features:

Scrapes and stores grad schemes across 7 UK companies
Automatic updates to grad scheme data every 24 hours
Classifies grad schemes by industry
Provides a user interface for users to view available grad schemes
Displays relevant grad schemes according to user's desired industry

Tech stack:

Python
SQLite
Flask
HTML
Tailwind CSS
Javascript
Requests
BeautifulSoup
Playwright (for JS-rendered pages)

How to run it locally:

1) Run "git clone https://github.com/shiv9476t/grad-track" in terminal
2) Run "pip install -r requirements.txt" in terminal
3) Run "python3 registry.py" in terminal to setup database and run the scrapers to populate the database
4) Run "python3 app.py" in terminal
5) Search "http://localhost:5000" in browser

Project structure:

app.py - creates the backend API using Flask
classifier.py - classifies grad schemes by industry
database.py - contains database class for creating database, its tables, and its SQL functions
models/grad_scheme.py - contains GradScheme class for defining structure
registry.py - contains registry of scrapers and function to run all scrapers and upsert into the database
scrape.py - calls registry.py function
scrapers/ - contains base class for scrapers, and company-specific scrapers, to fetch and parse HTML and JSON
templates/index.html - contains HTML, Tailwind CSS and Javascript for UI

Roadmap:

1) Testing
2) Personalised recommendation system using ML
3) Option for email alerts when matching roles open
4) Analytics dashboard
5) Social media feature, to connect similar users