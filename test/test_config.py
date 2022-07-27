import tempfile

from src.utility.config import get_config, DEFAULT_SELENIUM_CONFIG, DEFAULT_CHROME_CONFIG


def create_temp_file(content: bytes = b"") -> str:
    """
    Create a temp file with a content, then returns the name got from OS
    """

    with tempfile.NamedTemporaryFile("wb", delete=False) as f:
        f.write(content)
    return f.name


def create_text_temp_file(text: str, encoding="utf-8") -> str:
    """
    Create a temp file with a string as input (defaults to utf-8 charset)
    """

    with tempfile.NamedTemporaryFile("w", encoding=encoding, delete=False) as f:
        f.write(text)
    return f.name


def test_config():
    cfg_as_text = """
[selenium]
headless=true

[chrome]
profile_root = /path/
"""
    cfg_filename = create_text_temp_file(text=cfg_as_text)
    config = get_config(cfg_fp=cfg_filename)

    assert config.selenium.headless
    assert config.selenium.logging is DEFAULT_SELENIUM_CONFIG.logging

    assert config.chrome.profile_root == "/path/"
    assert config.chrome.profile is DEFAULT_CHROME_CONFIG.profile
