# basic_trade_history.py
import os
from dotenv import load_dotenv
from strands import Agent, tool
from strands.models.mistral import MistralModel
import falcon_tools

load_dotenv()
MISTRAL_KEY = os.getenv("MISTRAL_API_KEY")

@tool
async def log_trade(symbol: str, price: float, qty: float, side: str="buy"):
    return await falcon_tools.log_trade(symbol, price, qty, side)

@tool
async def get_trade_history(symbol: str):
    return await falcon_tools.get_trade_history(symbol)

@tool
async def get_trade_summary(symbol: str):
    return await falcon_tools.get_trade_summary(symbol)

model = MistralModel(api_key=MISTRAL_KEY, model_id="mistral-large-latest")
agent = Agent(model=model, tools=[log_trade, get_trade_history, get_trade_summary])

query = "Log 0.5 BTC at 28000, then show BTC history and summary."
result = agent(query)
print(result)
