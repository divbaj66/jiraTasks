# ...existing code...
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import types
from unittest.mock import Mock
import pytest

import fetch_data as fd

def make_elem(text="", href=None):
    m = Mock()
    m.text = text
    if href is not None:
        m.href = href
    # For elements that will be passed to execute_script, keep identity
    return m

def test_fetch_jira_story_data_parses_elements(monkeypatch):
    # No real sleeping
    monkeypatch.setattr(fd, "time", types.SimpleNamespace(sleep=lambda _s: None))

    # Build a fake driver with required methods
    driver = Mock()
    driver.get = Mock()

    # execute_script should return textContent / href values when asked
    def execute_script(script, elem):
        # If script asks for href
        if "href" in script:
            return getattr(elem, "href", "")
        return getattr(elem, "text", "")
    driver.execute_script = Mock(side_effect=execute_script)

    # Prepare elements used in selectors
    elems = {
        "storyID": make_elem("JA-123"),
        "status": make_elem("In Progress"),
        "title": make_elem("Story title"),
        "assignee": make_elem("AssigneeName"),
        "reporter": make_elem("ReporterName"),
        "dueDate": make_elem("2025-11-01"),
        "affectVersion": make_elem("v1"),
        "fixedVersion": make_elem("v2"),
        "storyPoints": make_elem("5"),
        "label": make_elem("label1"),
        "acceptanceCriteria": make_elem("AC text"),
        "description": make_elem("Desc text"),
        "teamName": make_elem("Team A"),
        "epic": make_elem("", href="http://epic/EPIC-1"),
    }

    # safe_find is used for many selectors; return corresponding mocks for keys used
    def fake_safe_find(driver_arg, by, selector):
        # map selectors to our elems by checking substrings
        if "summary.heading" in selector:
            return elems["title"]
        if "current-issue" in selector:
            return elems["storyID"]
        if "profilecard" in selector:
            return elems["reporter"]
        if "customfield_10061" in selector:
            return elems["affectVersion"]
        if "customfield_10059" in selector:
            return elems["fixedVersion"]
        if "issue-field-parent" in selector or "view-link" in selector:
            return elems["epic"]
        if "status-button" in selector:
            return elems["status"]
        if "assignee" in selector:
            return elems["assignee"]
        if "coloured-due-date" in selector:
            return elems["dueDate"]
        if "issue-field-date" in selector:
            return elems["startDate"] if "startDate" in locals() else None
        if "labels" in selector:
            return elems["label"]
        if "story-point-estimate" in selector:
            return elems["storyPoints"]
        if "customfield_10060" in selector:
            return elems["acceptanceCriteria"]
        if "description" in selector:
            return elems["description"]
        if "view-team-name" in selector:
            return elems["teamName"]
        if 'issue-table' in selector:
            # Create a fake table with one row where status is DONE
            row_td0 = Mock()
            row_td0.find_element = Mock(return_value=make_elem("ISSUE-1"))
            td1 = Mock(); td2 = Mock()
            td3 = make_elem("DONE")
            row = Mock()
            row.find_elements = Mock(return_value=[row_td0, td1, td2, td3])
            table = Mock()
            table.find_elements = Mock(return_value=[row])
            return table
        if 'issue-links.group-container' in selector:
            # No linked issues to be incomplete
            ul = Mock()
            status_el = make_elem("DONE")
            key_el = make_elem("LINK-1")
            ul.find_element = Mock(side_effect=lambda by, sel: status_el if "status-field-container" in sel else key_el)
            return Mock(find_elements=Mock(return_value=[ul]))
        return None

    # Patch safe_find in module
    monkeypatch.setattr(fd, "safe_find", fake_safe_find)
    # Attach execute_script and get to driver
    driver.execute_script = Mock(side_effect=execute_script)

    result = fd.fetch_jira_story_data(driver, "http://dummy/story")
    # Validate result is list and contains some expected items
    assert isinstance(result, list)
    assert "JA-123" in result[0]  # storyID present
    assert "In Progress" in result[1] or "In Progress" in result[1]  # status in cleaned text
    assert "Story title" in result[2]