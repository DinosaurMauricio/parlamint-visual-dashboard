from utils.aggregators import (
    aggregate_count_by_columns,
)


class GenderAnalysisSection:
    def __init__(self, text_analyzer, chart_builder):
        self.text_analyzer = text_analyzer
        self.chart_builder = chart_builder

    def render(self, df, filters):
        aggregator = lambda: aggregate_count_by_columns(
            df,
            filters,
            ["year", "Speaker_gender"],
            ["year"],
        )
        chart_fn = lambda x: self.chart_builder.build_gender_by_year_line_chart(x)
        self.chart_builder.display_chart(aggregator, chart_fn)
