"""
    Collect datas from each products and store them inside product and reviews directory.
"""

import os
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

#set paths
PATH_DRIVER = "C:\Program Files (x86)\chromedriver_win32\chromedriver.exe"
PATH_PRODUCTS = os.path.join(os.curdir, 'products')
PATH_REVIEWS = os.path.join(os.curdir, 'reviews')
PATH_URLS_NEW = os.path.join(os.curdir, 'urls_new')

#set driver options to avoid getting detected as a bot
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
        'thumbs_up':None,
        'thumbs_down':None
    }

    return review_dict

def check_if_span_exist(d, className):
    """ Checks if an element in span exist

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


def main():

    # Load the urls
    urls_dicts = json.load(open('./urls_new/urls_new.json', 'r', encoding='utf-8'))

    products_dict = []
    reviews_dict = []
    # Go to each url and scrape datas
    for url_dict in urls_dicts:

        # Set the driver
        driver = webdriver.Chrome(PATH_DRIVER, options=options)
        driver.get(url_dict['url'])

        # Retrieve product info
        product_dict = init_product_dict()

        try:
            product_dict['product_name'] = driver.find_element(By.CLASS_NAME,"fn").text
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

        products_dict.append(product_dict)
        print(products_dict)
        """
        # Retrieve reviews
        try:
            reviews = driver.find_elements(By.CLASS_NAME, "bv-content-item-avatar-offset")
            for review in reviews:
                try:
                    stars = str(review.find_element(By.CLASS_NAME, "bv-off-screen").get_attribute('innerText'))
                    reviews_dict['rating'] = stars[0]
                except:
                    reviews_dict['rating'] = None
                    pass

                try:
                    reviews_dict['author'] = str(review.find_element(By.CSS_SELECTOR, ".bv-avatar-popup-target span").get_attribute('innerText'))
                except:
                    reviews_dict['author'] = None
                    pass

                try:
                    reviews_dict['date'] = str(review.find_element(By.CLASS_NAME, "bv-content-datetime-stamp").get_attribute('innerText'))
                except:
                    reviews_dict['date'] = None
                    pass

                try:
                    reviews_dict['review_title'] = review.find_element(By.CLASS_NAME, "bv-content-title").text
                except:
                    reviews_dict['review_title'] = None
                    pass

                try:
                    reviews_dict['review_text'] = review.find_element(By.CSS_SELECTOR, ".bv-content-summary-body-text p").text
                except:
                    reviews_dict['review_text'] = None
                    pass

                try:
                    if str(review.find_element(By.CLASS_NAME, "bv-badge-label").get_attribute('innerText')) ==
                    reviews_dict['product_purchased_by_author'] = review.find_element()


            """










if __name__ == "__main__":
    main()