import json
from pandas import DataFrame
import streamlit as st

from agno.tools import Toolkit


from .data_loader import YahooFinance

yf = YahooFinance()


@st.cache_data
def getFinancials(symbol):
    return yf.get(symbol)


@st.cache_data
def getRatios(symbol):
    return yf.ratios(symbol)


def getFinancialData(symbol: str):
    """Use this function to get fundamental data for a given stock symbol yfinance API.

    Args:
        symbol (str): The stock symbol.
    Returns:
        str: JSON string of the financial data
    """

    try:
        data = yf.get(symbol)
        return json.dumps(data.to_json())
    except Exception as e:
        return f"Failed getting Financials for {symbol}"


class CustomFinanceData(Toolkit):
    """
    CustomFinanceData is a toolkit for getting financial data
    and scale the values to 100 crores.
    """

    def getFinancialData(self, symbol: str):
        """Use this function to get fundamental data for a given stock symbol yfinance API.

        Args:
            symbol (str): The stock symbol.
        Returns:
            str: JSON string of the financial data
        """

        try:
            data = yf.get(symbol)
            return json.dumps(data.to_json())
        except Exception as e:
            return f"Failed getting Financials for {symbol}"

