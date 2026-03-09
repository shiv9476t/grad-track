from registry import run_all
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

logging.info("Starting scrape run")
run_all()
logging.info("Scrape run complete")