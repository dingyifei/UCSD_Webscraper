from selenium import webdriver
from selenium.webdriver.common.by import By
import os
import sqlite3
import logging

from settings import HOME_DIR
from settings import DEPARTMENT_URL
from settings import DATABASE_PATH


class DepartmentScraper:

    def __init__(self):
        # Start up the browser TODO: add a driver directory
        self.browser = webdriver.Firefox(executable_path=os.path.join(HOME_DIR, "driver/geckodriver.exe"))

        # Establish database connection under the assumption the sqlite db exist
        self.database = sqlite3.connect(DATABASE_PATH)
        self.database.row_factory = sqlite3.Row
        self.cursor = self.database.cursor()
        logging.info("Database connected")

    def create_table(self):
        self.cursor.execute('DROP TABLE IF EXISTS department')
        self.cursor.execute(
            'CREATE TABLE IF NOT EXISTS department ('
            'dept_id integer primary key AUTOINCREMENT,'
            'dept_code TEXT NOT NULL,'
            'dept_description TEXT,'
            'UNIQUE(dept_id, dept_code)'
            ')')
        self.cursor.execute(
            'CREATE TABLE IF NOT EXISTS update_tracker ('
            'name TEXT NOT NULL,'
            'last_update TIMESTAMP,'
            'UNIQUE(name)'
            ')')
        self.cursor.execute(
            "INSERT OR IGNORE INTO update_tracker(name, last_update) VALUES('department', CURRENT_TIMESTAMP)"
        )
        self.cursor.execute(
            "UPDATE update_tracker SET last_update=CURRENT_TIMESTAMP WHERE name='department'"
        )

    def scrape(self):
        self.create_table()
        self.search()
        self.get_departments()
        self.close()

    def search(self):
        self.browser.get(DEPARTMENT_URL)

    def get_departments(self):
        departments = self.browser.find_element(By.ID, "selectedSubjects") \
            .find_elements(By.TAG_NAME, "option")
        for department in departments:
            department_data=self.__normalize_department(department.text)
            logging.info("Department %s added" % str(department_data))
            self.cursor.execute(
                'INSERT INTO department(dept_code, dept_description) VALUES(?, ?)',
                department_data
            )

    def __normalize_department(self, department:str):
        data = department.split(" - ")
        return data[0].strip(),data[1].strip()

    def close(self):
        self.database.commit()
        self.database.close()
        self.browser.close()
