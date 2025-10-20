import streamlit as st


class SentimentAnalysisSection:
    def __init__(self, text_analyzer, chart_builder):
        self.text_analyzer = text_analyzer
        self.chart_builder = chart_builder

    def render(self, df):
        data = self.text_analyzer.get_sentiment_statistics(df)
        col_1, col_2 = st.columns(2)

        with col_1:
            fig = self.chart_builder.build_pie_chart(
                data["sentiment_3"], "Sentiment Distribution (3 Classes)"
            )
            st.plotly_chart(fig)
        with col_2:
            fig = self.chart_builder.build_pie_chart(
                data["sentiment_6"], "Sentiment Distribution (6 Classes)"
            )
            st.plotly_chart(fig)
