from selenium.webdriver.chrome.options import Options


def get_options(**kwargs) -> Options:
    options = Options()
    options.add_argument("no-sandbox")
    options.add_argument("ignore-certificate-errors")
    options.add_argument("allow-running-insecure-content")
    options.add_argument("disable-dev-shm-usage")
    options.add_argument("disable-gpu")

    profile_root = kwargs.get("profile_root") or config["selenium"]["profile_root"]
    profile_dir = kwargs.get("profile_dir")

    if profile_root and profile_dir:
        if IN_DOCKER_CONTAINER:
            logger.warning(
                "Cannot use profiles in docker env! Defaults to old login method"
            )
        else:
            logger.info(f"Using profile '{profile_dir}' (root: {profile_root})")
            options.add_argument(f"--user-data-dir={profile_root}")
            options.add_argument(f"--profile-directory={profile_dir}")
    elif profile_dir:  # ignore only profile_root set
        raise ValueError(
            "Cannot use Chrome profile without 'profile_root' variable set in configuration"
        )

    ua = kwargs.get("user_agent")
    if ua:
        options.add_argument(f"user-agent={ua}")

    if kwargs.get("headless") or config["selenium"]["headless"]:
        options.add_argument("headless")

    if not config["selenium"]["enable_logging"]:
        options.add_experimental_option("excludeSwitches", ["enable-logging"])

    binary_location = config["selenium"]["binary_location"]
    if binary_location:
        logger.info(f"Binary location provided: {binary_location}")
        options.binary_location = binary_location

    return options
