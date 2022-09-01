#!/usr/bin/env python
"""Pages collector.

Starts the collect of multiple pages by cycling through dictionaries found in urls_to_collect files,
sends for each product its URL and category information to the pages navigators."""

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

PATH_PRODUCTS = os.path.join(os.curdir, 'products')
PATH_REVIEWS = os.path.join(os.curdir, 'reviews')
PATH_URLS_TO_COLLECT = os.path.join(os.curdir, 'urls_to_collect')
PATH_DRIVER = os.path.join(os.curdir, 'chromedriver')

# Collect mode
if SPECIFIC_URLS_TO_COLLECT:
    PATH_FILE_URLS_TO_COLLECT = os.path.join(PATH_URLS_TO_COLLECT,
                                             COLLECT_DATE + '_specific_urls_to_collect_' + SOURCE + '.json')
else:
    PATH_FILE_URLS_TO_COLLECT = os.path.join(PATH_URLS_TO_COLLECT,
                                             COLLECT_DATE + '_urls_to_collect_' + SOURCE + '.json')


def main():

    # Load the urls
    urls_dicts = json.load(open(PATH_FILE_URLS_TO_COLLECT, 'r', encoding='utf-8'))

    for url_dict in urls_dicts:

        # Retrieve the categories
        category_dict = {
            'url': url_dict['url'],
            'category': url_dict['category'],
            'sub_category': url_dict['sub_category'],
            'sub_sub_category': url_dict['sub_sub_category']
        }

        # Select the url under specific conditions
        if url_dict['collected'] == 'no':

            # Load the driver
            ser = Service(PATH_DRIVER)
            driver = webdriver.Chrome(service=ser, options=OPTIONS)
            print("[LOG] Time:", time.strftime('%H:%M:%S'))

            try:
                # Collect and save the product and reviews data
                product_dict, reviews_dicts = save_product_page_data(
                    driver,
                    category_dict,
                    PATH_PRODUCTS,
                    PATH_REVIEWS
                )

                # Change the status of the current url and save it
                # --------------------------------------------------------
                # Step 1: Verify if the product has a name
                if product_dict['product_name']:

                    # Step 2: Verify if the product has reviews
                    if product_dict['n_reviews']:

                        # Step 3: Verify if the product has at least 1 review
                        if int(product_dict['n_reviews']) > 0:
                            url_dict['collected'] = 'yes'
                            print("[LOG] All the reviews have been collected for the product.")

                        # Step 3 (if not): The current url has 0 reviews
                        # The current url has 0 reviews
                        else:
                            url_dict['collected'] = 'yes'
                            print("[LOG] There are no reviews for the current url.")

                    # Step 2 (if not): The current url has 0 reviews
                    # The current url has 0 reviews
                    else:
                        url_dict['collected'] = 'yes'
                        print("[LOG] There are no reviews for the current url.")

                # Step 1 (if not): The page data didn't load
                else:
                    # If the page data didn't load
                    # The collect for the current url has raised some errors
                    # The url is set as 'issue'
                    url_dict['collected'] = 'issue'
                    print("[LOG] Issue with the current url. Saved as url with issues.")

            # Errors
            # --------------------------------------------------------
            # The collect for the current url has raised an error so the url status is set to 'issue'
            except:
                url_dict['collected'] = 'issue'
                print("[LOG] Issue with the current url. Saved as url with issues.")

            finally:
                with open(PATH_FILE_URLS_TO_COLLECT, 'w', encoding='utf-8') as file_to_dump:
                    json.dump(urls_dicts, file_to_dump, indent=4, ensure_ascii=False)

            driver.delete_all_cookies()
            driver.quit()


if __name__ == "__main__":
    main()
