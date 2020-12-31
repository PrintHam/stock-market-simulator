from yahoo_fin import stock_info


class Stock_info:
    def __init__(self, ticker):
        self.ticker = ticker

    def return_stock_price(self, debug_type=None):
        try:
            stock_price = stock_info.get_live_price(self.ticker)

            if debug_type is None:
                return round(stock_price)
            elif debug_type == 'price':
                print(round(stock_price))

        except Exception:
            print('No stock was found! Try again')

    def return_stock_profits(self, debug_type=None):
        try:
            stock_profit = stock_info.get_earnings(self.ticker)

            if debug_type is None:
                return round(stock_profit)
            elif debug_type == 'profit':
                print(round(stock_profit))

        except Exception:
            print('No stock was found! Try again')

    def return_stock_ticker(self):
        return self.ticker


class Append_stock(object):
    stocks_bought = []

    def __init__(self, price, amount_bought, ticker):
        self.price = price
        self.amount_bought = amount_bought
        self.ticker = ticker

        # self.stocks_bought.append([self.price, self.amount_bought, self.ticker])
        self.stocks_bought.append(self.price)
        self.stocks_bought.append(self.amount_bought)
        self.stocks_bought.append(self.ticker)