from stock_market_sim import Stock_info, Append_stock
import pickle
import os


def stock_market():
    wallet = pickle.load(open('character_wallet.dat', 'rb'))
    stocks_owned = list(pickle.load(open('stocks_owned.dat', 'rb')))
    stock_purchase_log = pickle.load(open('stock_purchase_log.dat', 'rb'))
    option = int(input('1: Buy Stocks, 2: Sell Stocks, 3: To view purchase history, 4 : To leave'))

    if option == 1:
        stock_ticker = str(input('Enter a stock ticker'))

        buy_stock = Stock_info(stock_ticker)
        price = buy_stock.return_stock_price()

        print(f'{buy_stock.ticker} Costs ', price)
        purchase_amount = int(input(f'How many do you want to buy? Your Wallet: {wallet}'))

        if wallet < purchase_amount * price:
            print('You are too poor!')
            stock_market()
        else:
            wallet = wallet - (purchase_amount * price)
            bought_stocks = Append_stock(price, purchase_amount, stock_ticker)

            # if no stock is in stocks_owned then it will just append the bought shares
            # otherwise it will loop through stocks_owned
            if not stocks_owned:
                stocks_owned.append(bought_stocks.stocks_bought)
            else:
                # looping through the multi-dimensional stock array
                for stock in stocks_owned:

                    if stock_ticker in stock:
                        # fetching the index of the existing stock
                        index = stocks_owned.index(stock)

                        # checking if the matched stock is the same price
                        # helps avoid stocks that are bought for lower getting mixed in with pre-existing shares
                        if stocks_owned[index][0] != price:
                            stocks_owned.append(bought_stocks.stocks_bought)
                        else:
                            # adding the amount of stocks purchased if the ticker already exists in stocks_owned
                            stocks_owned[index][1] += purchase_amount
                        break

            print(f'Purchase completed! Your remaining gold: {wallet}', bought_stocks.stocks_bought)

            # logging purchase
            stock_purchase_log += f'\n{str(bought_stocks.stocks_bought)}'

            # saving the data
            pickle.dump(wallet, open('character_wallet.dat', 'wb'))
            pickle.dump(stocks_owned, open('stocks_owned.dat', 'wb'))
            pickle.dump(stock_purchase_log, open('stock_purchase_log.dat', 'wb'))

            stock_market()

    elif option == 2:
        sell_stock = list(map(int, input(
            f'Choose a stock to sell: {stocks_owned}, type the number the stock is in! 0 - ...\nThen type the amount you wish to sell').split()))
        try:
            # place where the stock is in the list
            stock_slot = sell_stock[0]

            # amount the player wants to sell
            sell_amount = sell_stock[1]

            # total shares owned by player
            shares_owned = stocks_owned[stock_slot][1]

            # fetching the ticker of the stock
            ticker = stocks_owned[stock_slot][2]

            # making new instance of of Stock_info to return current price of the stock bought
            current_stock_price = Stock_info(ticker)

            # live price + bought price
            bought_price = int(stocks_owned[stock_slot][0])
            live_price = current_stock_price.return_stock_price()

        except Exception:
            print('Something was entered incorrectly')
            stock_market()

        confirm_sell = str(
            input(f'Are sure you want to sell y/n? Bought Price: ${bought_price}, Live Price: ${live_price}'))

        # checking if the player has the amount of stocks he wants to sell and if he is sure
        if shares_owned >= sell_amount and confirm_sell == 'y':
            # adding the money the stocks sold for
            sold_total = sell_amount * current_stock_price.return_stock_price()
            wallet = sold_total + wallet

            # deducting the sold stocks
            stocks_owned[stock_slot][1] -= sell_amount
            print(
                f'Stocks have been sold for a total amount of {sold_total}\nBought Price: ${bought_price}, Sold Price: ${live_price}')

            # removing the stock if it the amount is at zero
            if stocks_owned[stock_slot][1] == 0:
                stocks_owned.pop(stock_slot)

            # logging sold stocks
            stock_purchase_log += f'\n {ticker}, ${bought_price}, ${live_price}'

            # saving the data
            pickle.dump(stocks_owned, open('stocks_owned.dat', 'wb'))
            pickle.dump(wallet, open('character_wallet.dat', 'wb'))
            pickle.dump(stock_purchase_log, open('stock_purchase_log.dat', 'wb'))

            stock_market()

        else:
            print(f'Error: You do not own that many shares {shares_owned} / selling canceled')
            stock_market()

    elif option == 3:
        print(f'Here is your Stock history\n{stock_purchase_log}')
        stock_market()
    else:
        stock_market()


# gives you money :)
def add_money():
    bal = pickle.load(open('character_wallet.dat', 'rb'))
    bal += 1
    pickle.dump(bal, open('character_wallet.dat', 'wb'))


# run this function first to get the files
def set_up():
    wallet = 0
    stocks_owned = []
    stock_purchase_log = ''

    # saving player data
    if not os.path.exists('character_name.dat'):
        pickle.dump(wallet, open('character_wallet.dat', 'wb'))
        pickle.dump(stock_purchase_log, open('stock_purchase_log.dat', 'wb'))
        pickle.dump(stocks_owned, open('stocks_owned.dat', 'wb'))
    stock_market()
