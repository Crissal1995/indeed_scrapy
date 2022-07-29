import logging

from selenium.webdriver.chrome.options import Options

from src.utility.config import Config

logger = logging.getLogger(__name__)


def get_chrome_options(config: Config = None) -> Options:
    if not config:
        config = Config()

    options = Options()

    selenium_cfg = config.selenium

    if selenium_cfg.disable_gpu:
        options.add_argument("disable-gpu")

    if selenium_cfg.no_sandbox:
        options.add_argument("no-sandbox")

    if selenium_cfg.ignore_certificate_errors:
        options.add_argument("ignore-certificate-errors")

    if selenium_cfg.allow_running_insecure_content:
        options.add_argument("allow-running-insecure-content")

    if selenium_cfg.disable_dev_shm_usage:
        options.add_argument("disable-dev-shm-usage")

    if selenium_cfg.headless:
        options.add_argument("headless")

    if not selenium_cfg.logging:
        options.add_experimental_option("excludeSwitches", ["enable-logging"])

    chrome_cfg = config.chrome

    profile_root = chrome_cfg.profile_root
    profile_dir = chrome_cfg.profile

    if profile_root and profile_dir:
        logger.info(f"Using profile '{profile_dir}' (root: {profile_root})")
        options.add_argument(f"--user-data-dir={profile_root}")
        options.add_argument(f"--profile-directory={profile_dir}")
    elif profile_dir:  # ignore only profile_root set
        raise ValueError(
            "Cannot use Chrome profile without 'profile_root' variable set in configuration"
        )

    user_agent = chrome_cfg.user_agent
    if user_agent:
        options.add_argument(f"user-agent={user_agent}")

    binary_location = chrome_cfg.binary_location
    if binary_location:
        logger.info(f"Binary location provided: {binary_location}")
        options.binary_location = binary_location

    return options
