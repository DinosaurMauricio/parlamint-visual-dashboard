import streamlit as st

from config import FILTERS
from data.loader import get_view_options
from views.analysis import *
from ui.charts import ChartBuilder

from utils.text_analyzer import TextAnalyzer


class GeneralView:
    @staticmethod
    def create_sidebar(df):
        with st.sidebar:
            st.header("Overview")
            st.session_state.view_selector = st.selectbox(
                "Choose Party Orientation:", get_view_options(df)
            )

            st.header("Filters")
            with st.container(border=True):
                st.markdown("**Select Filters**")

                for filter in FILTERS:
                    header, key = filter
                    with st.expander(header):
                        select_all = st.checkbox(
                            "Select All", value=True, key=f"select_all_{header.lower()}"
                        )
                        st.markdown(f"**Select {header}:**")
                        for y in sorted(df[key].unique()):
                            st.checkbox(
                                str(y), value=select_all, key=f"{key.lower()}_{y}"
                            )

    @staticmethod
    def create_view(df, text_df, filters):
        tab = st.selectbox(
            "Choose Insights view", ["Dataset Overview", "Gender", "Topic", "Party"]
        )

        chart_builder = ChartBuilder(filters)
        text_analyzer = TextAnalyzer()
        sentiment_analysis = SentimentAnalysisSection(text_analyzer, chart_builder)
        segment_analysis = SegmentAnalysisSection(text_analyzer)
        word_analysis = WordAnalysisSection(text_analyzer, chart_builder)
        overview_analysis = OverviewAnalysisSection(text_analyzer)
        gender_analysis = GenderAnalysisSection(text_analyzer, chart_builder)
        topic_analysis = TopicAnalysisSection(text_analyzer, chart_builder)

        # processing all the texts could take hours because the amount of text so
        # to speed it up just preprocessed with spaCy in colab
        pre_processed_df = st.session_state.pre_processed_df

        if tab == "Dataset Overview":
            overview_tab, words_tab, segments_tab, sentiment_tab = st.tabs(
                ["Overview", "Words", "Segments", "Sentiment"]
            )
            with overview_tab:
                overview_analysis.render(text_df, pre_processed_df)

            with words_tab:
                word_analysis.render(pre_processed_df)
                word_analysis.render_chart(df, filters)

            with segments_tab:
                segment_analysis.render(df)

            with sentiment_tab:
                sentiment_analysis.render(df)

        elif tab == "Gender":
            gender_analysis.render(df, filters)

        elif tab == "Topic":
            topic_analysis.render(df, filters)
        # elif tab == "Party":
        #    party_analysis.render(df)
