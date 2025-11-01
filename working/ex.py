from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
# ---- CONFIG ----
JIRA_URL = "https://id.atlassian.com/login"
USERNAME = "jiratasks657@gmail.com"
PASSWORD = "SomeRandomPassword@1"

# ---- SETUP ----
options = Options()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=options)

try:
    # 1️⃣ Go to Jira login page
    driver.get(JIRA_URL)

    # 2️⃣ Enter email & click Continue
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "username-uid1"))
    ).send_keys(USERNAME)
    time.sleep(5)
    driver.find_element(By.ID, "login-submit").click()

    time.sleep(10)

    # 3️⃣ Wait for password field & enter password
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "password"))
    ).send_keys(PASSWORD)

    time.sleep(5)
    driver.find_element(By.ID, "login-submit").click()

    time.sleep(5)

    print("✅ Logged in successfully!")

    time.sleep(15)

    print("✅ Redirect to jira story!")

    # 5️⃣ Open a Jira board or issue
    driver.get("https://jiraautomation.atlassian.net/browse/JA-5")
    time.sleep(30)

    print("✅ Redirected")

    time.sleep(20)

    # let the dtaa be fetched

    # get the data from the page
    title = driver.find_element(By.CSS_SELECTOR, '[data-testid="issue.views.issue-base.foundation.summary.heading"]')
    epic = driver.find_element(By.CSS_SELECTOR, '[data-testid="issue-field-parent.ui.view-link"]')
    assignee = driver.find_element(By.CSS_SELECTOR, '[data-testid="issue.views.field.user.assignee"]')
    dueDate = driver.find_element(By.CSS_SELECTOR, '[data-testid="coloured-due-date.ui.colored-due-date-container"]')
    startDate = driver.find_element(By.CSS_SELECTOR, '[data-testid="issue-field-date.ui.issue-field-date--container"]')
    label = driver.find_element(By.CSS_SELECTOR, '[data-testid="issue-field-inline-edit-read-view-container.ui.container"]')
    storyPoints = driver.find_element(By.CSS_SELECTOR, '[data-testid="issue-field-story-point-estimate-readview-full.ui.story-point-estimate"]')
    print("Title:", title.text)
    print("Epic:", epic.text)
    print("Assignee:", assignee.text)
    print("DueDate:", dueDate.text)
    print("StartDate:", startDate.text)
    print("Label:", label.text)
    print("StoryPoints:", storyPoints.text)


#Next step will be to log the data in a excel and match the criteria
#with DOD expectation

    time.sleep(5)  # just to see the page

finally:
    driver.quit()

