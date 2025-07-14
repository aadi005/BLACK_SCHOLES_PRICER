import math
from scipy.stats import norm

def calculate_pnl(fair_price, purchase_price, quantity=1):
    """
    Calculate profit or loss on an option position.

    Parameters:
        fair_price (float): Current option value
        purchase_price (float): Price paid for the option
        quantity (int): Number of contracts

    Returns:
        float: Total PnL
    """
    return (fair_price - purchase_price) * quantity


def calculate_greeks(spot, strike, time, rate, volatility, option_type='call'):
    """
    Calculate Delta and Vega for a European option.

    Returns:
        dict: { 'delta': float, 'vega': float }
    """
    if time <= 0:
        return {'delta': 0.0, 'vega': 0.0}

    d1 = (math.log(spot / strike) + (rate + 0.5 * volatility**2) * time) / (volatility * math.sqrt(time))

    if option_type == 'call':
        delta = norm.cdf(d1)
    else:
        delta = -norm.cdf(-d1)

    vega = spot * norm.pdf(d1) * math.sqrt(time)

    return {'delta': delta, 'vega': vega}