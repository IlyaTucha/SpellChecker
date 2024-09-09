import string
from src.checker import SpellChecker
import re
from src.entry import Entry
from time import perf_counter
from src.fb_trie_node import FBTrieNode


class SpellCheckerConsole:
    def __init__(self, language='ru'):
        self.language = language
        self.FBTrieNode = FBTrieNode()
        self.checker = SpellChecker(sorting_key=lambda item: item.distance)
        self.print_welcome_message()

    def print_welcome_message(self):
        welcome_message = {
            'ru': "Добро пожаловать в Спеллчекер!\n"
                  "Эта программа поможет вам выявить и исправить орфографические ошибки в вашем тексте.\n",
            'en': "Welcome to the Spell Checker Console!\n"
                  "This program can help you identify and correct spelling errors in your text.\n"
        }

        if self.language not in welcome_message:
            self.language = 'en'
            print("Unsupported language. Using English as the default.")

        print(welcome_message[self.language])

    def run(self):
        while True:
            if self.language == 'ru':
                text_input = input("Введите текст (введите 'exit' для выхода): ")
            else:
                text_input = input("Enter text (type 'exit' to quit): ")
            if text_input.lower() == 'exit':
                break
            self.check_text(text_input)

    def check_text(self, text):
        words = re.split(r'[ ,.!?]', text)
        for original_word in words:
            word_without_punctuation = original_word.rstrip(string.punctuation)
            word_lower = word_without_punctuation.lower()

            if not word_lower:
                continue

            if not self.is_russian(word_lower):
                if self.language == 'ru':
                    print(f"Ошибка: Пожалуйста, введите на русском языке."
                          f" Слово '{original_word}' не на русском языке или содержит цифры.")
                else:
                    print(f"Error: Please write in Russian."
                          f" Word '{original_word}' is not in Russian or contains digits.")
                continue

            t1 = perf_counter()
            if word_lower.startswith("пол-"):
                second_part = word_lower.split("-")[1]
                viterby_correction, viterby_probability = self.FBTrieNode.viterbi_segment(second_part)
                corrections = self.check_word(second_part)
            else:
                viterby_correction, viterby_probability = self.FBTrieNode.viterbi_segment(word_lower)
                corrections = self.check_word(word_lower)

            self.print_correction(original_word, [correction for correction in corrections]
                                  + [' '.join(viterby_correction)], perf_counter() - t1)

    @staticmethod
    def is_russian(word):
        return all(1072 <= ord(char) <= 1103 or char in ['ё', '-'] for char in word)

    def check_word(self, word):
        corrections = self.checker.get_corrections(word)
        return corrections

    def print_correction(self, original_word, corrections, time):
        if self.language == 'ru':
            print(f"Оригинальный текст: {original_word}".ljust(50), "Исправленный текст: ", end="")
        else:
            print(f"Original Text: {original_word}".ljust(50), "Corrected text: ", end="")

        corrected_words = []
        for correction in corrections:
            if isinstance(correction, Entry):
                corrected_words.append(f"{correction.word} ({correction.distance * 100:.2f}%)")
            elif correction != original_word.lower():
                corrected_words.append(f"{correction}")

        if self.language == 'ru':
            print('\n'.ljust(72).join(corrected_words))
            print(f'\nНайдено исправление за {time} секунд\n')
        else:
            print('\n'.ljust(68).join(corrected_words))
            print(f'\nFound correction in {time}s\n')


if __name__ == "__main__":
    language_choice = input("Choose language (enter 'ru' for Russian, 'en' for English): ")
    console = SpellCheckerConsole(language=language_choice.lower())
    console.run()
