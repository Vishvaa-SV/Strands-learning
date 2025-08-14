# falcon_tools.py
from datetime import datetime

# --- Mock trade history data ---
trade_history = [
    {"symbol": "BTC", "price": 1000, "qty": 1, "side": "buy", "timestamp": "2025-08-01 09:00"},
    {"symbol": "BTC", "price": 1050, "qty": 1, "side": "sell", "timestamp": "2025-08-02 14:30"},
    {"symbol": "ETH", "price": 1800, "qty": 2, "side": "buy", "timestamp": "2025-08-01 10:15"},
    {"symbol": "ETH", "price": 1900, "qty": 1, "side": "sell", "timestamp": "2025-08-03 09:45"},
    {"symbol": "DOGE", "price": 0.08, "qty": 1000, "side": "buy", "timestamp": "2025-08-02 11:00"},
]

# --- Basic trade functions ---
async def log_trade(symbol: str, price: float, qty: float, side: str = "buy", note: str = ""):
    trade = {
        "symbol": symbol.upper(),
        "price": price,
        "qty": qty,
        "side": side.lower(),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "note": note
    }
    trade_history.append(trade)
    return {"status": "success", "trade": trade}

async def get_trade_history(symbol: str):
    return [t for t in trade_history if t["symbol"].lower() == symbol.lower()]

async def get_trade_summary(symbol: str):
    buys = sum(t["qty"] for t in trade_history if t["symbol"].lower() == symbol.lower() and t["side"]=="buy")
    sells = sum(t["qty"] for t in trade_history if t["symbol"].lower() == symbol.lower() and t["side"]=="sell")
    net = buys - sells
    return {"symbol": symbol.upper(), "total_buys": buys, "total_sells": sells, "net_position": net}

# --- Portfolio & PnL ---
async def get_portfolio_value(prices: dict):
    portfolio = {}
    for t in trade_history:
        qty = t["qty"] if t["side"]=="buy" else -t["qty"]
        portfolio[t["symbol"]] = portfolio.get(t["symbol"], 0) + qty
    total_value = sum(portfolio[sym] * prices.get(sym, 0) for sym in portfolio)
    return {"portfolio": portfolio, "total_value": total_value}

async def get_trade_pnl(symbol: str, current_price: float):
    trades = await get_trade_history(symbol)
    pnl = 0
    for t in trades:
        if t["side"]=="buy":
            pnl += (current_price - t["price"]) * t["qty"]
        else:
            pnl += (t["price"] - current_price) * t["qty"]
    net_position = sum(t["qty"] if t["side"]=="buy" else -t["qty"] for t in trades)
    return {"symbol": symbol.upper(), "net_position": net_position, "pnl": pnl}

# --- Risk / Position sizing ---
async def suggest_position_size(account_balance: float, risk_percent: float, entry_price: float, stop_loss_price: float):
    risk_amount = account_balance * (risk_percent / 100)
    qty = risk_amount / abs(entry_price - stop_loss_price)
    return {"position_size": qty}

# --- Simple moving average ---
async def simple_moving_average(prices: list, period: int):
    if len(prices) < period:
        return {"error": "Not enough data"}
    sma = sum(prices[-period:]) / period
    return {"SMA": sma}

# --- OB suggestion (mock) ---
async def get_ob_suggestion(symbol: str):
    return {"symbol": symbol.upper(), "suggestion": "buy", "price": 28000}


# falcon_tools.py (add this at the bottom)
import pytesseract
from PIL import Image

async def extract_trade_text_from_image(image_path: str):
    """
    Extract text from uploaded trade screenshot using OCR.
    """
    try:
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img)
        return {"status": "success", "extracted_text": text}
    except Exception as e:
        return {"status": "error", "message": str(e)}
