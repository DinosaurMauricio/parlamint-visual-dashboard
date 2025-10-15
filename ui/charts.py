import plotly.express as px


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

    def build_pie_chart(self, df, orientation):

        return px.pie(
            df,
            names="Topic",
            values="Count",
            title=f"Topic Mentions by {orientation}",
        )
