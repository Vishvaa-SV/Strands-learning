# trade_summary_formatting.py
import os
from dotenv import load_dotenv
from strands import Agent, tool
from strands.models.mistral import MistralModel
import falcon_tools

load_dotenv()
MISTRAL_KEY = os.getenv("MISTRAL_API_KEY")

@tool
async def get_trade_summary(symbol: str):
    summary = await falcon_tools.get_trade_summary(symbol)
    return f"{summary['symbol']} → Buys: {summary['total_buys']}, Sells: {summary['total_sells']}, Net: {summary['net_position']}"

model = MistralModel(api_key=MISTRAL_KEY, model_id="mistral-large-latest")
agent = Agent(model=model, tools=[get_trade_summary])

query = "Show formatted summary for BTC and ETH."
result = agent(query)
print(result)
