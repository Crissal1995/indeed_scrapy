import configparser
import logging
from typing import Optional

from attrs import define


logger = logging.getLogger(__name__)


@define
class ChromeConfig:
    user_agent: Optional[str] = None

    profile_root: Optional[str] = None
    profile: Optional[str] = None

    binary_location: Optional[str] = None


@define
class SeleniumConfig:
    headless: bool = False

    logging: bool = True
    no_sandbox: bool = True
    ignore_certificate_errors: bool = True
    allow_running_insecure_content: bool = True
    disable_dev_shm_usage: bool = True
    disable_gpu: bool = True


@define
class Config:
    chrome: ChromeConfig
    selenium: SeleniumConfig


def get_config(cfg_fp: str = "", *, first_usage=False) -> Config:
    parser = configparser.ConfigParser()

    # skip the read if it's first usage,
    # found in this file with no path provided
    if not first_usage:
        # read file (can also be not found)
        if not cfg_fp:
            logger.warning("No config provided! Defaults will be used.")
        elif not parser.read(cfg_fp):
            logger.warning(f"Cannot read config from {cfg_fp}. Defaults will be used.")

    # get selenium options
    path = parser.get("selenium", "path")
    url = parser.get("selenium", "url")
    headless = parser.getboolean("selenium", "headless")
    enable_logging = parser.getboolean("selenium", "logging")
    profile_root = parser.get("selenium", "profile_root")
    binary_location = parser.get("selenium", "binary_location")

    # get automsr options
    skip = parser.get("automsr", "skip").lower()
    retry = parser.getint("automsr", "retry")
    credentials = parser.get("automsr", "credentials")
    search_type = parser.get("automsr", "search_type")
    verbose = parser.getboolean("automsr", "verbose")

    # get email options
    send = parser.getboolean("email", "send")
    strategy = parser.get("email", "strategy")
    sender = parser.get("email", "sender")
    password = parser.get("email", "password")
    recipient = parser.get("email", "recipient")
    tls = parser.getboolean("email", "tls")
    host = parser.get("email", "host")
    port = parser.getint("email", "port")

    # get prize options
    mask = parser.get("prize", "mask")

    # finally, return the config dictionary
    return {
        "automsr": dict(
            skip=skip,
            skip_activity=skip_activity,
            skip_punchcard=skip_punchcard,
            skip_search=skip_search,
            retry=retry,
            credentials=credentials,
            search_type=search_type,
            verbose=verbose,
        ),
        "selenium": dict(
            env=env,
            path=path,
            url=url,
            headless=headless,
            enable_logging=enable_logging,
            profile_root=profile_root,
            binary_location=binary_location,
        ),
        "email": dict(
            send=send,
            strategy=strategy,
            sender=sender,
            password=password,
            recipient=recipient,
            tls=tls,
            host=host,
            port=port,
        ),
        "prize": dict(
            mask=mask,
        ),
    }


# read one time and then use it
config = get_config(first_usage=True)
