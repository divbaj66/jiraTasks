from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from openpyxl import load_workbook
import time

from assets.login import driver, login
# ---- CONFIG ----


# ---- SETUP ----
options = Options()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=options)

try:
    login()
    print("✅ Redirect to jira story!")

    # 5️⃣ Open a Jira board or issue
    driver.get("https://jiraautomation.atlassian.net/browse/JA-4")
    time.sleep(30)

    print("✅ Redirected")

    time.sleep(20)

    # let the dtaa be fetched

    # get the data from the page
    title = driver.find_element(By.CSS_SELECTOR, '[data-testid="issue.views.issue-base.foundation.summary.heading"]')
    storyID = driver.find_element(By.CSS_SELECTOR, '[data-testid="issue.views.issue-base.foundation.breadcrumbs.current-issue.item"]')
    reporter = driver.find_element(By.CSS_SELECTOR, '[data-testid="profilecard-next.ui.profilecard.profilecard-trigger"]')
    affectVersion = driver.find_element(By.CSS_SELECTOR, '[data-testid="issue.views.field.single-line-text.read-view.customfield_10061"]')
    fixedVersion = driver.find_element(By.CSS_SELECTOR, '[data-testid="issue.views.field.single-line-text.read-view.customfield_10059"]')
    epic = driver.find_element(By.CSS_SELECTOR, '[data-testid="issue-field-parent.ui.view-link"]')
    assignee = driver.find_element(By.CSS_SELECTOR, '[data-testid="issue.views.field.user.assignee"]')
    dueDate = driver.find_element(By.CSS_SELECTOR, '[data-testid="coloured-due-date.ui.colored-due-date-container"]')
    startDate = driver.find_element(By.CSS_SELECTOR, '[data-testid="issue-field-date.ui.issue-field-date--container"]')
    label = driver.find_element(By.CSS_SELECTOR, '[data-testid="issue.views.issue-base.context.labels"] a')
    storyPoints = driver.find_element(By.CSS_SELECTOR, '[data-testid="issue-field-story-point-estimate-readview-full.ui.story-point-estimate"]')
    acceptanceCriteria = driver.find_element(By.CSS_SELECTOR, '[data-testid="issue.views.field.rich-text.customfield_10060"]')
    description = driver.find_element(By.CSS_SELECTOR, '[data-testid="issue.views.field.rich-text.description"]')
    teamName = driver.find_element(By.CSS_SELECTOR, '[data-testid="issue-field-team.ui.view-team-name"]')
    
    # fetching the in-complete sub-tasks
    # Step 1: Find the table
    issue_table = driver.find_element(By.CSS_SELECTOR, '[data-vc="issue-table"]')

    # Step 2: Get all <tr> rows
    rows = issue_table.find_elements(By.CSS_SELECTOR, 'tr')

    # Step 3: Loop through rows and collect keys where 4th <td> is not DONE
    incomplete_issue_keys = []
    for row in rows:
        tds = row.find_elements(By.CSS_SELECTOR, 'td')
        if len(tds) >= 4:
            status = tds[3].text.strip().upper()
            if status != "DONE":
                try:
                    issue_key_elem = tds[0].find_element(By.CSS_SELECTOR, '[data-vc="native-issue-table-ui-issue-key-cell"]')
                    issue_key = issue_key_elem.text.strip()
                    incomplete_issue_keys.append(issue_key)
                except:
                    pass  # if the cell isn't found, skip it
    incomplete_issue_keys_str = ", ".join(incomplete_issue_keys)
    subTasks = "Not Completed" if incomplete_issue_keys else "Done"
    
    # Step 1: Get the container element
    container = driver.find_element(By.CSS_SELECTOR, '[data-testid="issue.views.issue-base.content.issue-links.group-container"]')

    # Step 2: Get all <ul> elements inside it
    uls = container.find_elements(By.TAG_NAME, 'ul')

    # Step 3: Loop and collect issue keys with status != 'DONE'
    incomplete_linked_issues = []

    for ul in uls:
        try:
            # Get status element and issue key element
            status_el = ul.find_element(By.CSS_SELECTOR, '[data-testid="issue-line-card.ui.status.status-field-container"]')
            key_el = ul.find_element(By.CSS_SELECTOR, '[data-testid="issue.issue-view.views.common.issue-line-card.issue-line-card-view.key"]')

            # Clean and compare status
            status = status_el.text.strip().upper()
            if status != "DONE":
                issue_key = key_el.text.strip()
                incomplete_linked_issues.append(issue_key)

        except Exception as e:
            # Optional: print or log exception
            pass  # If elements are missing in any <ul>, skip it

    # Step 4: Convert the list to a comma-separated string for Excel, if needed
    incomplete_linked_issues_str = ", ".join(incomplete_linked_issues)
    
    linkedIssues = "Not Completed" if incomplete_linked_issues else "Done"

    
#     data = [
#         {"Title": title.text, 
#          "Epic": epic.text, 
#          "Assignee": assignee.text, 
#          "DueDate": dueDate.text, 
#          "StartDate": startDate.text, 
#          "Label": label.text,
#          "StoryPoints": storyPoints.text }
# ]
    reporterText = driver.execute_script("return arguments[0].textContent;", reporter)
    affectVersionText = driver.execute_script("return arguments[0].textContent;", affectVersion)
    fixedVersionText = driver.execute_script("return arguments[0].textContent;", fixedVersion)
    acceptanceCriteriaText = driver.execute_script("return arguments[0].textContent;", acceptanceCriteria)
    descriptionText = driver.execute_script("return arguments[0].textContent;", description)
    teamNameText = driver.execute_script("return arguments[0].textContent;", teamName)
    epicText = driver.execute_script("return arguments[0].textContent;", epic)
    data = [
        [storyID.text, 
         title.text, 
         assignee.text, 
         reporterText, 
         dueDate.text, 
         affectVersionText,
         fixedVersionText, 
         storyPoints.text,
         label.text,
         acceptanceCriteriaText,
         descriptionText,
         teamNameText,
         epicText,
         subTasks,
         incomplete_issue_keys_str,
         linkedIssues,
         incomplete_linked_issues_str
        ]
]
    # print("Title:", title.text)
    # print("Epic:", epic.text)
    # print("Assignee:", assignee.text)
    # print("DueDate:", dueDate.text)
    # print("StartDate:", startDate.text)
    # print("Label:", label.text)
    # print("StoryPoints:", storyPoints.text)
    

    # File path of the excel
    excelPath = 'dod_report.xlsx'
    

    # Write headers
    workbook = load_workbook(excelPath)
    sheet = workbook["DOD Staging"]

    # Write data rows
    for row in data:
        sheet.append(row)

    # Save the file
    workbook.save(excelPath)


#Next step will be to log the data in a excel and match the criteria
#with DOD expectation

    time.sleep(5)  # just to see the page

finally:
    driver.quit()

