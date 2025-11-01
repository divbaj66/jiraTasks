# login.py

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from credentials import JIRA_URL, USERNAME, PASSWORD


def login_to_jira():
    options = Options()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)

    driver.get(JIRA_URL)

    # Enter username
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "username-uid1"))
    ).send_keys(USERNAME)
    time.sleep(5)
    driver.find_element(By.ID, "login-submit").click()

    time.sleep(10)

    # Enter password
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "password"))
    ).send_keys(PASSWORD)

    time.sleep(5)
    driver.find_element(By.ID, "login-submit").click()

    time.sleep(5)
    print("✅ Logged in successfully!")

    return driver
