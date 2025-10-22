import spacy
import streamlit as st

from utils.word_analysis import WordAnalysis
from utils.vocabulary_analyzer import VocabularyAnalyzer
from utils.corpus_metrics import CorpusMetrics, SegmentMetrics
from collections import Counter
from patterns.singleton_meta import SingletonMeta
from scipy.stats import skew


class TextAnalyzer(metaclass=SingletonMeta):

    def __init__(self, lang_model="en_core_web_sm"):
        self.nlp = spacy.load(lang_model, disable=["parser", "ner", "tagger"])
        self.word_analysis = WordAnalysis()
        self.vocabulary_analyzer = VocabularyAnalyzer()
        self.corpus_metrics = CorpusMetrics(
            self.word_analysis, self.vocabulary_analyzer
        )
        self.segment_metrics = SegmentMetrics(self.word_analysis)

    @staticmethod
    @st.cache_data
    def get_number_of_rows(df):
        return df.shape[0]

    @staticmethod
    @st.cache_data
    def get_corpus_unique_sentences_count(df):
        return df.full_text.nunique()

    @staticmethod
    @st.cache_data
    def get_corpus_unique_segments_count(df):
        return df.text.nunique()

    @staticmethod
    @st.cache_data
    def get_total_words_corpus(df):
        word_count = df["full_text"].str.split().str.len()
        return word_count.sum()

    @staticmethod
    @st.cache_data
    def get_sentences_skewness(df):
        word_count = df["clean_text"].str.split().str.len()
        return skew(word_count)

    @staticmethod
    @st.cache_data
    def get_sentiment_statistics(df):
        results = {
            "sentiment_3": df["senti_3"].value_counts(),
            "sentiment_6": df["senti_6"].value_counts(),
        }
        return results

    @st.cache_data
    def get_data_statistics(_self, df):
        results = _self.corpus_metrics.calculate(df)
        return results

    @st.cache_data
    def get_segments_word_statistics(_self, df):
        results = _self.segment_metrics.calculate(df)
        return results

    @st.cache_data
    def most_frequent_words(_self, df, top=10):
        results = _self.vocabulary_analyzer.get_most_frequent_words(
            df, "no_stopwords", top
        )
        return results
