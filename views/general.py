import streamlit as st

from config import FILTERS
from data.loader import get_view_options
from views.analysis.overview_analysis import OverviewAnalysisSection
from views.analysis.sentiment_analysis import SentimentAnalysisSection
from views.analysis.segments_analysis import SegmentAnalysisSection
from views.analysis.word_analysis import WordAnalysisSection
from ui.charts import ChartBuilder
from utils.aggregators import (
    aggregate_words,
    aggregate_count_by_columns,
)
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
            "Choose Insights view", ["Dataset Overview", "Gender", "Topic"]
        )

        chart_builder = ChartBuilder(filters)
        text_analyzer = TextAnalyzer()
        sentiment_analysis = SentimentAnalysisSection(text_analyzer, chart_builder)
        segment_analysis = SegmentAnalysisSection(text_analyzer)
        word_analysis = WordAnalysisSection(text_analyzer)
        overview_analysis = OverviewAnalysisSection(text_analyzer)

        # processing all the texts could take hours because the amount of text so
        # to speed it up just preprocessed with spaCy in colab
        pre_processed_df = st.session_state.pre_processed_df

        # NOTE: Could be further abstracted but this
        # structure is readable and clear for now.
        if tab == "Dataset Overview":
            overview_tab, words_tab, segments_tab, sentiment_tab = st.tabs(
                ["Overview", "Words", "Segments", "Sentiment"]
            )
            with overview_tab:
                overview_analysis.render(text_df, pre_processed_df)

            with words_tab:
                word_analysis.render(pre_processed_df)

                aggregator = lambda: aggregate_words(df, filters)
                chart_fn = lambda x: chart_builder.build_word_count_bar_chart(x)
                chart_builder.display_chart(aggregator, chart_fn)

            with segments_tab:
                segment_analysis.render(df)

            with sentiment_tab:
                sentiment_analysis.render(df)

        elif tab == "Gender":
            aggregator = lambda: aggregate_count_by_columns(
                df,
                filters,
                ["year", "Speaker_gender"],
                ["year"],
            )
            chart_fn = lambda x: chart_builder.build_gender_by_year_line_chart(x)
            chart_builder.display_chart(aggregator, chart_fn)

        elif tab == "Topic":
            aggregator = lambda: aggregate_count_by_columns(
                df,
                filters,
                ["Party_orientation", "Topic"],
                ["Party_orientation", "Topic"],
            )
            chart_fn = (
                lambda x: chart_builder.build_count_by_topic_and_orientation_bar_chart(
                    x
                )
            )
            chart_builder.display_chart(aggregator, chart_fn)

            aggregator = lambda: aggregate_count_by_columns(
                df,
                filters,
                ["Party_orientation", "Topic", "year"],
                ["Party_orientation", "Topic", "year"],
            )
            chart_fn = lambda x: chart_builder.build_topics_per_year_chart(x)
            chart_builder.display_chart(aggregator, chart_fn)
