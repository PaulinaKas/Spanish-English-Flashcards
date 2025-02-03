import config
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
from sklearn.metrics import accuracy_score
from collections import Counter

def categorize_words():
    df = pd.read_csv(config.words_with_categories_list_path)
    df = df[['spanish', 'english', 'category']]
    df['category'] = df['category'].str.replace('_', ' ')
    df_predictions_spanish, accuracy_spanish = predict_categories_by_language(df, 'spanish')
    df_predictions_english, accuracy_english = predict_categories_by_language(df, 'english')

    print(1)

def predict_categories_by_language(df: pd.DataFrame, language: str) -> (pd.DataFrame, float):
    labels_balanced = is_labels_distribution_equal(df)
    if not labels_balanced:
        stratify = df['category']
    else:
        stratify = None
    try:
        X_train, X_test, y_train, y_test = train_test_split(df[language], df['category'],
                                                            test_size=0.1, random_state=42, stratify=stratify)
    except ValueError:
        # train / test groups have not enough elements
        df = df.groupby('category').filter(lambda x: len(x) > 1)
        stratify = df['category']
        X_train, X_test, y_train, y_test = train_test_split(df[language], df['category'],
                                                            test_size=0.1, random_state=42, stratify=stratify)
        stratified = y_train.value_counts()

    model = make_pipeline(TfidfVectorizer(), MultinomialNB())
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    df_outcome = pd.DataFrame(data={'X_test': X_test.to_list(),
                                    'y_test': y_test.to_list(),
                                    'y_pred': list(y_pred)})

    return df_outcome, accuracy


def is_labels_distribution_equal(df: pd.DataFrame) -> bool:
    category_counts = dict(Counter(df['category']))
    plt.figure(figsize=(12, 6))
    bars = plt.barh(list(category_counts.keys()), list(category_counts.values()), color='skyblue')
    for bar in bars:
        plt.text(bar.get_width() + 5, bar.get_y() + bar.get_height() / 2, str(int(bar.get_width())), va='center')
    plt.xlabel('Count')
    plt.ylabel('Categories')
    plt.title('Distribution of labels')
    plt.tight_layout()
    # plt.show()
    plt.savefig(config.labels_distribution, dpi=300, bbox_inches='tight')

    counts = np.array(list(category_counts.values()))
    mean_count = np.mean(counts)
    threshold = 0.1 * mean_count
    is_equally_distributed = np.all(np.abs(counts - mean_count) <= threshold)

    return is_equally_distributed



