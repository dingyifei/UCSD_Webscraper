import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from settings import HTML_STORAGE
from settings import DEPARTMENT


class Scraper:
    def __init__(self):
        os.chdir('C:/Users/ctran/Downloads/chromedriver')

        self.dir_path = None
        self.login_url = 'https://act.ucsd.edu/webreg2/start'
        self.username = input('Enter your username')
        self.password = input('Enter your password')

        self.browser = webdriver.Chrome()
        self.browser.set_page_load_timeout(30)

        os.chdir('C:/Users/ctran/PycharmProjects/UCSD_Webscraper')

    def scrape(self):
        self.login()
        self.pick_quarter()
        self.search_department()
        self.iter_pages()

    def login(self):
        self.browser.get(self.login_url)
        self.browser.find_element_by_id('ssousername').send_keys(self.username)
        self.browser.find_element_by_id('ssopassword').send_keys(self.password)
        try:
            self.browser.find_element_by_class_name('sso-button').submit()
        except Exception:
            pass

    def pick_quarter(self):
        try:
            submit = WebDriverWait(self.browser, 200).until(EC.presence_of_element_located(
                (By.ID, 'startpage-button-go')
            ))
            while self.browser.find_element_by_id('startpage-button-go'):
                submit = self.browser.find_element_by_id('startpage-button-go')
                submit.click()
        except Exception:
            pass

    def search_department(self):
        self.dir_path = os.path.join(HTML_STORAGE, DEPARTMENT)
        try:
            class_search = WebDriverWait(self.browser, 200).until(EC.presence_of_element_located
                                                                  ((By.ID, 's2id_autogen1')))
            class_search.click()
            class_search.send_keys(DEPARTMENT)
            class_search.send_keys(Keys.RETURN)

        except Exception as e:
            print(e)
            pass

    def iter_pages(self):
        # now I should be at the course pages
        page_ul = WebDriverWait(self.browser, 200).until(EC.presence_of_element_located
                                                         ((By.CLASS_NAME, 'jPag-pages')))
        pages = page_ul.find_elements_by_tag_name('li')
        for page in pages:
            current = self.browser.find_element_by_class_name('jPag-current').text
            print(current)
            print(page.text)
            if int(page.text) == int(current) + 1:
                page.click()
                print("Have clicked page", page.text)
            try:
                while True:
                    class_search = WebDriverWait(self.browser, 10).until(EC.presence_of_element_located
                                                                         ((By.CLASS_NAME, 'ui-icon-circlesmall-plus')))
                    class_search.click()
            except Exception:
                print('I should be moving to the next page now.')
                html = self.browser.page_source
                self.add_page(html, page.text)
                pass

    def add_page(self, page_contents, num_str):
        if not os.path.exists(self.dir_path):
            os.makedirs(self.dir_path)

        file = open(os.path.join(self.dir_path, num_str + '.html'), 'w')
        file.write(page_contents)
        print(file.name)
        file.close()
