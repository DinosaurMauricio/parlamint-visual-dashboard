import streamlit as st
import pandas as pd


class WordAnalysisSection:
    def __init__(self, text_analyzer):
        self.text_analyzer = text_analyzer

    def render(self, pre_processed_df):

        top_n = st.number_input(
            "Top N words", min_value=5, max_value=20, value=10, step=5
        )

        most_frequent = self.text_analyzer.most_frequent_words(
            pre_processed_df, top=top_n
        )

        freq_df = pd.DataFrame(most_frequent, columns=["Word", "Frequency"])
        freq_df.index = freq_df.index + 1
        st.dataframe(freq_df, use_container_width=True)
