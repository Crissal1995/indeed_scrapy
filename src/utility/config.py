import configparser
import logging
from typing import Optional

from attr import dataclass

logger = logging.getLogger(__name__)


@dataclass
class ChromeConfig:
    user_agent: Optional[str] = None

    profile_root: Optional[str] = None
    profile: Optional[str] = None

    binary_location: Optional[str] = None
    chromedriver: Optional[str] = None


@dataclass
class SeleniumConfig:
    headless: bool = False

    logging: bool = True
    no_sandbox: bool = True
    ignore_certificate_errors: bool = True
    allow_running_insecure_content: bool = True
    disable_dev_shm_usage: bool = True
    disable_gpu: bool = True


DEFAULT_CHROME_CONFIG = ChromeConfig()
DEFAULT_SELENIUM_CONFIG = SeleniumConfig()


@dataclass
class Config:
    chrome: ChromeConfig = DEFAULT_CHROME_CONFIG
    selenium: SeleniumConfig = DEFAULT_SELENIUM_CONFIG


DEFAULT_CONFIG = Config()


def get_config(cfg_fp: str = "", *, first_usage=False) -> Config:
    parser = configparser.ConfigParser()

    if first_usage and not cfg_fp or not parser.read(cfg_fp):
        logger.debug(f"Cannot read config from {cfg_fp}. Defaults will be used.")
        return DEFAULT_CONFIG
    else:
        logger.debug(f"Correctly parsed config from {cfg_fp}")

    # get selenium options
    selenium = parser["selenium"]
    headless = selenium.getboolean(
        "headless", fallback=DEFAULT_SELENIUM_CONFIG.headless
    )
    _logging = selenium.getboolean("logging", fallback=DEFAULT_SELENIUM_CONFIG.logging)
    no_sandbox = selenium.getboolean(
        "no_sandbox", fallback=DEFAULT_SELENIUM_CONFIG.no_sandbox
    )
    ignore_certificate_errors = selenium.getboolean(
        "ignore_certificate_errors",
        fallback=DEFAULT_SELENIUM_CONFIG.ignore_certificate_errors,
    )
    allow_running_insecure_content = selenium.getboolean(
        "allow_running_insecure_content",
        fallback=DEFAULT_SELENIUM_CONFIG.allow_running_insecure_content,
    )
    disable_dev_shm_usage = selenium.getboolean(
        "disable_dev_shm_usage", fallback=DEFAULT_SELENIUM_CONFIG.disable_dev_shm_usage
    )
    disable_gpu = selenium.getboolean(
        "disable_gpu", fallback=DEFAULT_SELENIUM_CONFIG.disable_gpu
    )

    # get chrome options
    chrome = parser["chrome"]
    user_agent = chrome.get("user_agent", fallback=DEFAULT_CHROME_CONFIG.user_agent)
    profile_root = chrome.get(
        "profile_root", fallback=DEFAULT_CHROME_CONFIG.profile_root
    )
    profile = chrome.get("profile", fallback=DEFAULT_CHROME_CONFIG.profile)
    binary_location = chrome.get(
        "binary_location", fallback=DEFAULT_CHROME_CONFIG.binary_location
    )
    chromedriver = chrome.get(
        "chromedriver", fallback=DEFAULT_CHROME_CONFIG.chromedriver
    )

    _config = Config(
        chrome=ChromeConfig(
            user_agent=user_agent,
            profile_root=profile_root,
            profile=profile,
            binary_location=binary_location,
            chromedriver=chromedriver,
        ),
        selenium=SeleniumConfig(
            headless=headless,
            logging=_logging,
            no_sandbox=no_sandbox,
            ignore_certificate_errors=ignore_certificate_errors,
            allow_running_insecure_content=allow_running_insecure_content,
            disable_dev_shm_usage=disable_dev_shm_usage,
            disable_gpu=disable_gpu,
        ),
    )

    return _config


# read one time and then use it
config = get_config(first_usage=True)
