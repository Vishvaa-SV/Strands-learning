# explore_strands.py (final)
import os
from dotenv import load_dotenv
from strands import Agent
from strands.models.mistral import MistralModel
from strands.tools import tool
import falcon_tools

# Load .env
load_dotenv()
MISTRAL_KEY = os.getenv("MISTRAL_API_KEY")

# tools
trade_history_tool = tool(
    name="get_trade_history",
    description="Get past trades for a given symbol",
    func=falcon_tools.get_trade_history
)

log_trade_tool = tool(
    name="log_trade",
    description="Log a trade with symbol, price, and quantity",
    func=falcon_tools.log_trade
)

# Model & Agent
model = MistralModel(api_key=MISTRAL_KEY, model_id="mistral-large-latest")
agent = Agent(model=model, tools=[trade_history_tool, log_trade_tool])

# Run
query = "Log a BTC trade at price 28000 for 0.5 BTC, then show me my BTC trade history"
result = agent(query)

# Debug full object
print("=== Raw AgentResult ===")
print(result)

# Some versions store text under `result['output']`
if isinstance(result, dict) and "output" in result:
    print("\n=== Agent Output ===")
    print(result["output"])
else:
    print("\nNo `output` field found — printing as string:")
    print(str(result))
