from selenium import webdriver

from utility.config import Config
from utility.options import get_chrome_options


def get_driver(config: Config = None) -> webdriver.Chrome:
    if not config:
        config = Config()

    return webdriver.Chrome(
        executable_path=config.chrome.chromedriver,
        chrome_options=get_chrome_options(config=config),
    )
