import unittest
from src.damerau_levenshtein import levenshtein_calculate_distance


class TestLevenshteinDistanceNormalized(unittest.TestCase):

    def test_same_strings(self):
        self.assertEqual(levenshtein_calculate_distance("самовар", "самовар"), 1.0)

    def test_one_empty_string(self):
        self.assertEqual(levenshtein_calculate_distance("самовар", ""), 0.0)
        self.assertEqual(levenshtein_calculate_distance("", "чайник"), 0.0)

    def test_insertion(self):
        self.assertEqual(levenshtein_calculate_distance("самовар", "самоварь"), 0.875)

    def test_case_insensitive(self):
        self.assertEqual(levenshtein_calculate_distance("самовар", "СамОвАр"), 1.0)

    def test_deletion(self):
        self.assertEqual(levenshtein_calculate_distance("самовар", "самоварь"), 0.875)

    def test_hyphenated_words(self):
        self.assertEqual(levenshtein_calculate_distance("пол-арбуза", "поларбуза"), 0.9)

    def test_missing_space(self):
        self.assertEqual(levenshtein_calculate_distance("как у тебя дела", "какутебядела"), 0.8)

    def test_substitution(self):
        self.assertEqual(levenshtein_calculate_distance("самовар", "симовар"),  0.8571428571428572)


if __name__ == '__main__':
    unittest.main()
