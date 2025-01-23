import pandas as pd
import config
from transformers import pipeline

all_words_path = config.words_with_categories_list_path

def create_sentence_in_spanish(words):
    generator = pipeline("text-generation", model='')

def get_words_to_create_sentence() -> [str]:
    df_raw = pd.read_csv(all_words_path)
    df = df_raw[['spanish', 'english', 'category']]

    get_new_random_word(df, 'noun', 'people')
    a = df

def process_sentences():
    words = get_words_to_create_sentence()
    exit()
    create_sentence_in_spanish(words)


def get_all_categories(df: pd.DataFrame, pos: str) -> [str]:
    result = df[df['category'].str.startswith(pos)]
    return list(result['category'].unique())


def get_new_random_word(df: pd.DataFrame, pos: str, subset_condition: str) -> pd.DataFrame:
    categories = get_all_categories(df, pos) # verb, adjective, noun

    if subset_condition == 'people':
        selected_category = [i for i in categories if subset_condition in i]
    else:
        return

    df = df[df['category'] == selected_category]

    return df






process_sentences()

words = input("Introduce palabras en español separadas por comas: ").split(',')
words = [word.strip() for word in words]
result = create_sentence_in_spanish(words)
print("Oración generada:", result)
