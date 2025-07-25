from .data_loader import YahooFinance
from pandas import DataFrame
import streamlit as st

yf = YahooFinance()


@st.cache_data
def getFinancials(symbol):
    return yf.get(symbol)

@st.cache_data
def getRatios(symbol):
    return yf.ratios(symbol)


## Not using anymore
def calculate_performance_ratios(data_df: DataFrame):
    """
    Calculates various performance ratios from a transposed balance sheet
      DataFrame.

    Args:
        data_df: A pandas DataFrame containing transposed balance sheet data,
                 with financial line items as columns and years as index.

    Returns:
        A pandas DataFrame with calculated performance ratios.
    """
    # Check the Data Frame
    if data_df.index.dtype == "O":
        data_df = data_df.transpose()

    performance_ratios = DataFrame(index=data_df.index)

    # Calculate Liquidity Ratios
    if "Current Assets" in data_df.columns and "Current Liabilities" in data_df.columns:
        performance_ratios["Current Ratio"] = (
            data_df["Current Assets"] / data_df["Current Liabilities"]
        )
        if "Inventory" in data_df.columns:
            performance_ratios["Quick Ratio"] = (
                data_df["Current Assets"] - data_df["Inventory"]
            ) / data_df["Current Liabilities"]
        if "Cash And Cash Equivalents" in data_df.columns:
            performance_ratios["Cash Ratio"] = (
                data_df["Cash And Cash Equivalents"] / data_df["Current Liabilities"]
            )
        performance_ratios["Working Capital"] = (
            data_df["Current Assets"] - data_df["Current Liabilities"]
        )  # Corrected working capital calculation

    # Calculate Solvency Ratios
    if (
        "Total Liabilities Net Minority Interest" in data_df.columns
        and "Total Assets" in data_df.columns
    ):
        performance_ratios["Debt Ratio"] = (
            data_df["Total Liabilities Net Minority Interest"] / data_df["Total Assets"]
        )
    elif (
        "Total Liabilities" in data_df.columns and "Total Assets" in data_df.columns
    ):  # Fallback for 'Total Liabilities'
        performance_ratios["Debt Ratio"] = (
            data_df["Total Liabilities"] / data_df["Total Assets"]
        )

    # Add more ratios as needed

    return performance_ratios
