# fetch_data.py

import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

def safe_find(driver, by, selector):
    """Try to find an element. If missing, return None."""
    try:
        return driver.find_element(by, selector)
    except NoSuchElementException:
        return None

def fetch_jira_story_data(driver, story_url):
    time.sleep(15)
    driver.get(story_url)
    time.sleep(30)

    print("✅ Redirected")

    time.sleep(20)


   # Extract required fields
    selectors = {
        "title": '[data-testid="issue.views.issue-base.foundation.summary.heading"]',
        "storyID": '[data-testid="issue.views.issue-base.foundation.breadcrumbs.current-issue.item"]',
        "reporter": '[data-testid="profilecard-next.ui.profilecard.profilecard-trigger"]',
        "affectVersion": '[data-testid="issue.views.field.single-line-text.read-view.customfield_10061"]',
        "fixedVersion": '[data-testid="issue.views.field.single-line-text.read-view.customfield_10059"]',
        "epic": '[data-testid="issue-field-parent.ui.view-link"]',
        "status": '[data-testid="issue-field-status.ui.status-view.status-button.status-button"]',
        "assignee": '[data-testid="issue.views.field.user.assignee"]',
        "dueDate": '[data-testid="coloured-due-date.ui.colored-due-date-container"]',
        "startDate": '[data-testid="issue-field-date.ui.issue-field-date--container"]',
        "label": '[data-testid="issue.views.issue-base.context.labels"] a',
        "storyPoints": '[data-testid="issue-field-story-point-estimate-readview-full.ui.story-point-estimate"]',
        "acceptanceCriteria": '[data-testid="issue.views.field.rich-text.customfield_10060"]',
        "description": '[data-testid="issue.views.field.rich-text.description"]',
        "teamName": '[data-testid="issue-field-team.ui.view-team-name"]'
    }

    elems = {}
    for key, selector in selectors.items():
        elems[key] = safe_find(driver, By.CSS_SELECTOR, selector)

    # --- Subtasks ---
    issue_table = safe_find(driver, By.CSS_SELECTOR, '[data-vc="issue-table"]')
    rows = issue_table.find_elements(By.CSS_SELECTOR, 'tr')
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
                    pass

    subTasks = "Not Completed" if incomplete_issue_keys else "Done"
    incomplete_issue_keys_str = ", ".join(incomplete_issue_keys)

    # --- Linked Issues ---
    container = safe_find(driver, By.CSS_SELECTOR, '[data-testid="issue.views.issue-base.content.issue-links.group-container"]')
    uls = container.find_elements(By.CSS_SELECTOR, 'div[role="listitem"]')
    incomplete_linked_issues = []

    for ul in uls:
        try:
            status_el = ul.find_element(By.CSS_SELECTOR, '[data-testid="issue-line-card.ui.status.status-field-container"]')
            key_el = ul.find_element(By.CSS_SELECTOR, '[data-testid="issue.issue-view.views.common.issue-line-card.issue-line-card-view.key"]')
            if status_el.text.strip().upper() != "DONE":
                incomplete_linked_issues.append(key_el.text.strip())
        except:
            pass

    linkedIssues = "Not Completed" if incomplete_linked_issues else "Done"
    incomplete_linked_issues_str = ", ".join(incomplete_linked_issues)

    # --- Clean text using JS ---
    js = driver.execute_script
    data = [
        elems["storyID"].text,
        js("return arguments[0].textContent;", elems["status"]),
        elems["title"].text,
        elems["assignee"].text,
        js("return arguments[0].textContent;", elems["reporter"]),
        elems["dueDate"].text,
        js("return arguments[0].textContent;", elems["affectVersion"]),
        js("return arguments[0].textContent;", elems["fixedVersion"]),
        elems["storyPoints"].text,
        elems["label"].text,
        js("return arguments[0].textContent;", elems["acceptanceCriteria"]),
        js("return arguments[0].textContent;", elems["description"]),
        js("return arguments[0].textContent;", elems["teamName"]),
        js("return arguments[0].href;", elems["epic"]),
        subTasks,
        incomplete_issue_keys_str,
        linkedIssues,
        incomplete_linked_issues_str
    ]

    return data
