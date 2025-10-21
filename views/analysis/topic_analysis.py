from utils.aggregators import (
    aggregate_count_by_columns,
)


class TopicAnalysisSection:
    def __init__(self, text_analyzer, chart_builder):
        self.text_analyzer = text_analyzer
        self.chart_builder = chart_builder

    def render(self, df, filters):
        aggregator = lambda: aggregate_count_by_columns(
            df,
            filters,
            ["Party_orientation", "Topic"],
            ["Party_orientation", "Topic"],
        )
        chart_fn = (
            lambda x: self.chart_builder.build_count_by_topic_and_orientation_bar_chart(
                x
            )
        )
        self.chart_builder.display_chart(aggregator, chart_fn)

        aggregator = lambda: aggregate_count_by_columns(
            df,
            filters,
            ["Party_orientation", "Topic", "year"],
            ["Party_orientation", "Topic", "year"],
        )
        chart_fn = lambda x: self.chart_builder.build_topics_per_year_chart(x)
        self.chart_builder.display_chart(aggregator, chart_fn)
