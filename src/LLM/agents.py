from agno.agent import Agent
from agno.team import Team
from agno.tools.pandas import PandasTools
from agno.tools.googlesearch import GoogleSearchTools
from agno.tools.yfinance import YFinanceTools
from agno.playground import Playground

from src.LLM.models import model
from src.statement_analyser import CustomFinanceData

Financial_Agents = []

news_agent = Agent(
    name="Finance News & Market Agent",
    description="You are a news agent that helps users find the latest news.",
    instructions="You are the Finance News & Market Agent. Fetch the latest relevant"
    " financial and market updates using the tools for specific company asked."
    " Provide concise news highlights with source references. "
    "Avoid personal opinions and keep results factual.",
    tools=[GoogleSearchTools()],
    model=model,
)

Financial_Agents.append(news_agent)

metrics_agent = Agent(
    model=model,
    name="KPI & Metrics Agent",
    description="Performs financial calculations using backend tools.",
    instructions="You are the KPI & Metrics Agent."
    "Given raw financial data, calculate all relevant performance metrics"
    "and ratios using tools provided, and search for formulaes online using"
    "google search tool provided. Ensure all outputs are numerically correct"
    "and formatted as JSON. Do not provide analysis or commentary,"
    " just clean computed values.",
    tools=[PandasTools(), GoogleSearchTools()],
)

Financial_Agents.append(metrics_agent)

analyst_agent = Agent(
    name="Senior Analyst",
    description="Interprets financial data, explains trends, and highlights key insights",
    instructions="You are the Analyst Agent. Your task is to review performance metrics and"
    " provide a concise, professional analysis of trends, variances, and"
    " anomalies. Use financial logic and reasoning to explain the 'why' behind"
    " numbers. Avoid generic language and be precise. You can search online using tools provided",
    tools=[GoogleSearchTools()],
    model=model,
)

Financial_Agents.append(analyst_agent)

manager_agent = Agent(
    name="Assistant to Manager",
    description="An intelligent assistant to provide high-level executive"
    " summaries, recommendations, and strategic viewpoints",
    instructions="You are the Manager Agent. Summarize financial insights"
    " into bullet points suitable for executives. Focus on the big picture,"
    " highlighting risks, opportunities, and strategic recommendations. "
    "Use clear and actionable language.",
    model=model,
)

Financial_Agents.append(manager_agent)


report_agent = Agent(
    name="The Smart Reporter",
    description="Compiles reports, visualizations, and presentations from other agents’ outputs.",
    instructions="You are the Report Generator Agent. Your job is to compile insights, charts, and performance metrics "
    "into a clean report format (PDF or PowerPoint). Focus on formatting"
    " and structuring the information without altering meaning.",
    model=model,
)

Financial_Agents.append(report_agent)

cool_agent = Agent(
    name="Insights and QnA Agent",
    description="Handles subjective or open-ended user questions like “What are the key factors driving our growth?",
    instructions="You are the Insights & Q&A Agent. Answer subjective and"
    "analytical questions by synthesizing data from other agents. Your response must be thoughtful,"
    " concise, and supported by data-driven evidence.",
    model=model,
)

Financial_Agents.append(cool_agent)

data_agent = Agent(
    name="Financial Data Agent",
    model=model,
    description="Fetches raw financial data",
    instructions=[
        "You are the Financial Data Agent. Your job is to retrieve accurate,",
        " up-to-date financial data from tools provided",
        " Never Never summarize or interpret data. Always",
        " prefer balance sheets and financials data",
        "and return results in structured JSON or tabular "
        "format for further processing.",
    ],
    tools=[
        YFinanceTools(
            stock_fundamentals=True,
            income_statements=True,
            key_financial_ratios=True,
        ),
    ],
)
Financial_Agents.append(data_agent)

endpoint = Team(
    name="Query Handler",
    instructions=[
        "You are the Orchestrator Agent. Analyze the user query,"
        " there previous queries if present, and the data provided"
        " along with it.",
        "Than decide which specialized agent or tool to invoke.",
        "Always prioritize tools for calculations and data retrieval",
        " before using LLM reasoning.However if the data is insufficient"
        "do acknowledge that fast For complex queries, break tasks ",
        "into sub-steps and gather responses from multiple agents.",
        "Present findings in a structured, easy-to-follow format",
        "Only output the final consolidated analysis report,",
        "not individual agent responses nor your process to reach the"
        "final outcome.",
    ],
    members=Financial_Agents,
    model=model,
    mode="coordinate",
    monitoring=True,
)


if __name__ == "__main__":
    playground_app = Playground(teams=[endpoint])
    app = playground_app.get_app()
    playground_app.serve("playground:app", reload=True)
