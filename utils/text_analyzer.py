import spacy
import streamlit as st

from collections import Counter
from patterns.singleton_meta import SingletonMeta
from scipy.stats import skew


class TextAnalyzer(metaclass=SingletonMeta):

    def __init__(self, lang_model="en_core_web_sm"):
        self.nlp = spacy.load(lang_model, disable=["parser", "ner", "tagger"])

    @staticmethod
    @st.cache_data
    def get_corpus_senteces_count(df):
        return df.shape[0]

    @staticmethod
    @st.cache_data
    def get_corpus_unique_sentences_count(df):
        return df.full_text.unique().shape[0]

    @staticmethod
    @st.cache_data
    def get_total_words_corpus(df):
        df["word_count"] = df["full_text"].str.split().str.len()
        total_words = df["word_count"].sum()
        return total_words

    @st.cache_data
    def get_data_statistics(_self, df):

        df["word_count"] = df["clean_text"].str.split().str.len()
        # this total words are just the unique senteces!
        total_words = df["word_count"].sum()
        df["word_count_no_stop_words"] = df["no_stopwords"].str.split().str.len()
        total_no_stopwords = df["word_count_no_stop_words"].sum()

        percentage_of_stop_words = total_no_stopwords * 100 / total_words

        word_array = df["word_count"].to_numpy()
        avg_len = total_words / len(word_array)
        min_len = min(word_array)
        max_len = max(word_array)

        vocab = set(df["clean_text"].str.split().explode())

        vocab_size = len(vocab)

        results = {
            "average_length": avg_len,
            "min_len": min_len,
            "max_len": max_len,
            "vocab_size": vocab_size,
            "no_stop_words_text": total_no_stopwords,
            "total_words": total_words,
            "percentage_stop_words": percentage_of_stop_words,
        }

        return results

    @staticmethod
    @st.cache_data
    def get_sentences_skewness(df):
        df["word_count"] = df["clean_text"].str.split().str.len()
        return skew(df["word_count"])

    @staticmethod
    @st.cache_data
    def get_segments_word_statistics(df):
        results = {}
        df["word_count"] = df["text"].str.split().str.len()
        total_words = df["word_count"].sum()

        word_array = df["word_count"].to_numpy()
        avg_len = total_words / len(word_array)
        min_len = min(word_array)
        max_len = max(word_array)

        results = {
            "average_length": avg_len,
            "min_len": min_len,
            "max_len": max_len,
            "total_words": total_words,
        }
        return results

    @staticmethod
    @st.cache_data
    def get_number_of_rows(df):
        return df.shape[0]

    @staticmethod
    @st.cache_data
    def most_frequent_words(df, top=10):
        all_words_df = df["no_stopwords"].str.split()
        all_words = [word for sentence in all_words_df for word in sentence]
        word_freq = Counter(all_words)
        most_common_words = word_freq.most_common(top)

        return most_common_words

    @staticmethod
    @st.cache_data
    def get_sentiment_statistics(df):
        sentiment_3 = df["senti_3"].value_counts()
        sentiment_6 = df["senti_6"].value_counts()

        results = {"sentiment_3": sentiment_3, "sentiment_6": sentiment_6}
        return results
