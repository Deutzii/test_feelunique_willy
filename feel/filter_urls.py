#!/usr/bin/env python
"""Urls filter.

Deletes duplicates in the urls_to_filter file."""

import json
import os

from const import (
    COLLECT_DATE,
    SOURCE
)

PATH_URLS_TO_FILTER = os.path.join(os.curdir, 'urls_to_filter')
PATH_URLS_TO_COLLECT = os.path.join(os.curdir, 'urls_to_collect')
PATH_URLS_TO_COLLECT_ANCHOR = os.path.join(os.curdir, 'urls_to_collect_anchor')


def filter_urls(new_urls):
    """Filters the urls to collect.

    Args:
        new_urls (list): list of dictionaries with the new urls.

    Returns:
        list: List of dictionaries with the new urls to collect with the status key 'collected' as no.
    """

    print("[LOG] Start the filtration of the urls.")

    urls_to_collect = []
    for new_url in new_urls:
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
    with open(os.path.join(PATH_URLS_TO_FILTER, COLLECT_DATE + '_urls_to_filter_' + SOURCE + '.json'),
              encoding='utf-8') as file_to_open:
        new_urls = json.load(file_to_open)

    # Filter the urls
    urls_to_collect = filter_urls(new_urls)

    # Save the urls to collect
    with open(os.path.join(PATH_URLS_TO_COLLECT, COLLECT_DATE + '_urls_to_collect_' + SOURCE + '.json'),
              'w', encoding='utf-8') as file_to_dump:
        json.dump(urls_to_collect, file_to_dump, indent=4, ensure_ascii=False)

    with open(os.path.join(PATH_URLS_TO_COLLECT_ANCHOR, COLLECT_DATE + '_urls_to_collect_anchor_' + SOURCE + '.json'),
              'w', encoding='utf-8') as file_to_dump:
        json.dump(urls_to_collect, file_to_dump, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    main()
