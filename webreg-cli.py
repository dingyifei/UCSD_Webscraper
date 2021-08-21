from scraper.departmentscraper import DepartmentScraper
import logging

logging.basicConfig(filename='cli.log', level=logging.INFO)
logging.info('Started')
print("This is a experimental command line interface."
      "press 1 to scrape departments.")
answer = input("input")
if int(answer) == 1:
    logging.info("Scraping department")
    dept_scraper = DepartmentScraper()
    dept_scraper.scrape()
    logging.info("Successful")
