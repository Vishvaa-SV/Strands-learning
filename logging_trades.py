# logging_trades.py
import os
from dotenv import load_dotenv
from strands import Agent, tool
from strands.models.mistral import MistralModel
import falcon_tools

load_dotenv()
MISTRAL_KEY = os.getenv("MISTRAL_API_KEY")

@tool
async def log_trade(symbol: str, price: float, qty: float, side: str="buy", note: str=""):
    return await falcon_tools.log_trade(symbol, price, qty, side, note)

@tool
async def get_trade_notes(symbol: str):
    trades = await falcon_tools.get_trade_history(symbol)
    return [{"timestamp": t["timestamp"], "note": t.get("note", "")} for t in trades]

model = MistralModel(api_key=MISTRAL_KEY, model_id="mistral-large-latest")
agent = Agent(model=model, tools=[log_trade, get_trade_notes])

query = "Log 1 ETH at 1850 with note 'scalping strategy'. Show notes."
result = agent(query)
print(result)
