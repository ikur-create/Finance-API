import requests
from api.yahoo_finance import YahooFinanceAPI
from models.portfolio import Portfolio

def basic():
    # Initialize the portfolio
    portfolio = Portfolio()
    
    # Example: Add stocks to the portfolio
    portfolio.add_stock('AAPL', 10)
    portfolio.add_stock('GOOGL', 5)
    portfolio.add_stock('TSLA', 5)
    


    # Fetch data for each stock in the portfolio
    api = YahooFinanceAPI()
    for stock in portfolio.stocks:
        data = api.fetch_data(stock)
        risk_metrics = api.get_risk_metrics(data)
        
        print(f"\n--- Informe de Riesgo: {stock} ---")
        for metrica, valor in risk_metrics.items():
            # Convertimos el valor de NumPy a un float de Python puro
            valor_num = float(valor)
            
            if metrica.lower() == 'sharpe_ratio':
                # El Sharpe Ratio es un índice, se suele mostrar con 2 decimales
                print(f"  > {metrica.replace('_', ' ').title()}: {valor_num:.2f}")
            else:
                # Volatilidad y retornos se entienden mejor como porcentaje
                print(f"  > {metrica.replace('_', ' ').title()}: {valor_num:.2%}")

if __name__ == "__basic__":
    basic()