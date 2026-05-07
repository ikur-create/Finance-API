import yfinance as yf

class YahooFinanceAPI:
    def fetch_data(self, symbol):
        stock_data = yf.Ticker(symbol)
        return stock_data.history(period="1y")

    def get_risk_metrics(self, data):
        returns = data['Close'].pct_change().dropna()
        volatility = returns.std() * (252 ** 0.5)  # Annualized volatility
        average_return = returns.mean() * 252  # Annualized average return
        sharpe_ratio = average_return / volatility if volatility != 0 else 0
        return {
            'volatility': volatility,
            'average_return': average_return,
            'sharpe_ratio': sharpe_ratio
        }