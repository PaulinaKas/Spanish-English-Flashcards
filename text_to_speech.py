import pandas as pd
import os
import config
from gtts import gTTS

words = config.words_list_path

column_name = 'spanish'

def generate_mp3_files(domain: str = 'es') -> None: # com.mx - mexico, es - spain
    output_folder = config.speech_folder
    output_folder = os.path.join(output_folder, domain)
    os.makedirs(output_folder, exist_ok=True)

    df = pd.read_csv(words)

    for index, row in df.iterrows():
        word = str(row[column_name]).strip()
        percent_lvl = round(index / df.shape[0]*100,1)
        if word:
            tts = gTTS(text=word, lang='es')
            mp3_filename = os.path.join(output_folder,  f'{word}.mp3')
            try:
                tts.save(mp3_filename)
            except OSError:
                mp3_filename = mp3_filename.replace('', '_')
            print(f'{percent_lvl}% Saved: {mp3_filename}')

    print('All files have been saved.')
