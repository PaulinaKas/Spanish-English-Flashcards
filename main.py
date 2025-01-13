import words_downloader as downloader

def main():
    words_df = downloader.download_from_html()
    # words = downloader.convert_to_word_obj(words_df)

if __name__ == "__main__":
    main()