# !/usr/bin/env python
"""Page navigators.

Regroups all the navigators that navigate on the target website.
Those navigators launch the data collectors and save the returns into JSON files."""

import random
import time

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from data_collector import (
    collect_urls_data,
    collect_product_data,
    collect_reviews_data
)

from utils import save_data


##### ------------------------------------------------ #####
##### ----------------- PRODUCTS PAGE ---------------- #####
##### ------------------------------------------------ #####

def save_products_page_data(driver, category_dict, path_urls):
    """Collects and saves the data contained in the products-listing page `category_dict['url_category']`.

    Args:
        driver: selenium webdriver.
        category_dict (dict): dictionary containing the category's URL and its arborescence.
        path_urls (str): path of the directory in which the urls will be saved.
    """

    # Load the url
    print("[LOG] Loading the page...")
    driver.get(category_dict['url_category'])
    print("[LOG] Current url: {}.".format(category_dict['url_category']))
    time.sleep(random.uniform(1, 5))

    # Accept the cookies
    try:
        cookie_btn = WebDriverWait(driver, 15).until(EC.presence_of_element_located((
            By.CSS_SELECTOR, 'button[id="notice-ok"]')))
        cookie_btn.click()
        print("[LOG] Click on the cookies button.")
        time.sleep(random.uniform(1, 5))
    except:
        pass

    # Load all the products
    while True:
        try:
            load_more_reviews_btn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((
                By.CSS_SELECTOR, 'a[class="loadMoreButton"]')))
            driver.execute_script("arguments[0].scrollIntoView(true);", load_more_reviews_btn)
            driver.execute_script("arguments[0].click();", load_more_reviews_btn)
            print("[LOG] Click on show more products button.")
            time.sleep(random.uniform(1, 5))

        except TimeoutException:
            print("[LOG] There isn’t any more products to show.")
            break
        except KeyboardInterrupt:
            print("[LOG] The collect has been interrupted by the user.")
            break
        except:
            break
    
    # Collect the printed products
    try:
        print("[LOG] Start collecting urls data.")

        # Collect urls data
        urls_dicts = collect_urls_data(driver, category_dict)

        # Save the urls data
        save_data(path_urls, urls_dicts, 'urls_new')

        print("[LOG] {} urls have been collected.".format(len(urls_dicts)))

    except KeyboardInterrupt:
        print("[LOG] The collect has been interrupted by the user.")
        pass

    except:
        print("[LOG] There is an error for the current url.")
        pass


##### ------------------------------------------------ #####
##### ----------------- PRODUCT PAGE ----------------- #####
##### ------------------------------------------------ #####

def save_product_page_data(driver, category_dict, path_products, path_reviews):
    """Collects the data contained in the product page `category_dict['url']`.

    Args:
        driver: selenium driver
        category_dict (dict): dictionary containing the product's categories and its URL.
        path_products (str): path of the directory in which the products will be saved.
        path_reviews (str): path of the directory in which the reviews will be saved.

    Returns:
        tuple[dict, list]:
            dict: Dictionary with the product data.
            list: List of dictionaries with the review data.
    """

    # Load the url
    print("[LOG] Loading the page...")
    driver.get(category_dict['url'])
    print("[LOG] Current url:", category_dict['url'])
    time.sleep(random.uniform(1, 5))

    # Close the cookies pop up
    try:
        cookie_btn = WebDriverWait(driver, 15).until(EC.presence_of_element_located((
            By.CSS_SELECTOR, 'button[id="notice-ok"]')))
        cookie_btn.click()
        print("[LOG] Click on the cookies button.")
        time.sleep(random.uniform(1, 5))
    except:
        pass

    print("[LOG] Start collecting product data.")

    # Collect the product data
    product_dict = collect_product_data(driver, category_dict)

    # Save the product data
    save_data(path_products, product_dict, 'products')

    # Detect the presence of the reviews and select them
    while True:
        try:
            reviews = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((
                By.CSS_SELECTOR, 'ol[data-bv-v] > li[data-content-id]')))
            print('[LOG] There are some reviews on the current page.')

        except KeyboardInterrupt:
            exit('[LOG] The collect has been interrupted by the user.')

        except TimeoutException:
            print("[LOG] There aren't any reviews on the current page.")
            pass

        except Exception as e:
            print(e)
            pass

        print("[LOG] Start collecting reviews data.")

        # Collect the reviews data
        reviews_dicts = collect_reviews_data(driver, product_dict)

        # Save the reviews data
        save_data(path_reviews, reviews_dicts, 'reviews')

        print("[LOG] {} reviews have been collected.".format(len(reviews_dicts)))

        # Go to the next reviews page
        try:
            driver.execute_script('arguments[0].click();', WebDriverWait(driver, 10).until(EC.presence_of_element_located((
                By.CSS_SELECTOR, '.bv-content-pagination-buttons-item-next a'))))
            print('[LOG] Go to the next reviews page.')
            time.sleep(5)

        except TimeoutException:
            print('[LOG] There are no more reviews pages.')
            break

        except Exception as e:
            print(e)
            break

    return product_dict, reviews_dicts
