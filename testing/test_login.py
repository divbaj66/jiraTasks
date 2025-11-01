# ...existing code...
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import types
from unittest.mock import Mock
import builtins
import pytest

import login as login_module

def test_login_to_jira_uses_driver_and_clicks(monkeypatch, capsys):
    # Prepare fake credentials and no-op sleep
    monkeypatch.setattr(login_module, "JIRA_URL", "http://jira.test")
    monkeypatch.setattr(login_module, "USERNAME", "user1")
    monkeypatch.setattr(login_module, "PASSWORD", "pass1")
    monkeypatch.setattr(login_module, "time", types.SimpleNamespace(sleep=lambda _s: None))

    # Mock webdriver.Chrome to return a mock driver
    mock_driver = Mock()
    mock_driver.get = Mock()
    # driver.find_element should return a mock with click
    login_button = Mock()
    login_button.click = Mock()
    mock_driver.find_element = Mock(return_value=login_button)

    # Track send_keys calls from WebDriverWait.until(...)
    class MockElement:
        def __init__(self):
            self.send_keys = Mock()

    # Replace WebDriverWait in module with a dummy that returns an object with until()
    class DummyWait:
        def __init__(self, driver, timeout):
            pass
        def until(self, condition):
            return MockElement()

    monkeypatch.setattr(login_module, "webdriver", types.SimpleNamespace(Chrome=lambda **kwargs: mock_driver))
    monkeypatch.setattr(login_module, "WebDriverWait", DummyWait)

    # Run login
    driver_returned = login_module.login_to_jira()

    # Assertions
    mock_driver.get.assert_called_with("http://jira.test")
    # driver.find_element (login button) should be clicked twice (after username and after password)
    assert mock_driver.find_element.call_count >= 2
    assert driver_returned is mock_driver

    captured = capsys.readouterr()
    assert "✅ Logged in successfully!" in captured.out