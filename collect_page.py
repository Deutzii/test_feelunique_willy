"""
    Collect datas from each products and store them inside product and reviews directory.
"""

import os
from typing import List

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException


import json
import time
import random

# Set target URL
targetURL = "https://www.feelunique.com/p/Liz-Earle-Pure-Muslin-Cloths-x-2"

# Set paths
PATH_DRIVER = "C:\Program Files (x86)\chromedriver_win32\chromedriver.exe"
PATH_PRODUCTS = os.path.join(os.curdir, 'products')
PATH_REVIEWS = os.path.join(os.curdir, 'reviews')
PATH_URLS_NEW = os.path.join(os.curdir, 'urls_new')

# Set driver options to avoid getting detected as a bot
options = webdriver.ChromeOptions()
options.add_argument("start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ['enable-automation'])
options.add_experimental_option('useAutomationExtension', False)

def init_product_dict():
    """Initializes the dictionary with the product data.

    Returns:
        dict: Dictionary with the product data.
    """

    product_dict = {
        'product_name':None,
        'product_rating':None,
        'product_rating_count':None,
        'product_price':None,
        'product_info': None
    }

    return product_dict

def init_review_dict():
    """Initializes the dictionary with the product review.

    Returns:
        dict: Dictionary with the product review.
    """

    review_dict = {
        'rating':None,
        'author':None,
        'date':None,
        'review_title':None,
        'review_text':None,
        'product_purchased_by_author':None,
        'author_recommends_product': None
    }

    return review_dict

def check_if_class_exist(d, className):
    """ Checks if a class exist in the HTML page

    Args:
        d (WebDriver) = Chromedriver
        className = name of span class that's being searched

    Returns:
        Boolean
    """
    try:
        d.findElement(By.CLASS_NAME, className)
    except NoSuchElementException:
        return False

    return True


def accept_cookies(driver):
    cookieButton = driver.find_element(By.ID,"notice-ok")
    time.sleep(random.uniform(1, 5))
    cookieButton.click()


def main():
    products_dicts = []

    # Set the driver
    driver = webdriver.Chrome(PATH_DRIVER, options=options)
    driver.get(targetURL)
    print("[LOG] Page loaded.")

    # accept cookies
    accept_cookies(driver)
    print("[LOG] Cookies accepted.")

    # Retrieve product info
    product_dict = init_product_dict()

    try:
        product_dict['product_name'] = driver.find_element(By.CLASS_NAME, "fn").text
    except:
        product_dict['product_name'] = None
        pass

    try:
        product_dict['product_rating'] = str(driver.find_element(By.CLASS_NAME,"Rating-average").get_attribute('data-aggregate-rating'))
    except:
        product_dict['product_rating'] = None
        pass

    try:
        product_dict['product_rating_count'] = str(driver.find_element(By.CSS_SELECTOR,".Rating-count span").get_attribute('innerText'))
    except:
        product_dict['product_rating_count'] = None
        pass

    try:
        product_dict['product_price'] = str(driver.find_element(By.CLASS_NAME,"Price").get_attribute('innerText'))
    except:
        product_dict['product_price'] = None
        pass

    try:
        product_dict['product_info'] = driver.find_element(By.CLASS_NAME,"Layout-golden-main").text
    except:
        product_dict['product_info'] = None
        pass

    products_dicts.append(product_dict)

    # Save products
    with open(os.path.join(
            PATH_PRODUCTS, 'products.json'), 'w', encoding='utf-8') as file_to_dump:
        json.dump(products_dicts, file_to_dump, indent=4, ensure_ascii=False)

    # Retrieve reviews
    while True:
        try:
            print("Scanning this page..")
            reviews = driver.find_elements(By.CSS_SELECTOR, 'ol[data-bv-v] > li[data-content-id]')
            for review in reviews:
                review_dict = init_review_dict()
                reviews_dicts: list[dict] = []
                try:
                    stars = str(review.find_element(By.CLASS_NAME, "bv-off-screen").get_attribute('innerText'))
                    review_dict['rating'] = stars[0]
                except:
                    review_dict['rating'] = None
                    pass

                try:
                    review_dict['author'] = str(review.find_element(By.CSS_SELECTOR, ".bv-avatar-popup-target span").get_attribute('innerText'))
                except:
                    review_dict['author'] = None
                    pass

                try:
                    review_dict['date'] = str(review.find_element(By.CLASS_NAME, "bv-content-datetime-stamp").get_attribute('innerText'))
                except:
                    review_dict['date'] = None
                    pass

                try:
                    review_dict['review_title'] = review.find_element(By.CLASS_NAME, "bv-content-title").text
                except:
                    review_dict['review_title'] = None
                    pass

                try:
                    review_dict['review_text'] = review.find_element(By.CSS_SELECTOR, ".bv-content-summary-body-text p").text
                except:
                    review_dict['review_text'] = None
                    pass

                try:
                    if check_if_class_exist(review, 'bv-content-data'):
                        review_dict['product_purchased_by_author'] = "Yes"
                    else:
                        review_dict['product_purchased_by_author'] = "No"
                except:
                    review_dict['product_purchased_by_author'] = None
                    pass


                try:
                    if review.find_element(By.CSS_SELECTOR, 'div[class="bv-content-data-recommend-no"]'):
                        review_dict['author_recommends_product'] = "No"
                    elif review.find_element(By.CSS_SELECTOR, 'div[class="bv-content-data-recommend-yes"]'):
                        review_dict['author_recommends_product'] = "Yes"
                except:
                    review_dict['author_recommends_product'] = None
                    pass

                reviews_dicts.append(review_dict)

            # Save reviews
            print("Saving reviews ..")
            with open(os.path.join(
                    PATH_REVIEWS, str(time.strftime('%Y_%m_%d_%H_%M_%S')) + '_reviews' + '.json'),
                    'w', encoding='utf-8') as file_to_dump:
                json.dump(reviews_dicts, file_to_dump, indent=4, ensure_ascii=False)
            print("Reviews saved !")

            try:
                driver.execute_script("arguments[0].click();", WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".bv-content-pagination-buttons-item-next a"))))
                print("[LOG] Next page button clicked.")
                time.sleep(3)
            except TimeoutException:
                print("[LOG] Last page reached.")
                break
            except Exception as e:
                print(e)
                break

        except:
            break


if __name__ == "__main__":
    main()