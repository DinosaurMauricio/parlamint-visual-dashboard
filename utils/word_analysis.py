class WordAnalysis:

    @staticmethod
    def calculate_word_count(df, column):
        return df[column].str.split().str.len()

    @staticmethod
    def calculate_total_words(word_counts):
        return word_counts.sum()

    @staticmethod
    def calculate_statistics(word_counts, total_words):
        word_array = word_counts.to_numpy()
        return {
            "average_length": total_words / len(word_array),
            "min_len": int(word_array.min()),
            "max_len": int(word_array.max()),
            "total_words": total_words,
        }
