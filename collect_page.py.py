#!/usr/bin/env python
""" Page Collector

Collects data from the product contained in the URL
The data is then stored inside JSON files in /products and /reviews directories."""

import json
import os
import random
import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# Set target URL
targetURL = "https://www.feelunique.com/p/Liz-Earle-Pure-Muslin-Cloths-x-2"

# Set paths
# PATH_DRIVER = "C:\Program Files (x86)\chromedriver_win32\chromedriver.exe"
PATH_DRIVER = os.path.join(os.curdir, 'chromedriver')
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
        'rating': None,
        'author': None,
        'date': None,
        'review_title': None,
        'review_text': None,
        'product_purchased_by_author': None,
        'author_recommends_product': None
    }

    return review_dict


def check_if_class_exist(d, className):
    """ Checks if a class exists in the HTML page

    Args:
        d (WebDriver): Chromedriver
        className: name of span class that's being searched

    Returns:
        Boolean
    """
    try:
        d.findElement(By.CLASS_NAME, className)
    except NoSuchElementException:
        return False

    return True


def accept_cookies(driver):
    cookieButton = driver.find_element(By.ID, "notice-ok")
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

    # ---------------------------------------------------
    # ----                  PRODUCT                  ----
    # ---------------------------------------------------

    # Retrieve product info
    product_dict = init_product_dict()
    print("[LOG] Start collecting the product data.")

    # Product name
    try:
        product_dict['product_name'] = driver.find_element(
            By.CLASS_NAME, "fn").text
    except:
        pass

    # Product rating
    try:
        product_dict['mean_rating'] = str(driver.find_element(
            By.CLASS_NAME,"Rating-average").get_attribute('data-aggregate-rating'))
    except:
        pass

    # Review count
    try:
        product_dict['n_reviews'] = str(driver.find_element(
            By.CSS_SELECTOR, ".Rating-count span").get_attribute('innerText'))
    except:
        pass

    # Product price
    try:
        product_dict['product_price'] = str(driver.find_element(
            By.CLASS_NAME,"Price").get_attribute('innerText')).replace(' ', '')
    except:
        pass

    # Product info
    try:
        product_dict['product_info'] = driver.find_element(
            By.CLASS_NAME,"Layout-golden-main").text
    except:
        pass

    products_dicts.append(product_dict)

    # Save the product data
    with open(os.path.join(PATH_PRODUCTS, 'products.json'), 'w', encoding='utf-8') as file_to_dump:
        json.dump(products_dicts, file_to_dump, indent=4, ensure_ascii=False)


    # ---------------------------------------------------
    # ----                  REVIEWS                  ----
    # ---------------------------------------------------
    while True:

        # Initialize the list that will contain the wanted review data
        reviews_dicts: list[dict] = []
        print("[LOG] Start collecting the reviews data.")

        # Detect the presence of the reviews and select them
        try:
            reviews = driver.find_elements(By.CSS_SELECTOR, 'ol[data-bv-v] > li[data-content-id]')
        except KeyboardInterrupt:
            exit("[LOG] The collect has been interrupted by the user.")

        except TimeoutException:
            print("[LOG] There aren't any reviews on the current page.")
            pass

        except Exception as e:
            print(e)
            pass

        for review in reviews:

            # Initialize a dictionary for the current review
            review_dict = init_review_dict()
            try:
                stars = str(review.find_element(
                    By.CLASS_NAME, "bv-off-screen").get_attribute('innerText'))
                review_dict['rating'] = stars[0]
            except:
                pass

            try:
                review_dict['author'] = str(review.find_element(
                    By.CSS_SELECTOR, ".bv-avatar-popup-target span").get_attribute('innerText'))
            except:
                pass

            try:
                review_dict['date'] = str(review.find_element(
                    By.CLASS_NAME, "bv-content-datetime-stamp").get_attribute('innerText'))
            except:
                pass

            try:
                review_dict['review_title'] = review.find_element(
                    By.CLASS_NAME, "bv-content-title").text
            except:
                pass

            try:
                review_dict['review_text'] = review.find_element(
                    By.CSS_SELECTOR, ".bv-content-summary-body-text p").text
            except:
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
                if review.find_element(
                        By.CSS_SELECTOR, 'div[class="bv-content-data-recommend-no"]'):
                    review_dict['author_recommends_product'] = "No"
                elif review.find_element(
                        By.CSS_SELECTOR, 'div[class="bv-content-data-recommend-yes"]'):
                    review_dict['author_recommends_product'] = "Yes"
            except:
                review_dict['author_recommends_product'] = None
                pass

            reviews_dicts.append(review_dict)

        # Save reviews
        with open(os.path.join(PATH_REVIEWS, str(time.strftime('%Y_%m_%d_%H_%M_%S')) + '_reviews' + '.json'),
                  'w', encoding='utf-8') as file_to_dump:
            json.dump(reviews_dicts, file_to_dump, indent=4, ensure_ascii=False)
        print('[LOG]', len(reviews_dicts), 'Reviews have been collected for the current page')

        # Go to the next reviews page
        try:
            driver.execute_script("arguments[0].click();", WebDriverWait(driver, 10).until(EC.presence_of_element_located((
                    By.CSS_SELECTOR, ".bv-content-pagination-buttons-item-next a"))))
            print("[LOG] Go to the next reviews page.")

        except TimeoutException:
            print("[LOG] There are no mo reviews pages.")
            break

        except Exception as e:
            print(e)
            break


if __name__ == "__main__":
    main()
