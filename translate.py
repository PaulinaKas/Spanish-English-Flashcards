import config
import pandas as pd
from diki_translate import Diki
from collections import Counter
from Levenshtein import distance

def translate_to_polish() -> [str]:
    filename = config.words_with_categories_list_path
    diki_eng = Diki('english')
    diki_spa = Diki('spanish')

    df = pd.read_csv(filename, index_col=None)
    df['polish'] = None
    df['to_manual_check'] = 0

    k = 0
    for row in df.iterrows():
        found = None
        common_translations = []
        word_spa = row[1]['spanish']
        translations_from_spanish = list(diki_spa.translation(word_spa, 0))

        word_eng = row[1]['english']
        translations_from_english = list(diki_eng.translation(word_eng, 0))

        for w_e in translations_from_english:
            for w_s in translations_from_spanish:
                if w_e in w_s:
                    common_translations.append(w_e)
        for w_s in translations_from_spanish:
            for w_e in translations_from_english:
                if w_s in w_e:
                    common_translations.append(w_s)

        if len(common_translations) == 0:
            common_translations = max(translations_from_english, translations_from_spanish)

        count = Counter(common_translations)
        common_translations = sorted(count, key=lambda x: (-count[x], x))
        if len(common_translations) > 2:
            if count[common_translations[0]] == count[common_translations[1]]:
                common_translations = [get_most_similar_words(common_translations[0], common_translations[0], word_spa)]
                df.at[k, 'to_manual_check'] = 1
            found = 1
        elif len(common_translations) > 1 and not found:
            if count[common_translations[0]] == count[common_translations[1]]:
                common_translations = list(count.keys())
                df.at[k, 'to_manual_check'] = 1

        try:
            df.at[k, 'polish'] = common_translations[0]
            k += 1
        except IndexError:
            k += 1
        percentage = round(k / df.shape[0]*100,1)
        print(f'{percentage}% translated')

    df.to_csv(filename, index=False)

def get_most_similar_words(word_1: str, word_2: str, target: str) -> str:
    distance_word_1 = distance(word_1, target)
    distance_word_2 = distance(word_2, target)

    return word_1 if distance_word_1 < distance_word_2 else word_2



