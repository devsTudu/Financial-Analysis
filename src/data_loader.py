import yfinance as yf
from pandas import DataFrame
from abc import ABC, abstractmethod

import logging


class data_source(ABC):

    @abstractmethod
    def fetch(self, source) -> DataFrame:
        """Get the raw data in a table format from the source(file/ticker symbol)"""
        pass

    @abstractmethod
    def get(self, source) -> DataFrame:
        """Get a processed version of Balance sheet and financials
        , with standard variables and value scaling"""
        pass

    @abstractmethod
    def ratios(self, source) -> DataFrame:
        """
        Returns the various performance ratios for interpretation
        """
        pass


class YahooFinance(data_source):
    """Using Yahoo Finance as Source of Data"""

    def fetch(self, source) -> DataFrame:
        ticker_symbol: str = source
        company = yf.Ticker(ticker_symbol)
        bs = company.balance_sheet
        fs = company.financials
        data = bs.transpose().join(fs.transpose())
        if len(data):
            return data.transpose()

        logging.warning("Unable to fetch BS for %s" % ticker_symbol)

        if "." not in ticker_symbol:
            # Handling the Indian Ticker Symbols for yfinance
            for suffix in [".BO", ".NS"]:
                data = self.fetch(ticker_symbol + suffix)
                if len(data):
                    return data
        return DataFrame([])

    def get(self, source) -> DataFrame:
        df = self.fetch(source)

        if len(df) < 1:
            logging.error("Unable to fetch data.")
        else:
            df = df / 100_00_00_000
            try:
                df.columns = df.columns.year
            except ValueError:
                logging.warning("The Periods are not defined properly")
        return df

    def ratios(self, source):
        data = self.get(source).transpose()

        ratios = DataFrame(index=data.index)

        # Template stores the formulae (var1, var2, var3) => var1 = var2/var3
        templates = (
            # Profitability Ratios
            ("Gross Profit Margin", "Gross Profit", "Total Revenue"),
            ("Operation Profit Margin", "Operating Income", "Total Revenue"),
            ("Net Profit Margin", "Net Income", "Total Revenue"),
            ("Return on Equity", "Net Income", "Total Revenue"),
            ("Return on Assets", "Net Income", "Stockholders Equity"),
            # Efficiency Ratios
            ("Inventory Turnover Ratio", "Cost Of Revenue", "Inventory"),
            ("Receivables Turnover Ratio", "Total Revenue", "Receivables"),
            # Liability Ratio
            ("Current Ratio", "Current Assets", "Current Liabilities"),
            (
                "Quick Ratio",
                "Cash Cash Equivalents And Short Term Investments",
                "Current Liabilities",
            ),
            ("Cash Ratio", "Cash And Cash Equivalents", "Current Liabilities"),
            ("Operating Cash Flow Ratio", "Operating Income", "Current Liabilities"),
        )

        for forms in templates:
            try:
                ratios[forms[0]] = data[forms[1]] / data[forms[2]]
            except KeyError:
                logging.warning("%s couldnot be calculated", forms[0])

        return ratios.transpose()
