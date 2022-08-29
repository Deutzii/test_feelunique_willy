#!/usr/bin/env python
"""Utils.

Contains all the tool functions useful in various steps of the collect."""

import json
import os
import time

from const import (
    COLLECT_DATE,
    SOURCE
)


##### ------------------------------------------------------------ #####
##### ---------------------- SAVING PROCESS ---------------------- #####
##### ------------------------------------------------------------ #####

def save_data(path, data, saved_data_type):
    """Saves the collected data.

    Args:
        path (str): path where the data will be saved.
        data (object): data to save.
        saved_data_type (str): 'url_new', 'products' or 'reviews'.
    """

    with open(os.path.join(path, COLLECT_DATE + '_' + saved_data_type + '_' + SOURCE + '_' + str(
            time.strftime('%Y_%m_%d_%H_%M_%S')) + '.json'), 'w', encoding='utf-8') as file_to_dump:
        json.dump(data, file_to_dump, indent=4, ensure_ascii=False)
