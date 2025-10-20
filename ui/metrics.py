import streamlit as st
import pandas as pd


class DashboardMetrics:

    @staticmethod
    def render_metrics_row(metrics, max_cols_per_row=2):

        for i in range(0, len(metrics), max_cols_per_row):
            cols = st.columns(max_cols_per_row)
            for col, metric in zip(cols, metrics[i : i + max_cols_per_row]):
                with col:
                    st.metric(
                        label=metric.get("label", ""),
                        value=metric.get("value"),
                    )
            st.divider()

    @staticmethod
    def render_dataframe(title, data):
        st.subheader(title)
        st.dataframe(pd.DataFrame(data), hide_index=True, use_container_width=True)
