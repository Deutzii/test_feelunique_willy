#!/usr/bin/env python
"""URLs aggregator.

Aggregates all the files contained in /urls_new into  aggregated_urls and urls_to_filter files."""

import glob
import json
import os
import pandas as pd

from const import (
    COLLECT_DATE,
    SOURCE
)

PATH_URLS_NEW = os.path.join(os.curdir, 'urls_new')
PATH_URLS_AGGREGATED = os.path.join(os.curdir, 'urls_aggregated')
PATH_URLS_TO_FILTER = os.path.join(os.curdir, 'urls_to_filter')


def aggregate_urls():
    """Gathers all the json files from the 'urls_new' folder.

    It aggregates them into:
        1/ a file in the 'urls_aggregated' folder
        2/ a file in the 'urls_to_filter' folder
    """

    print("[LOG] Start the aggregation of the urls.")

    # Save the aggregated urls in 'urls_aggregated' folder
    new_urls_dicts = []
    for url_dict in glob.glob(os.path.join(PATH_URLS_NEW, '*.json')):
        try:
            for new_url_dict in json.load(open(url_dict, 'r', encoding='utf8')):
                new_urls_dicts.append(new_url_dict)
        except:
            pass

    with open(os.path.join(PATH_URLS_AGGREGATED, COLLECT_DATE + '_aggregated_urls_' + SOURCE + '.json'), 'w',
              encoding='utf-8') as file_to_dump:
        json.dump(new_urls_dicts, file_to_dump, indent=4, ensure_ascii=False)

    # Save the aggregated urls in 'urls_to_filter' folder
    df = pd.DataFrame(new_urls_dicts)
    df = df.drop_duplicates(['url'])
    urls_filtered_list = df.to_dict(orient='records')

    with open(os.path.join(PATH_URLS_TO_FILTER, COLLECT_DATE + '_urls_to_filter_' + SOURCE + '.json'), 'w',
              encoding='utf-8') as file_to_dump:
        json.dump(urls_filtered_list, file_to_dump, indent=4, ensure_ascii=False)

    print("[LOG] The aggregation of the urls is finished.")


def main():
    aggregate_urls()


if __name__ == "__main__":
    main()
