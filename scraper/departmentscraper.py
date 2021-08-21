from selenium import webdriver
from selenium.webdriver.common.by import By

import logging

from settings import DEPARTMENT_URL


class DepartmentScraper:

    def __init__(self, driver_path: str, dept_url: str):
        # Start up the browser TODO: add a driver directory
        self.browser = webdriver.Firefox(executable_path=driver_path)
        self.dept_url = dept_url

    def scrape(self, out=print):
        self.browser.get(self.dept_url)
        departments = self.browser.find_element(By.ID, "selectedSubjects") \
            .find_elements(By.TAG_NAME, "option")
        for department in departments:
            department_data = self.__normalize_department(department.text)
            logging.info("Department %s added" % str(department_data))
            out(department_data)
        self.browser.close()

    def __normalize_department(dept: str):
        data = dept.split(" - ")
        return data[0].strip(), data[1].strip()
