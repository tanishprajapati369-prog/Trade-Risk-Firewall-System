def calculate_indian_market_costs(trade_val: float, is_options: bool = False) -> dict:
    stt = trade_val * (0.000125 if not is_options else 0.000625)
    brokerage = min(20.0, trade_val * 0.0003)
    gst = brokerage * 0.18
    exchange_charges = trade_val * 0.0000345
    slippage = trade_val * 0.0005

    return {
        "stt": round(stt, 2),
        "brokerage": round(brokerage, 2),
        "gst": round(gst, 2),
        "exchange_charges": round(exchange_charges, 2),
        "slippage": round(slippage, 2),
        "total_cost": round(stt + brokerage + gst + exchange_charges + slippage, 2)
    }