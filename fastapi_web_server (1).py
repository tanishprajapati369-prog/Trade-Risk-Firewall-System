from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from database import init_db, get_db
from digital_twin import get_or_create_digital_twin
from firewall_engine import evaluate_trade_risk
from strategy_autopsy import calculate_indian_market_costs

app = FastAPI(title="Trade Risk Firewall API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup():
    init_db()

class TradeIntentSchema(BaseModel):
    user_id: int = 1
    symbol: str
    side: str
    qty: float
    entry_price: float
    stop_loss: float
    take_profit: float
    leverage: Optional[int] = 10

class ExecuteTradeSchema(TradeIntentSchema):
    win_probability: float
    verdict: str

@app.post("/api/v1/firewall/check")
def check_trade_risk(intent: TradeIntentSchema):
    conn = get_db()
    twin = get_or_create_digital_twin(conn, intent.user_id)
    conn.close()
    return evaluate_trade_risk(intent.dict(), twin)

@app.post("/api/v1/trades/execute")
def execute_trade(trade: ExecuteTradeSchema):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO trades (user_id, symbol, side, qty, entry_price, stop_loss, take_profit, win_probability, risk_verdict)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (trade.user_id, trade.symbol, trade.side, trade.qty, trade.entry_price, trade.stop_loss, trade.take_profit, trade.win_probability, trade.verdict))
    trade_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return {"status": "SUCCESS", "trade_id": trade_id, "message": "Trade logged."}

@app.get("/api/v1/digital-twin/{user_id}")
def get_user_digital_twin(user_id: int):
    conn = get_db()
    twin = get_or_create_digital_twin(conn, user_id)
    conn.close()
    return twin

@app.get("/api/v1/autopsy/cost-calculator")
def get_trade_cost(trade_value: float, is_options: bool = False):
    return calculate_indian_market_costs(trade_value, is_options)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)