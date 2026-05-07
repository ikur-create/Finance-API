class Portfolio:
    def __init__(self):
        self._stocks = {}

    @property
    def stocks(self):
        """Return list of stock symbols."""
        return list(self._stocks.keys())

    def add_stock(self, symbol, quantity):
        if symbol in self._stocks:
            self._stocks[symbol] += quantity
        else:
            self._stocks[symbol] = quantity

    def calculate_total_value(self, stock_prices):
        total_value = 0
        for symbol, quantity in self._stocks.items():
            total_value += stock_prices.get(symbol, 0) * quantity
        return total_value