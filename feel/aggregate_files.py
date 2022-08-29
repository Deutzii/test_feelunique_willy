#!/usr/bin/env python
"""Files aggregator.

Aggregates all the files contained in reviews/ and products/ into merged_products and reviews_files files."""

import glob
import json
from json.decoder import JSONDecodeError
import os
import time

from const import (
    COLLECT_DATE,
    SOURCE
)

PATH_PRODUCTS = os.path.join(os.curdir, 'products')
PATH_MERGED_PRODUCTS = os.path.join(os.curdir, 'merged_products')
PATH_REVIEWS = os.path.join(os.curdir, 'reviews')
PATH_MERGED_REVIEWS = os.path.join(os.curdir, 'merged_reviews')


def aggregate_products_files():
    """Aggregates the collected products files."""

    products_files = []

    # For each json file, it opens the content of the file
    for products_file in glob.glob(os.path.join(PATH_PRODUCTS, '*.json')):
        try:
            open_product_file = json.load(open(products_file, 'r', encoding='utf8'))
            products_files.append(open_product_file)
        except JSONDecodeError:
            pass

    with open(os.path.join(PATH_MERGED_PRODUCTS, COLLECT_DATE + '_merged_products_' + SOURCE + '_' + str(
            time.strftime('%Y_%m_%d_%H_%M_%S')) + '.json'), 'w', encoding='utf-8') as file_to_dump:
        json.dump(products_files, file_to_dump, indent=4, ensure_ascii=False)

    print("[LOG] The products files have been merged.")
    print("[LOG] There are {} merged products.".format(len(products_files)))


def aggregate_reviews_files():
    """Aggregates the collected reviews files."""

    reviews_files = []

    # For each json file, it opens the content of the file
    for reviews_file in glob.glob(os.path.join(PATH_REVIEWS, '*.json')):
        try:
            open_reviews_file = json.load(open(reviews_file, 'r', encoding='utf8'))
            for review_file in open_reviews_file:
                reviews_files.append(review_file)
        except JSONDecodeError:
            pass

    with open(os.path.join(PATH_MERGED_REVIEWS, COLLECT_DATE + '_merged_reviews_' + SOURCE + '_' + str(
            time.strftime('%Y_%m_%d_%H_%M_%S')) + '.json'), 'w', encoding='utf-8') as file_to_dump:
        json.dump(reviews_files, file_to_dump, indent=4, ensure_ascii=False)

    print("[LOG] The reviews files have been merged.")
    print("[LOG] There are {} merged reviews.".format(len(reviews_files)))


def main():
    aggregate_products_files()
    aggregate_reviews_files()


if __name__ == "__main__":
    main()
