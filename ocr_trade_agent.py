import os
import re
from dotenv import load_dotenv
from PIL import Image
import pytesseract

from strands import Agent, tool
from strands.models.mistral import MistralModel
import falcon_tools  # your existing backend

# ---------------- Load API Key ----------------
load_dotenv()
MISTRAL_KEY = os.getenv("MISTRAL_API_KEY")

# ---------------- OCR Tool ----------------
@tool
async def extract_trade_text(image_path: str):
    """
    Extract text from a screenshot using OCR.
    """
    try:
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img)
        return {"status": "success", "extracted_text": text}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# ---------------- Parse & Log Trades ----------------
@tool
async def parse_and_log_trades(extracted_text: str):
    """
    Parse text and log trades in falcon_tools.
    Expected format per line: SYMBOL QTY SIDE PRICE
    Example: BTC 0.5 Buy 28000
    """
    results = []
    for line in extracted_text.splitlines():
        match = re.match(r"(\w+)\s+([\d\.]+)\s+(Buy|Sell)\s+([\d\.]+)", line.strip(), re.I)
        if match:
            symbol, qty, side, price = match.groups()
            trade_result = await falcon_tools.log_trade(symbol, float(price), float(qty), side.lower())
            results.append(trade_result)
    return {"logged_trades": results}

# ---------------- Existing Trade Tools ----------------
@tool
async def get_trade_history(symbol: str):
    return await falcon_tools.get_trade_history(symbol)

@tool
async def get_trade_summary(symbol: str):
    summary = await falcon_tools.get_trade_summary(symbol)
    return f"{summary['symbol']} → Buys: {summary['total_buys']}, Sells: {summary['total_sells']}, Net: {summary['net_position']}"

@tool
async def get_portfolio_value(prices: dict):
    return await falcon_tools.get_portfolio_value(prices)

@tool
async def get_trade_pnl(symbol: str, current_price: float):
    return await falcon_tools.get_trade_pnl(symbol, current_price)

# ---------------- Initialize Agent ----------------
model = MistralModel(api_key=MISTRAL_KEY, model_id="mistral-large-latest")

agent = Agent(model=model, tools=[
    extract_trade_text,
    parse_and_log_trades,
    get_trade_history,
    get_trade_summary,
    get_portfolio_value,
    get_trade_pnl
])

# ---------------- Example Workflow ----------------
query_workflow = """
1. Extract text from 'sample_trade.png'.
2. Parse and log trades from the extracted text.
3. Show BTC trade history and summary.
4. Calculate portfolio value using BTC=30000, ETH=2000, DOGE=0.1.
"""

result = agent(query_workflow)
print(result)
