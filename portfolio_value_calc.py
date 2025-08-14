# portfolio_value_calc.py
import os
from dotenv import load_dotenv
from strands import Agent, tool
from strands.models.mistral import MistralModel
import falcon_tools

load_dotenv()
MISTRAL_KEY = os.getenv("MISTRAL_API_KEY")

@tool
async def get_portfolio_value(prices: dict):
    return await falcon_tools.get_portfolio_value(prices)

@tool
async def get_trade_pnl(symbol: str, current_price: float):
    return await falcon_tools.get_trade_pnl(symbol, current_price)

@tool
async def suggest_position_size(account_balance: float, risk_percent: float, entry_price: float, stop_loss_price: float):
    return await falcon_tools.suggest_position_size(account_balance, risk_percent, entry_price, stop_loss_price)

model = MistralModel(api_key=MISTRAL_KEY, model_id="mistral-large-latest")
agent = Agent(model=model, tools=[get_portfolio_value, get_trade_pnl, suggest_position_size])

query = """
Calculate portfolio value if BTC=30000, ETH=2000, DOGE=0.1.
Show PnL for BTC at 29000.
Suggest position size for $10,000 account risking 2% with entry 2000, stop-loss 1950.
"""
result = agent(query)
print(result)
