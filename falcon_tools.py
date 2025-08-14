# falcon_tools.py
from datetime import datetime

# --- Mock trade history data ---
trade_history = [
    {"symbol": "BTC", "price": 1000, "qty": 1, "side": "buy",  "timestamp": "2025-08-01 09:00"},
    {"symbol": "BTC", "price": 1050, "qty": 1, "side": "sell", "timestamp": "2025-08-02 14:30"},
    {"symbol": "ETH", "price": 1800, "qty": 2, "side": "buy",  "timestamp": "2025-08-01 10:15"},
    {"symbol": "ETH", "price": 1900, "qty": 1, "side": "sell", "timestamp": "2025-08-03 09:45"},
    {"symbol": "DOGE", "price": 0.08, "qty": 1000, "side": "buy", "timestamp": "2025-08-02 11:00"},
]

# --- Functions (to be exposed as Strands tools) ---

async def get_trade_history(symbol: str):
    """
    Return trades filtered by symbol.
    """
    return [trade for trade in trade_history if trade["symbol"].lower() == symbol.lower()]

async def log_trade(symbol: str, price: float, qty: float, side: str = "buy"):
    """
    Add a trade to the in-memory history.
    """
    trade = {
        "symbol": symbol.upper(),
        "price": price,
        "qty": qty,
        "side": side.lower(),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    trade_history.append(trade)
    return {
        "status": "success",
        "message": f"Logged {side} trade for {qty} {symbol.upper()} at {price}",
        "trade": trade
    }

async def get_portfolio_value(prices: dict):
    """
    Calculate net holdings and portfolio value using provided current prices.
    Example prices: {"BTC": 30000, "ETH": 2000, "DOGE": 0.1}
    """
    portfolio = {}
    for trade in trade_history:
        sym = trade["symbol"]
        qty = trade["qty"] if trade["side"] == "buy" else -trade["qty"]
        portfolio[sym] = portfolio.get(sym, 0) + qty

    total_value = sum(portfolio[sym] * prices.get(sym, 0) for sym in portfolio)
    return {"portfolio": portfolio, "total_value": total_value}

async def get_trade_summary(symbol: str):
    """
    Summarize trades for a symbol: total buys, total sells, net position.
    """
    buys = sum(t["qty"] for t in trade_history if t["symbol"].lower() == symbol.lower() and t["side"] == "buy")
    sells = sum(t["qty"] for t in trade_history if t["symbol"].lower() == symbol.lower() and t["side"] == "sell")
    net = buys - sells
    return {
        "symbol": symbol.upper(),
        "total_buys": buys,
        "total_sells": sells,
        "net_position": net
    }
