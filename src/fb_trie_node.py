from src.checker import SpellChecker


class FBTrieNode:
    def __init__(self):
        self.checker = SpellChecker(sorting_key=lambda item: item.distance)
        self.children = {}
        self.probability = 0
        self.best_prev = None

    def update(self, probability, best_prev):
        if probability > self.probability:
            self.probability = probability
            self.best_prev = best_prev

    def word_probability(self, word):
        return self.checker.counter[word] / self.checker.total

    def viterbi_segment(self, text):
        root = FBTrieNode()
        probs = [1.0]
        lasts = [0]

        for i in range(1, len(text) + 1):
            max_probability, max_probability_index = self.find_max_probability(text, probs, i)

            prob_k, k = max_probability, max_probability_index

            probs.append(prob_k)
            lasts.append(k)

            node = root
            for char in text[lasts[i]:i]:
                node = self.get_or_create_child(node, char)

            node.update(prob_k, k)

        words = self.extract_words(text, lasts)
        return words, probs[-1]

    def find_max_probability(self, text, probs, i):
        max_probability = 0
        max_probability_index = 0

        for j in range(max(0, i - self.checker.max_len), i):
            prefix = text[j:i]
            current_probability = probs[j] * self.word_probability(prefix)

            if current_probability > max_probability:
                max_probability = current_probability
                max_probability_index = j

        return max_probability, max_probability_index

    def get_or_create_child(self, node, char):
        if char not in node.children:
            node.children[char] = FBTrieNode()
        return node.children[char]

    def extract_words(self, text, lasts):
        words = []
        i = len(text)
        while 0 < i:
            words.append(text[lasts[i]:i])
            i = lasts[i]

        words.reverse()
        return words
