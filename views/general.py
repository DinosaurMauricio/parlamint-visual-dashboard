import streamlit as st

from config import FILTERS
from data.loader import get_view_options
from ui.charts import ChartBuilder
from utils.aggregators import (
    aggregate_words,
    aggregate_count_by_columns,
)
from utils.text_analyzer import TextAnalyzer


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
                        st.checkbox(str(y), value=select_all, key=f"{key.lower()}_{y}")


def create_view(df, text_df, filters):
    tab = st.selectbox("Choose Insights view", ["Text Overview", "Gender", "Topic"])

    chart_builder = ChartBuilder(filters)
    text_analyzer = TextAnalyzer()

    # processing all the texts could take hours because the amount of text so
    # to speed it up just preprocessed with spaCy in colab

    pre_processed_df = st.session_state.pre_processed_df

    # NOTE: Could be further abstracted but this
    # structure is readable and clear for now.
    if tab == "Text Overview":
        word_count_tab, other_tab = st.tabs(["Word", "Other"])
        with word_count_tab:
            sentences_count = text_analyzer.get_corpus_senteces_count(text_df)
            unique_sentences_count = text_analyzer.get_corpus_unique_sentences_count(
                text_df
            )
            duplicated_sentences = sentences_count - unique_sentences_count
            results = text_analyzer.get_data_statistics(pre_processed_df)

            st.write(f"Sentences in Corpus: {sentences_count}")
            st.write(f"Unique sentences in Corpus: {unique_sentences_count}")
            st.write(f"Duplicate sentences in Corpus: {duplicated_sentences}")

        aggregator = lambda: aggregate_words(df, filters)
        chart_fn = lambda x: chart_builder.build_word_count_bar_chart(x)
        display_chart(aggregator, chart_fn)

    elif tab == "Gender":
        aggregator = lambda: aggregate_count_by_columns(
            df,
            filters,
            ["year", "Speaker_gender"],
            ["year"],
        )
        chart_fn = lambda x: chart_builder.build_gender_by_year_line_chart(x)
        display_chart(aggregator, chart_fn)

    elif tab == "Topic":
        aggregator = lambda: aggregate_count_by_columns(
            df,
            filters,
            ["Party_orientation", "Topic"],
            ["Party_orientation", "Topic"],
        )
        chart_fn = (
            lambda x: chart_builder.build_count_by_topic_and_orientation_bar_chart(x)
        )
        display_chart(aggregator, chart_fn)

        aggregator = lambda: aggregate_count_by_columns(
            df,
            filters,
            ["Party_orientation", "Topic", "year"],
            ["Party_orientation", "Topic", "year"],
        )
        chart_fn = lambda x: chart_builder.build_topics_per_year_chart(x)
        display_chart(aggregator, chart_fn)


def display_chart(
    aggregator, chart, error_message="No data available for the selected filters."
):
    """
    Display a chart based on an aggregator function and a chart function.

    Args:
        aggregator (callable): Function that returns the aggregated DataFrame.
        chart_fn (callable): Function that takes the aggregated DataFrame and returns a Plotly figure.
        error_message (str, optional): Message to display if the aggregated data is empty.
    """
    grouped = aggregator()
    if grouped.empty:
        st.warning(error_message)
    else:
        fig = chart(grouped)
        st.plotly_chart(fig, use_container_width=True)
