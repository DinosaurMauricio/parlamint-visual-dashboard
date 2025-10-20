from collections import Counter


class VocabularyAnalyzer:

    @staticmethod
    def calculate_vocab_size(df, column):
        vocab = set(df[column].str.split().explode())
        return len(vocab)

    @staticmethod
    def get_most_frequent_words(df, column, top):
        all_words = df[column].str.split().explode().tolist()
        word_freq = Counter(all_words)
        return word_freq.most_common(top)
