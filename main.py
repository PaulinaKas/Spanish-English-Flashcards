import words_downloader as downloader
import text_to_speech as speech
import translate

def main():
    # words_df = downloader.download_from_html()
    # words = downloader.convert_to_word_obj(words_df)
    # speech.generate_mp3_files('com.mx')
    translate.translate_to_polish()


if __name__ == "__main__":
    main()