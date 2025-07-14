# Black-Scholes Option Pricer & PnL Visualizer

This project replicates a real-world options trader’s workflow. It allows you to price European options, visualize the profit/loss across a range of market conditions, and log each session with traceable identifiers.

---

## Features

- Black-Scholes pricing for Call and Put options
- Delta and Vega calculation
- Dual PnL heatmaps (Call and Put) with a shared color scale
- Adjustable spot price range, volatility range, and PnL color scale
- Session tracking with UUID and timestamp
- Database auto-clears with each new session
- CSV export for:
  - Input parameters
  - PnL heatmap
- Downloadable heatmap as PDF

---

## How to Run

```bash
pip install -r requirements.txt
streamlit run app.py
```

On launch, the database is reset automatically for a clean session.

## Output Files

- `black_scholes.db`: SQLite database logging each session's inputs and heatmap data
- `inputs.csv`: CSV containing the session’s input parameters
- `heatmap_outputs.csv`: Full PnL grid across volatility and spot
- `heatmap_pnl.png`: Downloadable heatmap image
- `heatmap_pnl.pdf`: High-quality printable version of the heatmap

## Use Case

This tool is built to mirror how a trader analyzes option exposure. It can be used for:

- Understanding option payoff sensitivity
- Testing market assumptions
- Preparing model-driven trading decisions
- Logging and exporting trading scenarios

# Motivation

This project was inspired in part by [blackschole.streamlit.app](https://blackschole.streamlit.app/), but designed to go deeper—capturing trader intent, logging data for review, and aligning closer to real desk tools.

## Author

Aaditya Goel
