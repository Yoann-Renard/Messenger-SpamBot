from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import json
#import pandas as pd
import time
import threading
import os
from dotenv import load_dotenv
load_dotenv()

StartTime = time.time()

## INITIALISATION ##

print("Driver init...")

#executable = "chromedriver.exe"
executable = "chromedriver"
path = os.path.join("bin", executable)
#Options
chrome_options = Options()

"""Sans notif"""
chrome_options.add_argument('disable-notifications')

"""Affichage des images"""
"""chrome_prefs = {}
chrome_options.experimental_options["prefs"] = chrome_prefs
chrome_prefs["profile.default_content_settings"] = {"images": 2}
chrome_prefs["profile.managed_default_content_settings"] = {"images": 2}"""

"""Sans GUI"""
chrome_options.add_argument("--headless")

"""Driver & links"""
driver = webdriver.Chrome(path, options=chrome_options)
url_insta = 'https://www.instagram.com/?hl=fr'
url_facebook = 'https://www.facebook.com/'


class Instagram():
    """docstring for Instagram."""

    username = ''
    email = ''
    password = ''

    def __init__(self, user):
        pass

    def searchUser(self, user_to_search):
        cookieButton = driver.find_elements_by_class_name('aOOlW')
        cookieButton[0].click()
        ##
        WaitFor(EC.element_to_be_clickable,  By.CSS_SELECTOR,
                'input[aria-label="Num. téléphone, nom d’utilisateur ou e-mail"]', 10)
        driver.find_element_by_css_selector(
            'input[aria-label="Num. téléphone, nom d’utilisateur ou e-mail"]').send_keys(self.username)
        driver.find_element_by_css_selector(
            'input[ aria-label="Mot de passe" ]').send_keys(self.password + '\n')
        ##
        WaitFor(EC.element_to_be_clickable,  By.CSS_SELECTOR,
                'input[autocapitalize="none"]', 10)
        Search = driver.find_element_by_css_selector(
            'input[autocapitalize="none"]').send_keys(user_to_search)


class Facebook():
    """docstring for Facebook."""

    username = ''
    email = ''
    password = ''
    connected = False

    def __init__(self):
        """
        try:
            f = open('IDs_' + user + '.json', 'r')
            log = json.loads(f.read())
        except Exception as e:
            print(e)
            print('this user does not exist')
            driver.quit()
        else:
            self.email = log["Email"]
            self.password = log["Facebook_password"]
            self.username = user
        finally:
            f.close()
        """

        driver.get(url_facebook)
        try:
            self.username = os.environ["FB_USER"]
            self.email = os.environ["FB_EMAIL"]
            self.password = os.environ["FB_PASS"]
        except KeyError:
            print("FB_USER/FB_EMAIL/FB_PASS must be set as envrionment variable or written in a .env file.")
            exit(1)

    def connection(self):
        print("Connecting to facebook...")
        if self.connected:
            print(f"{self.username} is already connected")
        else:
            cookieButton = driver.find_element_by_css_selector(
                'button[data-cookiebanner="accept_button"]')
            cookieButton.click()
            ##
            WaitFor(EC.element_to_be_clickable,  By.NAME, 'email', 10)
            driver.find_element_by_name('email').send_keys(self.email)
            driver.find_element_by_name('pass').send_keys(self.password + '\n')
            ##
            self.connected = True

    def isConnected(self):
        if self.connected:
            return True
        else:
            print(f"{self.username} is not connected")
            return False

    def searchUser(self, user_to_search):
        if self.isConnected():
            WaitFor(EC.element_to_be_clickable,
                    By.CSS_SELECTOR, 'input[type="search"]', 10)
            Search = driver.find_element_by_css_selector(
                'input[type="search"]').send_keys(user_to_search)

    def sendMessage(self, user_to_dm, message_to_send, is_friend):
        if is_friend:
            WaitFor(EC.element_to_be_clickable, By.CSS_SELECTOR,
                    'div[aria-label="Messenger"]', 10)
            open_messenger_button = driver.find_element_by_css_selector(
                'div[aria-label="Messenger"]')
            open_messenger_button.click()
            print("Waiting for messenger...")
            WaitFor(EC.element_to_be_clickable, By.CSS_SELECTOR,
                    'input[aria-label="Rechercher dans Messenger"]', 10)
            search_bar = driver.find_element_by_css_selector(
                'input[aria-label="Rechercher dans Messenger"]')
            WaitFor(EC.presence_of_element_located,
                    By.CSS_SELECTOR, 'div[aria-label="Discussions"]', 10)
            print("Searching for user...")
            search_bar.send_keys(user_to_dm)
            WaitFor(EC.presence_of_element_located,
                    By.CSS_SELECTOR, 'ul li ul li', 10)
            first_result = driver.find_elements_by_css_selector('ul li ul li')
            first_result[0].click()
            WaitFor(EC.presence_of_element_located,
                    By.CSS_SELECTOR, 'div[aria-label="Écrire un message"]', 10)
            driver.find_element_by_css_selector(
                'div[aria-label="Écrire un message"]').send_keys(message_to_send + '\n')

    def goToMainPage(self):
        if self.isConnected():
            driver.find_element_by_tag_name('body').send_keys(Keys.ESCAPE)

            WaitFor(EC.element_to_be_clickable, By.CSS_SELECTOR, 'svg', 10)
            driver.find_element_by_tag_name('svg').click()


class setInterval:
    def __init__(self, interval, action):
        self.interval = interval
        self.action = action
        self.stopEvent = threading.Event()
        thread = threading.Thread(target=self.__setInterval)
        thread.start()

    def __setInterval(self):
        nextTime = time.time()+self.interval
        while not self.stopEvent.wait(nextTime-time.time()):
            nextTime += self.interval
            self.action()

    def cancel(self):
        self.stopEvent.set()


def WaitFor(methode, selector_type, element, timeout):
    try:
        # wait for search results to be fetched
        WebDriverWait(driver, timeout).until(
            methode((selector_type, element))
        )
    except Exception as e:
        print(e)
        driver.quit()


def CloseFirstTab():
    """Close first tab if required"""
    try:
        driver.switch_to.window(driver.window_handles[0])
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
    except Exception:
        print("CloseFirstTab() error : First tab can't be closed")
