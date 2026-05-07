import numpy as np

def calculate_volatility(data):
    returns = data['Close'].pct_change()
    # Usamos .iloc[1:] para evitar el primer valor que siempre es NaN
    volatility = returns.iloc[1:].std() * np.sqrt(252)
    return float(volatility) # Convertimos a float normal para evitar el 'np.float64'

def calculate_sharpe_ratio(data, risk_free_rate=0.01):
    returns = data['Close'].pct_change().iloc[1:]
    # Convertimos la tasa anual a diaria para que la resta sea justa
    daily_rf = (1 + risk_free_rate) ** (1/252) - 1
    
    excess_returns = returns - daily_rf
    sharpe_ratio = (excess_returns.mean() / returns.std()) * np.sqrt(252)
    return float(sharpe_ratio)