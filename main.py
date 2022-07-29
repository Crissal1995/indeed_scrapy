import logging

from scraper import get_driver
from utility.config import get_config

if __name__ == "__main__":
    FORMAT = "%(asctime)s :: %(levelname)s :: [%(module)s.%(funcName)s.%(lineno)d] :: %(message)s"

    logging.basicConfig(
        level=logging.DEBUG,
        format=FORMAT,
        encoding="utf-8",
    )

    config = get_config("dev.cfg")
    driver = get_driver(config=config)

    url = "https://employers.indeed.com/c#e/candidates?id=0&sort=datedefault&order=desc&statusName=0"
    driver.get(url)

    logging.debug("hello world")
