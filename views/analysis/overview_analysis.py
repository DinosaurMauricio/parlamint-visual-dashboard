import streamlit as st
import pandas as pd

from ui.metrics import DashboardMetrics


class OverviewAnalysisSection:

    def __init__(self, text_analyzer):
        self.text_analyzer = text_analyzer

    def render(self, text_df, pre_processed_df):

        # Calculate metrics
        # word/sentence count
        sentences_count = self.text_analyzer.get_number_of_rows(text_df)
        unique_sentences_count = self.text_analyzer.get_corpus_unique_sentences_count(
            text_df
        )
        duplicated_sentences = sentences_count - unique_sentences_count
        total_words = self.text_analyzer.get_total_words_corpus(text_df)
        # stats
        results = self.text_analyzer.get_data_statistics(pre_processed_df)
        sentence_skewness = self.text_analyzer.get_sentences_skewness(pre_processed_df)
        stopword_percentage = 100 - results["percentage_stop_words"]
        # vocabulary richness
        type_token_ratio = results["total_words"] / total_words

        metrics = [
            {"label": "Total Sentences", "value": f"{sentences_count:,}"},
            {"label": "Unique Sentences", "value": f"{unique_sentences_count:,}"},
            {"label": "Total Words", "value": f"{total_words:,}"},
            {"label": "Vocabulary Size", "value": f"{results['vocab_size']:,}"},
            {"label": "Duplicates", "value": f"{duplicated_sentences:,}"},
            {
                "label": "Avg. Sentence Length",
                "value": f"{results['average_length']:.2f}",
            },
            {"label": "Type-Token Ratio", "value": f"{type_token_ratio:.3f}"},
            {"label": "Skewness", "value": f"{sentence_skewness:.2f}"},
        ]

        DashboardMetrics.render_metrics_row(metrics, max_cols_per_row=4)

        cols = st.columns(2)
        data_stats = {
            "Sentence Length": {
                "Metric": ["Minimum", "Maximum", "Average", "Range"],
                "Value": [
                    results["min_len"],
                    results["max_len"],
                    float(f"{results['average_length']:.2f}"),
                    results["max_len"] - results["min_len"],
                ],
            },
            "Word Statistics": {
                "Metric": [
                    "Total Words",
                    "Without Stopwords",
                    "Stopwords Removed",
                ],
                "Value": [
                    f"{results['total_words']:,}",
                    f"{results['no_stop_words_text']:,}",
                    f"{stopword_percentage:.1f}%",
                ],
            },
        }

        for col, stats in zip(cols, data_stats.items()):
            with col:
                title, data = stats
                DashboardMetrics.render_dataframe(title, data)
