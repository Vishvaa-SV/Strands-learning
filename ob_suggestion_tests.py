# ob_suggestion_tests.py
import os
from dotenv import load_dotenv
from strands import Agent, tool
from strands.models.mistral import MistralModel
import falcon_tools

load_dotenv()
MISTRAL_KEY = os.getenv("MISTRAL_API_KEY")

@tool
async def get_ob_suggestion(symbol: str):
    return await falcon_tools.get_ob_suggestion(symbol)

@tool
async def log_trade(symbol: str, price: float, qty: float, side: str="buy"):
    return await falcon_tools.log_trade(symbol, price, qty, side)

model = MistralModel(api_key=MISTRAL_KEY, model_id="mistral-large-latest")
agent = Agent(model=model, tools=[get_ob_suggestion, log_trade])

query = "Get OB suggestion for BTC and log trade accordingly."
result = agent(query)
print(result)
