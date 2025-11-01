# test_main.py
import os
import sys

# Ensure the package root (parent dir containing main.py) is on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import importlib
import types
from unittest.mock import Mock
import pytest

# Import main.py directly from the project root
import main as main_module
from main import main

def test_main_runs_and_writes_excel(monkeypatch, capsys):
    # Arrange
    mock_driver = Mock()
    mock_driver.quit = Mock()

    test_stories = ["http://test/story/1", "http://test/story/2"]

    def fetch_stub(driver, url):
        return {"story": url}

    write_mock = Mock()

    # Patch module-level dependencies
    monkeypatch.setattr(main_module, "login_to_jira", lambda: mock_driver)
    monkeypatch.setattr(main_module, "fetch_jira_story_data", fetch_stub)
    monkeypatch.setattr(main_module, "write_to_excel", write_mock)
    monkeypatch.setattr(main_module, "JIRA_STORIES", test_stories)
    monkeypatch.setattr(main_module, "time", types.SimpleNamespace(sleep=lambda _s: None))

    # Act
    main()

    # Assert
    expected_data = [{"story": test_stories[0]}, {"story": test_stories[1]}]
    write_mock.assert_called_once_with("dod_report_2.xlsx", expected_data)
    mock_driver.quit.assert_called_once()

    captured = capsys.readouterr()
    assert "🚪 Browser closed" in captured.out

def test_main_ensures_driver_quit_on_exception(monkeypatch):
    # Arrange
    mock_driver = Mock()
    mock_driver.quit = Mock()

    test_stories = ["http://test/story/1", "http://test/story/2"]

    def fetch_maybe_raise(driver, url):
        if url == test_stories[1]:
            raise RuntimeError("fetch failed")
        return {"story": url}

    write_mock = Mock()

    # Patch
    monkeypatch.setattr(main_module, "login_to_jira", lambda: mock_driver)
    monkeypatch.setattr(main_module, "fetch_jira_story_data", fetch_maybe_raise)
    monkeypatch.setattr(main_module, "write_to_excel", write_mock)
    monkeypatch.setattr(main_module, "JIRA_STORIES", test_stories)
    monkeypatch.setattr(main_module, "time", types.SimpleNamespace(sleep=lambda _s: None))

    # Act & Assert: exception should propagate, but driver.quit must still be called
    with pytest.raises(RuntimeError):
        main()

    mock_driver.quit.assert_called_once()
    write_mock.assert_not_called()