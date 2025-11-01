# main.py

from login import login_to_jira
from fetch_data import fetch_jira_story_data
from write_excel import write_to_excel
from jira_links import JIRA_STORIES
import time

def main():
    driver = login_to_jira()

    try:
        all_data = []
        for story_url in JIRA_STORIES:
            data = fetch_jira_story_data(driver, story_url)
            all_data.append(data)
            time.sleep(5)

        # Save to Excel
        write_to_excel("dod_report_2.xlsx", all_data)

      
        

    finally:
        driver.quit()
        print("🚪 Browser closed")

if __name__ == "__main__":
    main()
