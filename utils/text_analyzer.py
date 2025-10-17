import spacy
import streamlit as st

from patterns.singleton_meta import SingletonMeta


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

    @st.cache_data
    @st.cache_data
    def get_data_statistics(_self, df):
        lengths = []
        vocab = set()

        df["word_count"] = df["clean_text"].str.split().str.len()
        total_words = df["word_count"].sum()
        avg_len = sum(lengths) / len(lengths)
        min_len = min(lengths)
        max_len = max(lengths)
        vocab_size = len(vocab)

        results = {
            "average_length": avg_len,
            "min_len": min_len,
            "max_len": max_len,
            "vocab_size": vocab_size,
        }

        return results
