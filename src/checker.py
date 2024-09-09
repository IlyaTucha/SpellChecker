import hashlib
import os

from src.damerau_levenshtein import levenshtein_calculate_distance
from src.entry import Entry
from collections import Counter
from concurrent.futures import ThreadPoolExecutor


class SpellChecker:
    def __init__(self, sorting_key) -> None:
        self.sorting_key = sorting_key
        self.cache = {}
        # Data from https://bokrcorpora.narod.ru/frqlist/frqlist.html
        data_file_path = 'resources/data.txt'

        if not os.path.exists(data_file_path):
            raise FileNotFoundError(f"The file '{data_file_path}' does not exist.")

        with open(data_file_path, 'r', encoding='utf-8') as data_file:
            self.data = [Entry(word) for word in data_file.read().split('\n')]
            self.max_len = max(len(entry.word) for entry in self.data)
            self.counter = Counter(words.word for words in self.data)
            self.total = float(sum(self.counter.values()))

    def calculate_distance(self, entry, target_word):
        entry.distance = levenshtein_calculate_distance(entry.word, target_word)
        return entry

    def calculate_distances(self, word) -> list[Entry]:
        hash_key = hashlib.md5(word.encode('utf-8')).hexdigest()
        if hash_key in self.cache:
            return self.cache[hash_key]

        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(self.calculate_distance, entry, word) for entry in self.data]
        self.cache[hash_key] = [future.result() for future in futures]
        return self.cache[hash_key]

    def get_corrections(self, word) -> list[Entry]:
        distance_data = self.calculate_distances(word)
        corrections = sorted(distance_data, key=self.sorting_key, reverse=True)[:5]
        for correction in corrections:
            correction.other = word
        return corrections
