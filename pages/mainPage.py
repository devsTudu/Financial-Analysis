import streamlit as st
import plotly.graph_objects as go

from src.statement_analyser import getRatios, getFinancials

# Main page content
st.markdown("# Main page")
st.sidebar.markdown("# Where all the dashboards lives 📉")

var = st.text_input("Ticker Symbol", "AAPL")
bs = getFinancials(var)
ratio = getRatios(var)

raw, perf_ratio, graphs = st.tabs(['Table',
                                   'Ratios',
                                   "Graphs"])

with raw:
    st.header("The Balance Sheet Table")
    st.badge("In 100 Crores",icon="💵")
    st.table(bs)

with perf_ratio:
    st.header("The Performance Ratios")
    st.badge("In 100 Crores",icon="💵")
    st.table(ratio)

with graphs:
    st.header("Plots are done here")

    # Beautiful grouped bar chart for performance ratios
    st.subheader("Performance Ratios by Year")
    for ratio_name in ratio.index:
        fig = go.Figure()
        fig.add_bar(
            x=ratio.columns,
            y=ratio.loc[ratio_name],
            marker_color='indianred',
            text=round(ratio.loc[ratio_name],3),           # Add labels
            textposition='auto'
        )
        fig.add_trace(
            go.Scatter(
                x=ratio.columns,
                y=ratio.loc[ratio_name],
                mode='lines+markers',
                name='Trend',
                marker=dict(color='royalblue'),
                line=dict(width=2)
            )
        )
        fig.update_layout(
            title=ratio_name,
            xaxis_title="Year",
            yaxis_title="Value",
            template="plotly_white",
            height=350,
            width=700,
            showlegend=False
            )
        st.plotly_chart(fig, use_container_width=True)
    
