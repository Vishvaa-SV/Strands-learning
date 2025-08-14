# master_test_runner.py
import os
from dotenv import load_dotenv
from strands import Agent, tool
from strands.models.mistral import MistralModel
import falcon_tools

# Load API key
load_dotenv()
MISTRAL_KEY = os.getenv("MISTRAL_API_KEY")

# ---------------- Wrapping all tools ----------------

@tool
async def log_trade(symbol: str, price: float, qty: float, side: str="buy", note: str=""):
    return await falcon_tools.log_trade(symbol, price, qty, side, note)

@tool
async def get_trade_history(symbol: str):
    return await falcon_tools.get_trade_history(symbol)

@tool
async def get_trade_summary(symbol: str):
    summary = await falcon_tools.get_trade_summary(symbol)
    return f"{summary['symbol']} → Buys: {summary['total_buys']}, Sells: {summary['total_sells']}, Net: {summary['net_position']}"

@tool
async def get_trade_notes(symbol: str):
    trades = await falcon_tools.get_trade_history(symbol)
    return [{"timestamp": t["timestamp"], "note": t.get("note","")} for t in trades]

@tool
async def get_portfolio_value(prices: dict):
    return await falcon_tools.get_portfolio_value(prices)

@tool
async def get_trade_pnl(symbol: str, current_price: float):
    return await falcon_tools.get_trade_pnl(symbol, current_price)

@tool
async def suggest_position_size(account_balance: float, risk_percent: float, entry_price: float, stop_loss_price: float):
    return await falcon_tools.suggest_position_size(account_balance, risk_percent, entry_price, stop_loss_price)

@tool
async def simple_moving_average(prices: list, period: int):
    return await falcon_tools.simple_moving_average(prices, period)

@tool
async def get_ob_suggestion(symbol: str):
    return await falcon_tools.get_ob_suggestion(symbol)

# ---------------- Initialize Agent ----------------
model = MistralModel(api_key=MISTRAL_KEY, model_id="mistral-large-latest")

agent = Agent(model=model, tools=[
    log_trade, get_trade_history, get_trade_summary, get_trade_notes,
    get_portfolio_value, get_trade_pnl, suggest_position_size,
    simple_moving_average, get_ob_suggestion
])

# ---------------- Example Queries ----------------
queries = [
    "Log 0.5 BTC at 28000, add note 'test trade', then show BTC history, summary, and notes.",
    "Calculate portfolio value if BTC=30000, ETH=2000, DOGE=0.1 and show PnL for BTC at 29000.",
    "Suggest position size for a $10,000 account risking 2% with entry 2000 and stop-loss 1950.",
    "Get OB suggestion for BTC and log trade accordingly.",
    "Compute 5-day SMA for ETH prices [1800, 1820, 1850, 1870, 1900]."
]

# ---------------- Run Queries ----------------
for q in queries:
    print(f"\n--- Query: {q} ---")
    result = agent(q)
    print(result)
