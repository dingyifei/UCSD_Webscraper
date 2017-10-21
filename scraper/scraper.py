import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from settings import HTML_STORAGE, HOME_DIR, WEBREG_URL, MANUAL_MODE, TIMEOUT, DEPARTMENTS, CLASS_SEARCH_TIMEOUT


class Scraper:
    def __init__(self, username=None, password=None):
        # Go to web browser directory
        os.chdir(os.path.join(HOME_DIR, "driver"))

        # Keeping track of HTML directory
        self.dir_path = None
        self.login_url = WEBREG_URL

        # Take input manually if does not come from the GUI
        if not username and not password:
            # Check if can enter information manually
            if MANUAL_MODE:
                self.username = input('Enter your username')
                self.password = input('Enter your password')
            else:
                raise IOError("You must put in a username and password!")
        else:
            self.username = username
            self.password = password

        self.browser = webdriver.Chrome()
        self.browser.set_page_load_timeout(TIMEOUT)

        os.chdir(HOME_DIR)

    def scrape(self):
        self.login()
        self.pick_quarter()
        self.iter_departments()

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
            submit = WebDriverWait(self.browser, TIMEOUT).until(EC.presence_of_element_located(
                (By.ID, 'startpage-button-go')
            ))
            while self.browser.find_element_by_id('startpage-button-go'):
                submit = self.browser.find_element_by_id('startpage-button-go')
                submit.click()
        except Exception:
            pass

    def iter_departments(self):
        for department in DEPARTMENTS:
            self.search_department(department)
            self.iter_pages()
            print('I should be moving to the next department now.')

    def search_department(self, department):
        self.dir_path = os.path.join(HTML_STORAGE, department)
        try:
            class_search = WebDriverWait(self.browser, TIMEOUT).until(EC.presence_of_element_located
                                                                      ((By.ID, 's2id_autogen1')))
            class_search.click()
            class_search.send_keys(department)
            class_search.send_keys(Keys.RETURN)

        except Exception as e:
            print(e)
            pass

    def iter_pages(self):
        # now I should be at the course pages
        page_ul = WebDriverWait(self.browser, TIMEOUT).until(EC.presence_of_element_located
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
                    class_search = WebDriverWait(self.browser, CLASS_SEARCH_TIMEOUT).until(
                        EC.presence_of_element_located(
                            (By.CLASS_NAME, 'ui-icon-circlesmall-plus')
                        )
                    )
                    class_search.click()
            except Exception:
                print('I should be moving to the next page now.')
                html = self.browser.page_source
                self.store_page(html, page.text)
                pass

    def store_page(self, page_contents, num_str):
        if not os.path.exists(self.dir_path):
            os.makedirs(self.dir_path)

        file = open(os.path.join(self.dir_path, num_str + '.html'), 'w')
        file.write(page_contents)
        print(file.name)
        file.close()
