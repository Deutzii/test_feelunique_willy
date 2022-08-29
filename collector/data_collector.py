#!/usr/bin/env python
"""Data collectors.

Regroups all the collectors that collect data on the targeted pages.
Those collectors return the data in form of dictionaries."""

import random
import time

from bs4 import BeautifulSoup
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from init_dict import (
    init_url_dict,
    init_product_dict,
    init_review_dict
)


##### --------------------------------------------------- #####
##### --------------------- URLS ------------------------ #####
##### --------------------------------------------------- #####

def collect_urls_data(driver, category_dict):
    """Collects the urls data on the page `category_dict['url_category']`.

    Args:
        driver (WebDriver): selenium webdriver.
        category_dict (dict): dictionary containing the category's URL and its arborescence.

    Returns:
        list: List of dictionaries with the urls data.
    """

    urls_dicts = []

    # HTML code
    html_page = BeautifulSoup(driver.page_source, 'html.parser')

    # Select the products
    products = html_page.find_all('div', class_='Product')

    for id_product, product in enumerate(products):
        url_dict = init_url_dict()

        # Product categories
        url_dict['category'] = category_dict['category']
        url_dict['sub_category'] = category_dict['sub_category']
        url_dict['sub_sub_category'] = category_dict['sub_sub_category']
        url_dict['url_category'] = category_dict['url_category']

        try:
            url_dict['id_product'] = id_product + 1
        except:
            pass

        # Product url
        try:
            url_dict['url'] = 'https://www.feelunique.com' + product.a['href']
        except:
            pass

        # Product name
        try:
            url_dict['product_name'] = product.select_one('div[class~="Product-summary"]').text.replace('\n', '').strip()
        except:
            pass

        # Product mean rating
        try:
            url_dict['mean_rating'] = float(product.select_one('span[class="Rating-average"]').text.replace('/5', '').strip())
        except:
            pass

        # Product review number
        try:
            url_dict['n_reviews'] = int(product.select_one('span[class="Rating-count"]').text)
        except:
            pass

        # Product price
        try:
            price = product.select_one('span[class="Price-integer"]').text + \
                    product.select_one('span[class="Price-decimal"]').text
            url_dict['product_price'] = price
        except:
            price = product.select_one('span[class="integers"]').text + \
                    product.select_one('span[class="decimals"]').text
            url_dict['product_price'] = price
            pass

        # Product reviews
        try:
            if product.select_one('div[class="Rating Rating--stars"]'):
                urls_dicts.append(url_dict)
        except:
            pass

    return urls_dicts


##### ------------------------------------------------------ #####
##### --------------------- PRODUCT ------------------------ #####
##### ------------------------------------------------------ #####

def collect_product_data(driver, category_dict):
    """Collects the data of the product on the page `category_dict['url']`.

    Args:
        driver (WebDriver): selenium driver
        category_dict (dict): dictionary containing the product's categories and its URL.

    Returns:
        dict: Dictionary with product data.
    """

    product_dict = init_product_dict()

    # Product url
    product_dict['url'] = category_dict['url']

    # Product categories
    product_dict['category'] = category_dict['category']
    product_dict['sub_category'] = category_dict['sub_category']
    product_dict['sub_sub_category'] = category_dict['sub_sub_category']

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

    # Product price
    try:
        product_dict['product_price'] = str(driver.find_element(
            By.CSS_SELECTOR, 'span[class="Price"]').get_attribute('innerText')).replace('  ', '')
    except:
        pass

    # Product description
    try:
        product_dict['product_description'] = driver.find_element(
            By.CSS_SELECTOR, 'section[id="information"] div[class="Layout-golden-main"]').text
    except:
        pass

    # Product mean rating
    try:
        product_dict['mean_rating'] = float(driver.find_element(
            By.CSS_SELECTOR, 'span[class="Rating-average"]').get_attribute('data-aggregate-rating'))
    except:
        pass

    # Product review count
    try:
        product_dict['n_reviews'] = int(driver.find_element(
            By.CSS_SELECTOR, 'span[class="Rating-count"]').get_attribute('innerText').split()[0])
    except:
        pass

    return product_dict


##### ------------------------------------------------------ #####
##### --------------------- REVIEWS ------------------------ #####
##### ------------------------------------------------------ #####

def collect_reviews_data(driver, product_dict):
    """Collects the data contained in the displayed reviews in the product page.

    Args:
        driver (WebDriver): selenium driver.
        product_dict (dict): dictionary with the product information.

    Returns:
        list: List of dictionaries with reviews data.
    """

    reviews_dicts = []

    try:
        reviews = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((
            By.CSS_SELECTOR, 'ol[data-bv-v] > li[itemprop="review"]')))
        print('[LOG] There are some reviews on the current page.')

    except KeyboardInterrupt:
        exit('[LOG] The collect has been interrupted by the user.')

    except TimeoutException:
        print("[LOG] There aren't any reviews on the current page.")
        pass

    except Exception as e:
        print(e)
        pass

    else:
        for id_review, review in enumerate(reviews):
            review_dict = init_review_dict()

            # Product categories
            review_dict['category'] = product_dict['category']
            review_dict['sub_category'] = product_dict['sub_category']
            review_dict['sub_sub_category'] = product_dict['sub_sub_category']

            # Review id
            review_dict['id_review_product'] = 1 + id_review

            # Retrieve the information from the product dictionary
            review_dict['url'] = product_dict['url']
            review_dict['product_name'] = product_dict['product_name']
            review_dict['product_brand'] = product_dict['product_brand']
            review_dict['n_reviews'] = product_dict['n_reviews']

            # Review title
            try:
                review_dict['review_title'] = review.find_element(
                    By.CSS_SELECTOR, 'h3[class="bv-content-title"]').text
            except:
                pass

            # Review text
            try:
                review_dict['review_text'] = review.find_element(
                    By.CSS_SELECTOR, 'div[class="bv-content-summary-body-text"] p').text
            except:
                pass

            # Writer's pseudo
            try:
                review_dict['writer_pseudo'] = str(review.find_element(
                    By.CSS_SELECTOR, '.bv-avatar-popup-target span[itemprop="name"]').get_attribute('innerText'))
            except:
                pass

            # Review recommendation
            try:
                if len(review.find_elements(By.CSS_SELECTOR, 'span[class="bv-badge-label"]')) > 0:
                    review_dict['writer_recommendation'] = True
                else:
                    review_dict['writer_recommendation'] = False
            except:
                pass

            # Review date
            try:
                review_dict['review_date'] = str(review.find_element(
                    By.CSS_SELECTOR, 'div[class="bv-content-datetime"] '
                                     'span[class="bv-content-datetime-stamp"]').get_attribute('innerText')) \
                    .replace(' ', '')
            except:
                pass

            # Review rating
            try:
                stars = str(review.find_element(
                    By.CSS_SELECTOR, 'span[class="bv-rating-stars-container"] '
                                     + 'span[class="bv-off-screen"]').get_attribute('innerText'))
                review_dict['review_rating'] = stars[0]
            except:
                pass

            # Verified purchase
            try:
                if len(review.find_elements(By.CSS_SELECTOR, 'span[class="bv-badge-label"]')) > 0:
                    review_dict['verified_purchase'] = True
                else:
                    review_dict['verified_purchase'] = False
            except:
                pass

            reviews_dicts.append(review_dict)

    return reviews_dicts
