import math
from scipy.stats import norm

def black_scholes_price(spot, strike, time, rate, volatility, option_type='call'):
    """
    Calculate the Black-Scholes price of a European option.

    Parameters:
        spot (float): Current stock price (S)
        strike (float): Strike price (K)
        time (float): Time to expiry in years (T)
        rate (float): Risk-free interest rate (r)
        volatility (float): Volatility (σ)
        option_type (str): 'call' or 'put'

    Returns:
        float: Option price
    """

    if time <= 0:
        return max(spot - strike, 0.0) if option_type == 'call' else max(strike - spot, 0.0)

    d1 = (math.log(spot / strike) + (rate + 0.5 * volatility**2) * time) / (volatility * math.sqrt(time))
    d2 = d1 - volatility * math.sqrt(time)

    if option_type == 'call':
        return spot * norm.cdf(d1) - strike * math.exp(-rate * time) * norm.cdf(d2)
    else:
        return strike * math.exp(-rate * time) * norm.cdf(-d2) - spot * norm.cdf(-d1)
