#!/usr/bin/env python
"""Constants.

Regroups all the parameters and constants that may need to be set up by the operator."""

from selenium.webdriver.chrome.options import Options

OPTIONS = Options()

# User agent
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36'
OPTIONS.add_argument(f'user-agent={user_agent}')

# Disable unnecessary functionality causing message error in the console
OPTIONS.add_argument("--disable-extensions --disable-gpu --disable-dev-shm-usage --disable")
OPTIONS.add_experimental_option('excludeSwitches', ['enable-logging'])

# Closing some unnecessary pop-ups
OPTIONS.add_argument("--no-first-run --no-service-autorun --password-store=basic")

# Start in full-screen with a defined window size
OPTIONS.add_argument("window-size=1920,1080")
OPTIONS.add_argument("start-maximised")

# Hide some bot related stuff to increase stealthiness
OPTIONS.add_argument('--disable-blink-features=AutomationControlled')
OPTIONS.add_experimental_option('useAutomationExtension', False)
OPTIONS.add_experimental_option("excludeSwitches", ['enable-automation'])

# Headless
OPTIONS.add_argument("--headless")

COLLECT_DATE = '2022_08_01'
SOURCE = 'feelunique_uk'
LANGUAGE = 'en'  # norme ISO language - 639-1
COUNTRY = 'uk'  # norme ISO country - alpha 2
INDUSTRY = 'cosmetic'

# Collect mode: specific or not specific
SPECIFIC_URLS_TO_COLLECT = False
SPECIFIC_KEYWORDS = ['VICHY']
