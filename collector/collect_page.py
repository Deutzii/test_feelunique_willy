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
target_url = 'https://www.feelunique.com/p/Liz-Earle-Pure-Muslin-Cloths-x-2'

# Set paths
PATH_DRIVER = 'C:\Program Files (x86)\chromedriver_win32\chromedriver.exe'
#PATH_DRIVER = os.path.join(os.curdir, 'chromedriver')
PATH_PRODUCT = os.path.join(os.curdir, 'product')
PATH_REVIEWS = os.path.join(os.curdir, 'reviews')
PATH_URLS_NEW = os.path.join(os.curdir, 'urls_new')

# Set driver options to avoid getting detected as a bot
options = webdriver.ChromeOptions()
options.add_argument('start-maximized')
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_experimental_option('excludeSwitches', ['enable-automation'])
options.add_experimental_option('useAutomationExtension', False)


def init_product_dict():
    """Initializes the dictionary with the product data.

    Returns:
        dict: Dictionary with the product data.
    """

    product_dict = {
        'product_name': None,
        'product_brand': None,
        'mean_rating': None,
        'n_reviews': None,
        'product_price': None,
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
        'author_recommends_product': None,
        'product_quality': None,
        'product_value': None,
        'product_result': None,
        'collect_date': time.strftime('%Y_%m_%d')
    }

    return review_dict


def check_if_class_exist(d, class_name):
    """ Checks if a class exists in the HTML page

    Args:
        d (WebDriver): Chromedriver
        class_name (str): name of span class that's being searched

    Returns:
        Boolean
    """
    try:
        d.findElement(By.CLASS_NAME, class_name)
    except NoSuchElementException:
        return False

    return True


def accept_cookies(driver):
    try:
        time.sleep(random.uniform(1, 5))
        cookie_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'notice-ok')))
    except NoSuchElementException:
        print('[LOG] No pop-up to close')
        pass
    else:
        cookie_button.click()
        print('[LOG] Pop-up closed')



