#!/usr/bin/env python
""" Page Collector

Collects data from the product contained in the URL
The data is then stored inside JSON files in /products and /reviews directories."""

import json
import os
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from page_navigator import save_product_page_data

from const import (
    OPTIONS,
    SOURCE,
    COLLECT_DATE,
    SPECIFIC_URLS_TO_COLLECT,
)

# Set target URL
target_url = 'https://www.feelunique.com/p/Liz-Earle-Pure-Muslin-Cloths-x-2'

# Set paths
PATH_PRODUCT = os.path.join(os.curdir, 'product')
PATH_REVIEW = os.path.join(os.curdir, 'review')
PATH_URLS_TO_COLLECT = os.path.join(os.curdir, 'urls_to_collect')
PATH_DRIVER = os.path.join(os.curdir, 'chromedriver')


def main():
    # Select the url
    category_dict = {
        'url': target_url,
        'category': 'Skincare',
        'sub_category': 'Cleansers',
        'sub_sub_category': 'Face Cloths & Sponges'
    }

    # Load the driver
    ser = Service(PATH_DRIVER)
    driver = webdriver.Chrome(service=ser, options=OPTIONS)
    print("[LOG] Time:", time.strftime('%H:%M:%S'))

    # Collect product and reviews data
    _ = save_product_page_data(driver, category_dict, PATH_PRODUCT, PATH_REVIEW)

    driver.delete_all_cookies()
    driver.quit()


if __name__ == '__main__':
    main()
