import sqlite3
import uuid
from datetime import datetime
import pandas as pd

DB_FILE = "black_scholes.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS inputs (
        id TEXT PRIMARY KEY,
        timestamp TEXT,
        spot REAL,
        strike REAL,
        time REAL,
        volatility REAL,
        rate REAL,
        purchase_price REAL,
        quantity INTEGER
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS heatmap_outputs (
        calculation_id TEXT,
        option_type TEXT,
        spot REAL,
        volatility REAL,
        pnl REAL,
        FOREIGN KEY(calculation_id) REFERENCES inputs(id)
    )
    """)

    conn.commit()
    conn.close()

def insert_inputs(spot, strike, time, volatility, rate, purchase_price, quantity):
    """
    Insert a new input row and return the generated UUID (calculation ID).
    """
    calc_id = str(uuid.uuid4())
    timestamp = datetime.now().isoformat()

    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        INSERT INTO inputs (id, timestamp, spot, strike, time, volatility, rate, purchase_price, quantity)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (calc_id, timestamp, spot, strike, time, volatility, rate, purchase_price, quantity))
    conn.commit()
    conn.close()
    return calc_id

def insert_heatmap_rows(calc_id, option_type, data_matrix, spot_vals, vol_vals):
    """
    Insert all PnL grid values for a given calculation ID and option type.
    """
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    for i, vol in enumerate(vol_vals):
        for j, spot in enumerate(spot_vals):
            pnl = data_matrix[i][j]
            c.execute("""
                INSERT INTO heatmap_outputs (calculation_id, option_type, spot, volatility, pnl)
                VALUES (?, ?, ?, ?, ?)
            """, (calc_id, option_type, spot, vol, pnl))

    conn.commit()
    conn.close()

def clear_all_data():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("DELETE FROM heatmap_outputs")
    c.execute("DELETE FROM inputs")
    conn.commit()
    conn.close()

def fetch_csv_data():
    conn = sqlite3.connect(DB_FILE)
    inputs_df = pd.read_sql_query("SELECT * FROM inputs", conn)
    heatmap_df = pd.read_sql_query("SELECT * FROM heatmap_outputs", conn)
    conn.close()
    return inputs_df, heatmap_df
