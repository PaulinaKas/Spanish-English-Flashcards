from lxml import html
import config
from datetime import datetime
from logger import logger
from word import Word
import pandas as pd
import warnings
import http.client

warnings.simplefilter(action='ignore', category=FutureWarning)

WORDS_LIST_LIMIT = 3000
WORDS_LIST_DOWNLOAD_DATE = 'date'

WORDS_TABLE_CLASS = 'cImu42Ep'
WORDS_TABLE_ID = 'main-container-video'

def download_from_html() -> pd.DataFrame:
    connection = http.client.HTTPSConnection(config.url_host)
    connection.request("GET", config.url_words)
    response = connection.getresponse()
    df = pd.DataFrame(columns=['spanish', 'english'])

    if response.status == 200:
        content = response.read()
        tree = html.fromstring(content)
        main_container = tree.get_element_by_id(WORDS_TABLE_ID, None)

        if main_container:
            current_date = datetime.now().date()
            table = main_container.find_class(WORDS_TABLE_CLASS)
            logger.info('Table with words found')
            if table:
                for k in range(1, WORDS_LIST_LIMIT):
                    try:
                        spanish = \
                        tree.xpath(f'/html/body/div/div/div[1]/div/div[1]/div[3]/div[{k}]/div/div[4]/a/div[1]')[0].text
                        english = \
                        tree.xpath(f'/html/body/div/div/div[1]/div/div[1]/div[3]/div[{k}]/div/div[4]/a/div[2]')[0].text
                        df.at[k, 'spanish'] = spanish
                        df.at[k, 'english'] = english
                    except IndexError:
                        try:
                            df_original = pd.read_csv(config.words_list_path)
                            df[WORDS_LIST_DOWNLOAD_DATE] = None
                            df = pd.concat([df_original, df])
                            df.reset_index(inplace=True, drop=True)
                            duplicated_rows = df.duplicated(subset=['spanish', 'english'], keep=False)
                            df_new_words = df.drop(duplicated_rows[duplicated_rows].index)
                            new_words_number = df_new_words.shape[0]
                            if new_words_number == 0:
                                logger.info('No new words')
                                return df_original
                            else:
                                logger.info(f' {datetime.now().strftime("%m/%d/%Y, %H:%M:%S")} - '
                                            f'{new_words_number} words downloaded')
                            df_old_words = df.drop(duplicated_rows[~duplicated_rows].index)
                            df_old_words.drop_duplicates(subset=['spanish', 'english'], inplace=True, keep='first')
                            df_new_words[WORDS_LIST_DOWNLOAD_DATE] = current_date
                            df = pd.concat([df_old_words, df_new_words])
                            df.to_csv(config.words_list_path, index=False)
                            logger.info(f'Newly downloaded words appended into {config.words_list_file_name}')
                            return df
                        except FileNotFoundError:
                            df[WORDS_LIST_DOWNLOAD_DATE] = current_date
                            df.to_csv(config.words_list_path, index=False)
                            logger.info(f'{config.words_list_file_name} file created')
                            return df
            else:
                logger.error('Table with words not found')
    else:
        logger.error(f'No connection with {config.url_host}. Response code {response.status}')
        try:
            df_original = pd.read_csv(config.words_list_path)
            return df_original
        except FileNotFoundError:
            return df
    logger.info('The program finished successfully')
    logger.info('-----------------------------------------')

    return df

def convert_to_word_obj(df: pd.DataFrame) -> [Word]:
    words = []
    for row in df.iterrows():
        spanish = row[1]['spanish']
        english = row[1]['english']
        entry_date = row[1]['date']
        word = Word(_spanish=spanish, _english=english)
        word.entry_date = entry_date
        words.append(word)

    return words
