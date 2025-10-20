import plotly.express as px
import streamlit as st


class ChartBuilder:
    # TODO: Check if a singleton could benefit

    def __init__(self, filters):
        self.party_active = bool(filters.get("Party_orientation"))

    def build_word_count_bar_chart(self, df):

        args = {
            "x": "year",
            "y": "Words",
            "title": "Total Words by Year"
            + (" and Party Orientation" if self.party_active else ""),
            "labels": {"Words": "Word Count", "year": "Year"},
            "hover_data": ["Topic"],
        }

        if self.party_active:
            args.update({"color": "Party_orientation", "barmode": "group"})

        return px.bar(df, **args)

    def build_gender_by_year_line_chart(self, df):
        return px.line(
            df,
            x="year",
            y="Count",
            color="Speaker_gender",
            markers=True,
            title="Gender Over Time",
        )

    def build_count_by_topic_and_orientation_bar_chart(self, df):
        return px.bar(
            df,
            x="Topic",
            y="Count",
            color="Party_orientation",
            barmode="group",  # shows bars side-by-side
            title="Topic Mentions by Party Orientation",
            labels={"Count": "Number of Mentions", "Topic": "Topic"},
        )

    def build_topics_per_year_chart(self, df):
        return px.bar(
            df,
            x="year",
            y="Count",
            color="Party_orientation",
            barmode="group",
            title="Topics Mentioned per Year by Party",
            hover_data=["Topic"],
            labels={"Count": "Mentions", "year": "Year"},
        )

    def build_pie_chart(self, df, title):
        return px.pie(df, names=df.index, values=df.values, title=title, hole=0.3)

    @staticmethod
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
