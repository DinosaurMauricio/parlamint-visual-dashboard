import streamlit as st
from utils.aggregators import (
    aggregate_count_by_columns,
)


class PartyAnalysisSection:
    def __init__(self, text_analyzer, chart_builder):
        self.text_analyzer = text_analyzer
        self.chart_builder = chart_builder

    def render(self, df):
        # TODO: Maybe place this on the side bar...
        use_unique = st.checkbox("Use Unique Elements")

        if use_unique:
            df = df.drop_duplicates(subset=["ID_meta"])
        st.write(df.shape)

        df["Speaker_party"] = df["Speaker_party"].replace("-", "Undefined")
        df["Party_orientation"] = df["Party_orientation"].replace("-", "Undefined")
        political_parties = df[["Speaker_party", "Party_orientation"]].drop_duplicates()

        PartyAnalysisSection.show_party_data(political_parties)

        utterances_per_year_and_orientation = (
            df.groupby(
                [
                    "Speaker_party",
                    "year",
                    "Party_orientation",
                ],
            )
            .size()
            .reset_index(name="Count")
        )

        fig = self.chart_builder.build_speaker_party_per_year_chart(
            utterances_per_year_and_orientation
        )
        st.plotly_chart(fig)

        utterances_per_year = (
            df.groupby(["year", "Party_orientation"]).size().reset_index(name="Count")
        )

        total_utterances_per_orientation = utterances_per_year.groupby(
            "Party_orientation"
        )["Count"].sum()
        fig = self.chart_builder.build_pie_chart(
            total_utterances_per_orientation, "Party Orientation Total Utterances"
        )
        st.plotly_chart(fig)

    @staticmethod
    # TODO: Clean this...
    def show_party_data(df):
        orientations = df["Party_orientation"]
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Parties", len(df))
        with col2:
            st.metric("Orientations", orientations.nunique())

        orientation_options = st.selectbox(
            "Choose Party Orientation:", orientations.unique()
        )
        parties_list = df[df["Party_orientation"] == orientation_options][
            "Speaker_party"
        ].tolist()
        for party in parties_list:
            st.write(f"{party}")
