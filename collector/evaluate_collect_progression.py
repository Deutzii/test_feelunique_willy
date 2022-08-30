#!/usr/bin/env python
"""Collect progression evaluator.

Evaluates the collect progression by counting the collected URLs."""

import json
import os

from const import (
    SOURCE,
    COLLECT_DATE,
    SPECIFIC_URLS_TO_COLLECT,
)

PATH_DRIVER = os.path.join(os.curdir, 'chromedriver')
PATH_URLS_TO_COLLECT = os.path.join(os.curdir, 'urls_to_collect')


# Collect mode
if SPECIFIC_URLS_TO_COLLECT:
    PATH_FILE_URLS_TO_COLLECT = os.path.join(PATH_URLS_TO_COLLECT,
                                             COLLECT_DATE + '_specific_urls_to_collect_' + SOURCE + '.json')
else:
    PATH_FILE_URLS_TO_COLLECT = os.path.join(PATH_URLS_TO_COLLECT,
                                             COLLECT_DATE + '_urls_to_collect_' + SOURCE + '.json')


def main():
    # Load the urls to collect
    urls_dicts = json.load(open(PATH_FILE_URLS_TO_COLLECT, 'r', encoding='utf-8'))

    # Get the number of urls to collect
    n_urls_to_collect = len(urls_dicts)

    # Get the number of urls 'yes', 'once', 'issue' and 'no'.
    n_status_yes = 0
    n_status_no = 0
    n_status_once = 0
    n_status_issue = 0
    for url_dict in urls_dicts:
        url_status = url_dict['collected']
        if url_status == 'yes':
            n_status_yes = n_status_yes + 1
        elif url_status == 'no':
            n_status_no = n_status_no + 1
        elif url_status == 'once':
            n_status_once = n_status_once + 1
        elif url_status == 'issue':
            n_status_issue = n_status_issue + 1

    print("[LOG] There are {} urls to collect.".format(n_urls_to_collect))
    print("[LOG] There are {} ({} %) urls with the status YES.".format(n_status_yes, int(100 * n_status_yes / n_urls_to_collect)))
    print("[LOG] There are {} ({} %) urls with the status NO.".format(n_status_no, int(100 * n_status_no / n_urls_to_collect)))
    print("[LOG] There are {} ({} %) urls with the status ONCE.".format(n_status_once, int(100 * n_status_once / n_urls_to_collect)))
    print("[LOG] There are {} ({} %) urls with the status ISSUE.".format(n_status_issue, int(100 * n_status_issue / n_urls_to_collect)))


if __name__ == "__main__":
    main()
