import streamlit as st
from ui.metrics import DashboardMetrics


class SegmentAnalysisSection:
    def __init__(self, text_analyzer):
        self.text_analyzer = text_analyzer

    def render(self, df):

        number_of_segments = self.text_analyzer.get_number_of_rows(df)
        data = self.text_analyzer.get_segments_word_statistics(df)

        metrics = [
            {"label": "Total Segments", "value": f"{number_of_segments:,}"},
            {"label": "Avg. Length", "value": f"{data["average_length"]:.2f}"},
            {"label": "Max. Length", "value": f"{data["max_len"]}"},
            {"label": "Min. Length", "value": f"{data["min_len"]}"},
            {"label": "Total words", "value": f"{data["total_words"]:,}"},
        ]

        DashboardMetrics.render_metrics_row(metrics)
