import streamlit as st
import pandas as pd
from utils.aggregators import aggregate_words


class WordAnalysisSection:
    def __init__(self, text_analyzer, chart_builder):
        self.text_analyzer = text_analyzer
        self.chart_builder = chart_builder

    def render(self, pre_processed_df):

        top_n = st.number_input(
            "Top N words", min_value=5, max_value=20, value=10, step=5
        )

        most_frequent = self.text_analyzer.most_frequent_words(
            pre_processed_df, top=top_n
        )

        freq_df = pd.DataFrame(most_frequent, columns=["Word", "Frequency"])
        freq_df.index = freq_df.index + 1
        st.dataframe(freq_df, width="stretch")

    def render_chart(self, df, filters):
        aggregator = lambda: aggregate_words(df, filters)
        chart_fn = lambda x: self.chart_builder.build_word_count_bar_chart(x)
        self.chart_builder.display_chart(aggregator, chart_fn)
