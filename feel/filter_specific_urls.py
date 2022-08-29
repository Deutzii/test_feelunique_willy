# !/usr/bin/env python
"""Specific url filter.

Filters specific URLs from urls_to_filter file with the wanted keywords referenced in const.py."""

import json
import os
import time

import pandas as pd
from unidecode import unidecode

from const import (
    COLLECT_DATE,
    SOURCE,
    SPECIFIC_KEYWORDS
)

PATH_URLS_AGGREGATED = os.path.join(os.curdir, 'urls_aggregated')
PATH_URLS_TO_COLLECT = os.path.join(os.curdir, 'urls_to_collect')
PATH_URLS_TO_COLLECT_ANCHOR = os.path.join(os.curdir, 'urls_to_collect_anchor')


def select_specific_urls(aggegated_urls, keywords):
    """Selects specific urls with the products of the `keywords`.

    Args:
        aggegated_urls (list): list of dictionaries of aggregated urls.
        keywords (list): list of keywords.

    Returns:
        list: List of dictionaries of specific aggregated urls.
    """

    specific_urls = []

    # Checks if the keyword is inside the url or the product name.
    for aggregated_url in aggegated_urls:
        for keyword in keywords:
            try:
                if str(unidecode(keyword).lower()) in str(unidecode(aggregated_url['product_name']).lower()):
                    specific_urls.append(aggregated_url)
            except:
                pass

            try:
                if str(unidecode(keyword).lower()) in str(unidecode(aggregated_url['product_brand']).lower()):
                    specific_urls.append(aggregated_url)
            except:
                pass

            try:
                if str(unidecode(keyword).lower()) in aggregated_url['url'].lower():
                    specific_urls.append(aggregated_url)
            except:
                pass

    if specific_urls:

        # Remove the duplicates
        df = pd.DataFrame(specific_urls)
        df = df.drop_duplicates(subset=['url'], keep='first')
        df = df[['category', 'sub_category', 'sub_sub_category', 'url']]
        df = df.reset_index(drop=True)
        unique_aggregated_urls = df.to_dict(orient='records')

        return unique_aggregated_urls

    else:
        time.sleep(0.001)
        exit("[LOG] No matching urls.")


def filter_specific_urls(specific_urls):
    """Filters the specific urls to collect.

    Args:
        specific_urls (list): list of dictionaries with the specific urls.

    Returns:
        list: List of dictionaries with the new urls to collect with the status key 'collected' as no.
    """

    print("[LOG] Start the filtration of the urls.")

    urls_to_collect = []
    for new_url in specific_urls:
        urls_to_collect.append({
            'url': new_url['url'],
            'category': new_url['category'],
            'sub_category': new_url['sub_category'],
            'sub_sub_category': new_url['sub_sub_category'],
            'collected': 'no'
        })

    print("[LOG] The filtration of the urls is finished.")
    print("[LOG] There are {} urls to collect.".format(len(urls_to_collect)))

    return urls_to_collect


def main():
    # Load the new aggregated urls
    with open(os.path.join(PATH_URLS_AGGREGATED, COLLECT_DATE + '_aggregated_urls_' + SOURCE + '.json'),
              encoding='utf-8') as file_to_open:
        aggregated_urls = json.load(file_to_open)

    specific_urls = select_specific_urls(aggregated_urls, SPECIFIC_KEYWORDS)
    specific_urls_to_collect = filter_specific_urls(specific_urls)

    # Save the specific urls to collect
    with open(os.path.join(PATH_URLS_TO_COLLECT, COLLECT_DATE + '_specific_urls_to_collect_' + SOURCE + '.json'),
              'w', encoding='utf-8') as file_to_dump:
        json.dump(specific_urls_to_collect, file_to_dump, indent=4, ensure_ascii=False)

    with open(os.path.join(PATH_URLS_TO_COLLECT_ANCHOR, COLLECT_DATE + '_specific_urls_to_collect_anchor_' + SOURCE + '.json'),
              'w', encoding='utf-8') as file_to_dump:
        json.dump(specific_urls_to_collect, file_to_dump, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    main()
