import words_downloader as downloader
import text_to_spech as speech

def main():
    # words_df = downloader.download_from_html()
    # words = downloader.convert_to_word_obj(words_df)
    speech.generate_mp3_files('com.mx')


if __name__ == "__main__":
    main()