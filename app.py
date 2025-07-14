import streamlit as st
import pandas as pd
from pricing import black_scholes_price
from utils import calculate_greeks
from visualize import plot_dual_heatmap
from db import init_db, insert_inputs, insert_heatmap_rows, clear_all_data, fetch_csv_data
from utils import calculate_pnl
import numpy as np
import io

st.set_page_config(page_title="Black-Scholes Option Pricer", layout="wide", initial_sidebar_state="expanded")
init_db()
clear_all_data()

st.title("📈 Black-Scholes Option Pricer & PnL Visualizer")

st.sidebar.header("Enter Option Parameters")

spot = st.sidebar.number_input("Spot Price (S)", value=100.0)
strike = st.sidebar.number_input("Strike Price (K)", value=110.0)
time = st.sidebar.number_input("Time to Expiry (T in years)", value=0.5, min_value=0.01)
volatility = st.sidebar.number_input("Volatility (σ)", value=0.2, min_value=0.01, max_value=1.0, step=0.01)
rate = st.sidebar.number_input("Risk-free Rate (r)", value=0.05, min_value=0.0)
purchase_price = st.sidebar.number_input("Purchase Price (₹)", value=5.0)
quantity = st.sidebar.number_input("Quantity", value=1, min_value=1)


calculation_id = insert_inputs(
    spot=spot,
    strike=strike,
    time=time,
    volatility=volatility,
    rate=rate,
    purchase_price=purchase_price,
    quantity=quantity
)


st.sidebar.markdown("### Heatmap Parameters")

min_spot = st.sidebar.number_input("Min Spot Price", value=0.8 * spot, step=1.0)
max_spot = st.sidebar.number_input("Max Spot Price", value=1.2 * spot, step=1.0)

min_vol = st.sidebar.slider("Min Volatility for Heatmap", 0.01, 1.00, 0.10, step=0.01)
max_vol = st.sidebar.slider("Max Volatility for Heatmap", 0.01, 1.00, 0.30, step=0.01)

st.sidebar.markdown("### Color Scale (PnL)")
vmin = st.sidebar.slider("Min PnL (₹)", -200, 0, -20, step=5)
vmax = st.sidebar.slider("Max PnL (₹)", 0, 200, 20, step=5)



st.markdown("## 🧠 Black-Scholes Pricing Model")
input_data = {
    "Current Asset Price": [spot],
    "Strike Price": [strike],
    "Time to Maturity (Years)": [time],
    "Volatility (σ)": [volatility],
    "Risk-Free Interest Rate": [rate]
}
st.dataframe(pd.DataFrame(input_data), use_container_width=True)

call_price = black_scholes_price(spot, strike, time, rate, volatility, 'call')
put_price = black_scholes_price(spot, strike, time, rate, volatility, 'put')

call_html = f"""
<div style='background-color: #572991; padding: 20px; border-radius: 15px; text-align: center;'>
    <h3 style='margin-bottom: 5px; color: white;'>CALL Value</h3>
    <h2 style='color:white;'>₹{call_price:.2f}</h2>
</div>
"""

put_html = f"""
<div style='background-color: #0A0380; padding: 20px; border-radius: 15px; text-align: center;'>
    <h3 style='margin-bottom: 5px; color: white;'>PUT Value</h3>
    <h2 style='color:white;'>₹{put_price:.2f}</h2>
</div>
"""

col1, col2 = st.columns(2)
with col1:
    st.markdown(call_html, unsafe_allow_html=True)
with col2:
    st.markdown(put_html, unsafe_allow_html=True)

greeks = calculate_greeks(spot, strike, time, rate, volatility, 'call')
st.markdown("### 📐 Greeks for Call Option")

delta_html = f"""
<div style='background-color: #0A0380; padding: 15px; border-radius: 10px; text-align: center;'>
    <h4 style='margin-bottom: 5px; color: white;'>Delta</h4>
    <h3 style='color:white;'>{greeks['delta']:.4f}</h3>
</div>
"""

vega_html = f"""
<div style='background-color: #572991; padding: 15px; border-radius: 10px; text-align: center;'>
    <h4 style='margin-bottom: 5px; color: white;'>Vega</h4>
    <h3 style='color:white;'>{greeks['vega']:.4f}</h3>
</div>
"""


col1, col2 = st.columns(2)
with col1:
    st.markdown(delta_html, unsafe_allow_html=True)
with col2:
    st.markdown(vega_html, unsafe_allow_html=True)


st.markdown("### PnL Heatmaps")
st.caption("Customize Spot and Volatility Ranges in Sidebar")

col1, col2 = st.columns(2)

spot_vals = np.linspace(min_spot, max_spot, 20)
vol_vals = np.linspace(min_vol, max_vol, 20)

call_matrix = np.array([
    [calculate_pnl(black_scholes_price(s, strike, time, rate, v, 'call'), purchase_price, quantity)
     for s in spot_vals]
    for v in vol_vals
])
put_matrix = np.array([
    [calculate_pnl(black_scholes_price(s, strike, time, rate, v, 'put'), purchase_price, quantity)
     for s in spot_vals]
    for v in vol_vals
])

insert_heatmap_rows(calculation_id, 'call', call_matrix, spot_vals, vol_vals)
insert_heatmap_rows(calculation_id, 'put', put_matrix, spot_vals, vol_vals)

fig = plot_dual_heatmap(
    spot_range=(min_spot, max_spot),
    vol_range=(min_vol, max_vol),
    strike=strike,
    time=time,
    rate=rate,
    purchase_price=purchase_price,
    quantity=quantity,
    vmin=vmin,
    vmax=vmax
)
st.pyplot(fig)

buf = io.BytesIO()
pdf_buf = io.BytesIO()
fig.savefig(pdf_buf, format="pdf", bbox_inches="tight", facecolor=fig.get_facecolor())
pdf_buf.seek(0)

st.markdown("### 📥 Export Data")

inputs_df, heatmap_df = fetch_csv_data()

col1, col2 = st.columns(2)

with col1:
    st.download_button(
        label="Download Inputs CSV",
        data=inputs_df.to_csv(index=False).encode('utf-8'),
        file_name="inputs.csv",
        mime="text/csv"
    )

with col2:
    st.download_button(
        label="Download Heatmap PnL CSV",
        data=heatmap_df.to_csv(index=False).encode('utf-8'),
        file_name="heatmap_outputs.csv",
        mime="text/csv"
    )

    st.download_button(
        label="Download Heatmap PDF",
        data=pdf_buf,
        file_name="heatmap_pnl.pdf",
        mime="application/pdf"
    )
