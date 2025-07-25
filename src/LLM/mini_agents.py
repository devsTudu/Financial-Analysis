from src.LLM.models import model
from agno.agent import Agent

from agno.tools.yfinance import YFinanceTools
from agno.tools.pandas import PandasTools
from src.statement_analyser import getFinancialData

data_manager = Agent(
    name="Fetch data for financial analysis",
    description="Fetches raw financial data",
    tools=[YFinanceTools(stock_fundamentals=True)],
    instructions="Use the tool by entering the subject company Ticker Symbol"
    "to get the financial information about the company ,and return results "
    "in structured JSON or tabular format for further processing.",
    model=model,
)
calculator = Agent(
    name="Financial Calculator",
    description="This Agent can calculate financial terms for analysis",
    instructions="Use the tool to calculate the financial ratios required by the user" \
    "return results in structured JSON or tabular format for further processing.",
    tools=[PandasTools()],
    model=model
)


# Chain execution
def chain_agents(query, company):

    data_response = getFinancialData(company)
    calculated = calculator.run(f"Calculate the necessary values from{data_response} that will help you answer '{query}'")
    # Step 2: Pass data to second agent
    analysis_response = calculator.run(
        f"Analyze this financial data: {calculated} and answer the query {query}"
    )

    

    return analysis_response.content


