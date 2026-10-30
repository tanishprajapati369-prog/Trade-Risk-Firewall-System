# Trade Risk Firewall — AI-Powered Exchange & Pre-Trade Risk Engine

Trade Risk Firewall is an artificial intelligence-driven decision-support layer and trading platform inspired by the **Delta Exchange** UI. It evaluates trades before capital is committed to identify behavioral anomalies, leverage risks, and portfolio concentration.

## File Structure

```text
trade-risk-firewall/
├── index.html            # Frontend Delta Exchange trading desk & charts
├── main.py               # FastAPI server REST endpoints
├── firewall_engine.py    # AI Pre-Trade Risk Engine & SHAP explainability
├── digital_twin.py       # Behavioral Digital Twin profile generator
├── strategy_autopsy.py   # Strategy Autopsy & Indian tax/cost model
├── database.py           # SQLite database schema & queries
└── requirements.txt      # Python dependencies
```

## How to Run Locally

1. **Install Backend Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Start the FastAPI Server**:
   ```bash
   python main.py
   ```

3. **Launch Frontend**:
   Open `index.html` directly in any web browser to use the interactive exchange and pre-trade firewall!