def main():
    products_dicts = []

    print("[LOG] Loading page..")
    # Set the driver
    driver = webdriver.Chrome(PATH_DRIVER, options=options)
    driver.get(target_url)
    print("[LOG] Page loaded.")

    # accept cookies
    accept_cookies(driver)

    # ---------------------------------------------------
    # ----                  PRODUCT                  ----
    # ---------------------------------------------------

    # Retrieve product info
    product_dict = init_product_dict()
    print("[LOG] Start collecting the product data.")

    # Product name
    try:
        product_dict['product_name'] = driver.find_element(
            By.CSS_SELECTOR, 'h1[class="fn"]').text
    except:
        pass

    # Product brand
    try:
        product_dict['product_brand'] = driver.find_element(
            By.CSS_SELECTOR, 'p[class="u-flush-v"] strong').text
    except:
        pass

    # Product rating
    try:
        product_dict['mean_rating'] = float(driver.find_element(
            By.CSS_SELECTOR, 'span[class="Rating-average"]').get_attribute('data-aggregate-rating'))
    except:
        pass

    # Review count
    try:
        product_dict['n_reviews'] = int(driver.find_element(
            By.CSS_SELECTOR, 'span[class="Rating-count"]').get_attribute('innerText').replace(' reviews', ''))
    except:
        pass

    # Product price
    try:
        product_dict['product_price'] = str(driver.find_element(
            By.CSS_SELECTOR, 'span[class="Price"]').get_attribute('innerText')).replace('  ', '')
    except:
        pass

    # Product info
    try:
        product_dict['product_info'] = driver.find_element(
            By.CSS_SELECTOR, 'div[class="Layout-golden-main"]').text
    except:
        pass

    products_dicts.append(product_dict)

    # Save the product data
    with open(os.path.join(PATH_PRODUCT, str(time.strftime('%Y_%m_%d_%H_%M_%S')) + '_product.json'),
              'w', encoding='utf-8') as file_to_dump:
        json.dump(products_dicts, file_to_dump, indent=4, ensure_ascii=False)
    print('[LOG] Product data saved.')
    # ---------------------------------------------------
    # ----                  REVIEWS                  ----
    # ---------------------------------------------------

    while True:

        # Initialize the list that will contain the wanted review data
        reviews_dicts: list[dict] = []
        print('[LOG] Start collecting the reviews data.')

        # Detect the presence of the reviews and select them
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

        for review in reviews:

            # Initialize a dictionary for the current review
            review_dict = init_review_dict()

            # Author's rating per 5
            try:
                stars = str(review.find_element(
                    By.CSS_SELECTOR, 'span[class="bv-rating-stars-container"] '
                                     + 'span[class="bv-off-screen"]').get_attribute('innerText'))
                review_dict['rating'] = stars[0]
            except:
                pass

            # Author's username
            try:
                review_dict['author'] = str(review.find_element(
                    By.CSS_SELECTOR, '.bv-avatar-popup-target span[itemprop="name"]').get_attribute('innerText'))
            except:
                pass

            # Author's review publication date
            try:
                review_dict['date'] = str(review.find_element(
                    By.CSS_SELECTOR, 'div[class="bv-content-datetime"] '
                                     'span[class="bv-content-datetime-stamp"]').get_attribute('innerText'))\
                    .replace(' ', '')
            except:
                pass

            # Author's review title
            try:
                review_dict['review_title'] = review.find_element(
                    By.CSS_SELECTOR, 'h3[class="bv-content-title"]').text
            except:
                pass

            # Author's review text
            try:
                review_dict['review_text'] = review.find_element(
                    By.CSS_SELECTOR, 'div[class="bv-content-summary-body-text"] p').text
            except:
                pass

            # Author purchased the product
            try:
                if len(review.find_elements(By.CSS_SELECTOR, 'span[class="bv-badge-label"]')) > 0:
                    review_dict['product_purchased_by_author'] = True
                else:
                    review_dict['product_purchased_by_author'] = False
            except:
                pass

            # Author recommends the product
            try:
                if len(review.find_elements(By.CSS_SELECTOR, 'div[class="bv-content-data-recommend-yes"]')) > 0:
                    review_dict['author_recommends_product'] = True
                elif len(review.find_elements(By.CSS_SELECTOR, 'div[class="bv-content-data-recommend-no"]')) > 0:
                    review_dict['author_recommends_product'] = False
            except:
                pass

            # Secondary reviews ( quality, value, and result )
            try:
                if len(review.find_elements(By.CSS_SELECTOR, 'div[class="bv-content-details-container"]')) > 0:
                    secondary_reviews = review.find_elements(
                            By.CSS_SELECTOR, 'ul[class="bv-content-secondary-ratings"] > '
                                             + 'li[class="bv-popup-histogram-ratings-bar"] '
                                             + 'span[class="bv-off-screen"]')
                    if len(secondary_reviews) > 0:
                        for x in secondary_reviews:
                            if str(x.get_attribute('innerText'))[0] == 'Q':
                                review_dict['product_quality'] = str(x.get_attribute('innerText'))[20]
                            elif str(x.get_attribute('innerText'))[0] == 'V':
                                review_dict['product_value'] = str(x.get_attribute('innerText'))[18]
                            elif str(x.get_attribute('innerText'))[0] == 'R':
                                review_dict['product_result'] = str(x.get_attribute('innerText'))[9]
            except:
                pass

            reviews_dicts.append(review_dict)

        # Save reviews
        with open(os.path.join(PATH_REVIEWS, str(time.strftime('%Y_%m_%d_%H_%M_%S')) + '_reviews' + '.json'),
                  'w', encoding='utf-8') as file_to_dump:
            json.dump(reviews_dicts, file_to_dump, indent=4, ensure_ascii=False)
        print('[LOG]', len(reviews_dicts), 'Reviews have been collected for the current page')

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


if __name__ == '__main__':
    main()
