class Portfolio:
    def __init__(self):
        self.stocks = {}

    def add_stock(self, symbol, quantity):
        if symbol in self.stocks:
            self.stocks[symbol] += quantity
        else:
            self.stocks[symbol] = quantity

    def calculate_total_value(self, stock_prices):
        total_value = 0
        for symbol, quantity in self.stocks.items():
            total_value += stock_prices.get(symbol, 0) * quantity
        return total_value