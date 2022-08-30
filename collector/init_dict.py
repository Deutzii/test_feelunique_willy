#!/usr/bin/env python
"""Dictionary initializer.

Initializes the required dictionaries and returns them to data_collector.py."""

import time

from const import (
    SOURCE,
    COUNTRY,
    LANGUAGE,
    INDUSTRY
)

##### --------------------------------------------------- #####
##### --------------------- URLS ------------------------ #####
##### --------------------------------------------------- #####

def init_url_dict():
    """Initializes the dictionary with the information of a product url

    Returns:
       dict: Dictionary with the product url data.
    """

    url_dict = {
        'id_product': None,
        'product_name': None,
        'mean_rating': None,
        'n_reviews': None,
        'product_price': None,
        'category': None,
        'sub_category': None,
        'sub_sub_category': None,
        'code_sku': None,
        'url': None,
        'url_category': None,
        'source': SOURCE,
        'country': COUNTRY,
        'language': LANGUAGE,
        'industry': INDUSTRY,
        'collect_date': str(time.strftime('%Y-%m-%d')),
    }

    return url_dict


##### ------------------------------------------------------ #####
##### --------------------- PRODUCT ------------------------ #####
##### ------------------------------------------------------ #####

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
        'product_description': None,
        'code_sku': None,
        'url': None,
        'category': None,
        'sub_category': None,
        'sub_sub_category': None,
        'source': SOURCE,
        'country': COUNTRY,
        'language': LANGUAGE,
        'industry': INDUSTRY,
        'collect_date': str(time.strftime('%Y-%m-%d')),
    }

    return product_dict


##### ------------------------------------------------------ #####
##### --------------------- REVIEWS ------------------------ #####
##### ------------------------------------------------------ #####

def init_review_dict():
    """Initializes the dictionary with the review data.

    Returns:
        dict: Dictionary with the review data.
    """

    review_dict = {
        'id_review_product': None,
        'product_name': None,
        'product_brand': None,
        'category': None,
        'sub_category': None,
        'sub_sub_category': None,
        'code_sku': None,
        'url': None,
        'writer_pseudo': None,
        'writer_recommendation': None,
        'review_rating': None,
        'review_date': None,
        'review_title': None,
        'review_text': None,
        'verified_purchase': None,
        'source': SOURCE,
        'country': COUNTRY,
        'language': LANGUAGE,
        'industry': INDUSTRY,
        'collect_date': str(time.strftime('%Y-%m-%d')),
    }

    return review_dict
