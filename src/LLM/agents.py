from agno.agent import Agent
from agno.tools.pandas import PandasTools
from agno.tools.googlesearch import GoogleSearchTools
from .models import model

data_manager = Agent(
    tools=[PandasTools()],
    instructions=f"Use the table {data.to_dict()} to answer the questions",
    model=model,
    
)

search_agent = Agent(
    tools=[GoogleSearchTools()],
    description="You are a news agent that helps users find the latest news.",
    instructions=[
        "Given a topic by the user, respond with 4 latest news items about that topic.",
        "Search for 10 news items and select the top 4 unique items.",
    ],
    show_tool_calls=True,
    debug_mode=True,
    model=model
)




agent.print_response("What is the current ratio by the company for 2024")
