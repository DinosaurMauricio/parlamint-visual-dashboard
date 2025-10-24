from abstract_class.base_statistics import BaseStatistics


class CorpusMetrics(BaseStatistics):
    def __init__(self, word_count, vocab_analyzer):
        self.word_analysis = word_count
        self.vocab_analyzer = vocab_analyzer

    def calculate(self, df):
        word_counts = self.word_analysis.calculate_word_count(df, "clean_text")
        total_words = self.word_analysis.calculate_total_words(word_counts)

        word_counts_no_stop = self.word_analysis.calculate_word_count(
            df, "no_stopwords"
        )
        total_no_stopwords = self.word_analysis.calculate_total_words(
            word_counts_no_stop
        )

        base_stats = self.word_analysis.calculate_statistics(word_counts, total_words)
        vocab_size = self.vocab_analyzer.calculate_vocab_size(df, "clean_text")

        percentage_stop_words = (total_no_stopwords * 100) / total_words

        return {
            "average_length": base_stats["average_length"],
            "min_len": base_stats["min_len"],
            "max_len": base_stats["max_len"],
            "vocab_size": vocab_size,
            "no_stop_words_text": total_no_stopwords,
            "total_words": total_words,
            "percentage_stop_words": percentage_stop_words,
        }


class SegmentMetrics(BaseStatistics):

    def __init__(self, word_counter):
        self.word_counter = word_counter

    def calculate(self, df):
        word_counts = self.word_counter.calculate_word_count(df, "text")
        total_words = self.word_counter.calculate_total_words(word_counts)
        stats = self.word_counter.calculate_statistics(word_counts, total_words)

        return stats
