import os
from dotenv import load_dotenv
from strands import Agent, tool  # Use tool from strands package
from strands.models.mistral import MistralModel
import falcon_tools  # Your sandbox backend

# Load API key
load_dotenv()
MISTRAL_KEY = os.getenv("MISTRAL_API_KEY")

# Wrap falcon_tools functions as Strands tools using @tool
@tool
async def log_trade(symbol: str, price: float, qty: float, side: str = "buy"):
    """
    Log a new trade with symbol, price, quantity, and optional side.
    Returns a confirmation message with trade details.
    """
    return await falcon_tools.log_trade(symbol, price, qty, side)

@tool
async def get_trade_history(symbol: str):
    """
    Retrieve trade history for the specified symbol.
    """
    return await falcon_tools.get_trade_history(symbol)

@tool
async def get_trade_summary(symbol: str):
    """
    Generate a summary of total buys, total sells, and net position.
    """
    return await falcon_tools.get_trade_summary(symbol)

# Initialize the agent
model = MistralModel(api_key=MISTRAL_KEY, model_id="mistral-large-latest")
agent = Agent(model=model, tools=[log_trade, get_trade_history, get_trade_summary])

# Run a test scenario
query = """
Log a buy trade for 0.5 BTC at 28000, then show me BTC trade history and summary.
"""
result = agent(query)

# Print the entire agent result for inspection
print("--- Agent Result ---")
print(result)
