import pandas as pd
import config
from transformers import pipeline

all_words_path = config.words_with_categories_list_path

def create_sentence_in_spanish(words):
    generator = pipeline("text-generation", model='')

def get_words_to_create_sentence(condition: str) -> [str]:
    df_raw = pd.read_csv(all_words_path)
    df = df_raw[['spanish', 'english', 'category']]

    series_noun = get_new_random_word(df, 'noun', condition)
    noun_spanish = series_noun['spanish'].values[0]
    a = df

def process_sentences(condition: str):
    words = get_words_to_create_sentence(condition)
    exit()
    create_sentence_in_spanish(words)


def get_all_categories(df: pd.DataFrame, pos: str) -> [str]:
    result = df[df['category'].str.startswith(pos)]
    return list(result['category'].unique())


def get_new_random_word(df: pd.DataFrame, pos: str, subset_condition: str) -> pd.Series:
    categories = get_all_categories(df, pos) # verb, adjective, noun

    if subset_condition == 'people':
        selected_category = [i for i in categories if subset_condition in i]
    elif subset_condition == 'clothes':
        selected_category = [i for i in categories if subset_condition in i]
    else:
        return

    if len(selected_category) == 1:
        selected_category = selected_category[0]
    else:
        pass
    df = df[df['category'] == selected_category]
    sample = df.sample(1)

    return sample

