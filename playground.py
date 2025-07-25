from agno.playground import Playground
from src.LLM.agents import endpoint

playground_app = Playground(teams=[endpoint])
app = playground_app.get_app()

if __name__ == "__main__":
    playground_app.serve("playground:app", reload=True)
