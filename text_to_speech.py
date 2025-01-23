import pandas as pd
import os
import re
import config
from gtts import gTTS

words = config.words_list_path

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

    print('All files have been saved.')
