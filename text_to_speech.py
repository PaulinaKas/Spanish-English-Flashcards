import pandas as pd
import os
import re
import config
from gtts import gTTS

words = config.words_with_categories_list_path

column_name = 'spanish'

def generate_mp3_files(date: str, domain: str = 'es') -> None: # com.mx - mexico, es - spain
    output_folder = config.speech_folder
    output_folder = os.path.join(output_folder, domain)
    os.makedirs(output_folder, exist_ok=True)

    df = pd.read_csv(words)
    df = df[df['date']==date]

    for index, row in df.iterrows():
        word = str(row[column_name]).strip()
        percent_lvl = round(index / df.shape[0]*100,1)
        if word:
            tts = gTTS(text=word, lang='es')
            mp3_filename = os.path.join(output_folder,  f'{word}.mp3')
            try:
                tts.save(mp3_filename)
                print(f'{percent_lvl}% Saved: {mp3_filename}')
            except OSError:
                invalid_chars = r'[<>:"\\|?*]'
                cleaned_word = re.sub(invalid_chars, '', word)
                invalid_chars = r'/'
                cleaned_word = re.sub(invalid_chars, ' ', cleaned_word)
                mp3_filename = os.path.join(output_folder, f'{cleaned_word}.mp3')
                tts.save(mp3_filename)
                print(f'**************************{word}**************************')
                print(f'{percent_lvl}% Saved: {mp3_filename}')

    print('All mp3 files have been saved.')

    fill_in_mp3_column(df, date)


def fill_in_mp3_column(df: pd.DataFrame, date: str):
    for index, row in df.iterrows():
        date_col = row['date']
        if date_col == date:
            spanish_col = row['spanish']

            invalid_chars = r'[<>:"\\|?*]'
            cleaned_mp3_col = re.sub(invalid_chars, '', spanish_col)
            invalid_chars = r'/'
            cleaned_mp3_col = re.sub(invalid_chars, ' ', cleaned_mp3_col)
            mp3_col = f'{spanish_col}[sound:{cleaned_mp3_col}.mp3]'

            df.at[index, 'mp3'] = mp3_col

    df.to_csv(words, index=False)


