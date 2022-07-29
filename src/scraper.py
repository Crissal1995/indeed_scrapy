from selenium import webdriver

from utility.config import Config
from utility.options import get_chrome_options


def get_driver(config: Config = None) -> webdriver.Chrome:
    return webdriver.Chrome(chrome_options=get_chrome_options(config=config))
