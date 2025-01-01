from lxml import html
from config import url_words, url_host, logger_file_name
from datetime import datetime
import pandas as pd
import warnings
import os
import http.client

warnings.simplefilter(action='ignore', category=FutureWarning)

WORDS_LIST_FOLDER_PATH = 'words_list'
WORDS_LIST_FILE_NAME = 'list.csv'
WORDS_LIST_PATH = os.path.join(WORDS_LIST_FOLDER_PATH, WORDS_LIST_FILE_NAME)
WORDS_LIST_LIMIT = 3000
WORDS_LIST_DOWNLOAD_DATE = 'date'

WORDS_TABLE_CLASS = 'cImu42Ep'
WORDS_TABLE_ID = 'main-container-video'

connection = http.client.HTTPSConnection(url_host)
connection.request("GET", url_words)
response = connection.getresponse()
df = pd.DataFrame(columns=['spanish', 'english'])

if response.status == 200:
    content = response.read()
    tree = html.fromstring(content)
    main_container = tree.get_element_by_id(WORDS_TABLE_ID, None)

    if main_container:
        current_date = datetime.now().date()
        table = main_container.find_class(WORDS_TABLE_CLASS)
        if table:
            for k in range(1, WORDS_LIST_LIMIT):
                try:
                    spanish = tree.xpath(f'/html/body/div/div/div[1]/div/div[1]/div[3]/div[{k}]/div/div[4]/a/div[1]')[0].text
                    english = tree.xpath(f'/html/body/div/div/div[1]/div/div[1]/div[3]/div[{k}]/div/div[4]/a/div[2]')[0].text
                    df.at[k, 'spanish'] = spanish
                    df.at[k, 'english'] = english
                except IndexError:
                    try:
                        # TODO: add loger info about saving status, new words number
                        df_original = pd.read_csv(WORDS_LIST_PATH)
                        df = pd.concat([df_original, df])
                        df[WORDS_LIST_DOWNLOAD_DATE] = None
                        duplicated_rows = df.duplicated(keep=False)
                        df_new_words = df.drop(duplicated_rows[duplicated_rows].index)
                        df_old_words = df.drop(duplicated_rows[~duplicated_rows].index)
                        df_new_words[WORDS_LIST_DOWNLOAD_DATE] = current_date
                        df = pd.concat([df_old_words, df_new_words])
                        df.to_csv(WORDS_LIST_PATH, index=False)
                        break
                    except FileNotFoundError:
                        df[WORDS_LIST_DOWNLOAD_DATE] = current_date
                        df.to_csv(WORDS_LIST_PATH, index=False)
                        break