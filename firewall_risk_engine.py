def evaluate_trade_risk(trade_intent: dict, digital_twin: dict) -> dict:
    price = trade_intent["entry_price"]
    qty = trade_intent["qty"]
    sl = trade_intent["stop_loss"]
    tp = trade_intent["take_profit"]
    leverage = trade_intent.get("leverage", 10)

    risk = abs(price - sl)
    reward = abs(tp - price)
    rr_ratio = round(reward / risk, 2) if risk > 0 else 1.0

    base_win_prob = digital_twin["win_rate"] * 100.0
    shap_factors = []
    penalty = 0.0

    size_ratio = qty / max(0.1, digital_twin["median_qty"])
    if size_ratio > 2.5:
        shap_factors.append({
            "factor": "Position Oversizing Deviation",
            "impact": "-18.0%",
            "description": f"Trade size ({qty} units) is {round(size_ratio, 1)}x historical median ({digital_twin['median_qty']} units)."
        })
        penalty += 18.0
    else:
        shap_factors.append({
            "factor": "Position Sizing Normal",
            "impact": "+4.0%",
            "description": "Position size aligns with historical median execution."
        })

    if digital_twin["consecutive_losses"] >= 3:
        shap_factors.append({
            "factor": "Revenge Trading Streak Flag",
            "impact": "-15.0%",
            "description": f"Entering trade immediately after {digital_twin['consecutive_losses']} consecutive losses."
        })
        penalty += 15.0

    if leverage > 25:
        shap_factors.append({
            "factor": "Excessive Leverage Flag",
            "impact": "-12.0%",
            "description": f"Leverage set to {leverage}x increases liquidation sensitivity."
        })
        penalty += 12.0

    win_probability = max(15.0, min(88.0, base_win_prob + 10.0 - penalty))
    loss_probability = round(100.0 - win_probability, 1)

    if win_probability >= 52.0:
        verdict = "PROCEED"
    elif win_probability >= 38.0:
        verdict = "REVIEW"
    else:
        verdict = "HIGH RISK"

    return {
        "win_probability": round(win_probability, 1),
        "loss_probability": loss_probability,
        "risk_reward_ratio": f"1 : {rr_ratio}",
        "verdict": verdict,
        "anomaly_score": round(penalty / 100.0, 2),
        "top_shap_factor": shap_factors[0]["description"] if shap_factors else "All checks normal.",
        "shap_breakdown": shap_factors
    }