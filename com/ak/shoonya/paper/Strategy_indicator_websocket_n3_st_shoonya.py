# DISCLAIMER:
# 1) This sample code is for learning purposes only.
# 2) Always be very careful when dealing with codes in which you can place orders in your account.
# 3) The actual results may or may not be similar to backtested results. The historical results do not guarantee any profits or losses in the future.
# 4) You are responsible for any losses/profits that occur in your account in case you plan to take trades in your account.
# 5) TFU and Aseem Singhal do not take any responsibility of you running these codes on your account and the corresponding profits and losses that might occur.
# 6) The running of the code properly is dependent on a lot of factors such as internet, broker, what changes you have made, etc. So it is always better to keep checking the trades as technology error can come anytime.
# 7) This is NOT a tip providing service/code.
# 8) This is NOT a software. Its a tool that works as per the inputs given by you.
# 9) Slippage is dependent on market conditions.
# 10) Option trading and automatic API trading are subject to market risks

# https://buildmedia.readthedocs.org/media/pdf/technical-analysis-library-in-python/latest/technical-analysis-library-in-python.pdf


import time
from datetime import datetime

import pandas as pd
import pandas_ta as pta  # Pandas TA Libv


def importLibrary():
    global shoonya_broker

    global helper
    global api_connect
    global breeze

    global kc
    global api

    if shoonya_broker == 1:
        from NorenApi import NorenApi
        api = NorenApi()
        api.token_setter()


# If you have any below brokers, then make it 1
shoonya_broker = 1

importLibrary()

stock = "NIFTY"
checkInstrument = helper.getIndexSpot(stock)
# FOR STOCKS UNCOMMENT BELOW
# checkInstrument = stock
timeFrame = 1
qty = 50
tradeCEoption = ""
tradePEoption = ""
papertrading = 0  # If paper trading is 0, then paper trading will be done. If paper trading is 1, then live trade
otm = 0
sl_point = 10
target_point = 10

# order's details dataframe
tradesDF = pd.DataFrame(columns=["Date", "Symbol", "Direction", "Price", "Qty", "PaperTrading"])

x = 1
close = []
opens = []
high = []
low = []
volume = []

st = 0
# 0 means no trde, but want to enter.
# 1 means buy trade.
# 2 means sell trade.
# -1 no trade and dont want to enter.
candle_formed = 0


def findStrikePriceATM(stock, cepe):
    global tradeCEoption
    global tradePEoption
    name = helper.getIndexSpot(stock)

    strikeList = []
    prev_diff = 10000
    closest_Strike = 10000

    if stock == "BANKNIFTY":
        intExpiry = helper.getBankNiftyExpiryDate()
    elif stock == "NIFTY":
        intExpiry = helper.getNiftyExpiryDate()
    elif stock == "FINNIFTY":
        intExpiry = helper.getFinNiftyExpiryDate()
    ######################################################
    # FINDING ATM
    ltp = helper.getLTP(name)

    if stock == "BANKNIFTY":
        closest_Strike = int(round((ltp / 100), 0) * 100)
        print(closest_Strike)

    elif stock == "NIFTY" or stock == "FINNIFTY":
        closest_Strike = int(round((ltp / 50), 0) * 50)
        print(closest_Strike)

    print("closest", closest_Strike)
    closest_Strike_CE = closest_Strike + otm
    closest_Strike_PE = closest_Strike - otm

    atmCE = helper.getOptionFormat(stock, intExpiry, closest_Strike_CE, "CE")
    atmPE = helper.getOptionFormat(stock, intExpiry, closest_Strike_PE, "PE")

    print(atmCE)
    print(atmPE)

    if (cepe == "CE"):
        # BUY AT MARKET PRICE
        print("In CE placeorder")
        oidentry = placeOrder1(atmCE, "BUY", qty, "MARKET", 0, "regular", papertrading)
        tradeCEoption = atmCE
        print("CE Entry OID: ", oidentry)
    else:
        # BUY AT MARKET PRICE
        print("In PE placeorder")
        oidentry = placeOrder1(atmPE, "BUY", qty, "MARKET", 0, "regular", papertrading)
        tradePEoption = atmPE
        print("PE Entry OID: ", oidentry)

    return oidentry


def exitPosition(tradeOption):
    # Sell existing option
    oidentry = placeOrder1(tradeOption, "SELL", qty, "MARKET", 0, "regular", papertrading)
    print("Exit OID: ", oidentry)
    return oidentry


def placeOrder1(inst, t_type, qty, order_type, price, variety, papertrading=0):
    global api_connect
    global breeze
    global fyers
    global api
    global kc
    global alice
    global tradesDF
    print("Trade taken. Symbol: ", inst, " Direction: ", t_type, " Quantity: ", qty)

    dt1 = datetime.now()
    tempLtp = helper.getLTP(inst)
    tradesDF.loc[len(tradesDF.index)] = [dt1, inst, t_type, tempLtp, qty, papertrading]

    if papertrading == 0:
        return 0
    elif (shoonya_broker == 1):
        return helper.placeOrder(inst, t_type, qty, order_type, price, variety, api, papertrading)
    else:
        return helper.placeOrder(inst, t_type, qty, order_type, price, variety, papertrading)


def getHistorical1(ticker, interval, duration):
    global api_connect
    global breeze
    global kc
    global api

    if (shoonya_broker == 1):
        return helper.getHistorical(ticker, interval, duration, api)
    else:
        return helper.getHistorical(ticker, interval, duration)


####################__INPUT__#####################


while x == 1:
    dt1 = datetime.now()

    # Find OHLC at the end of the timeframe
    if dt1.second <= 1 and dt1.minute % timeFrame == 0:
        candle_formed = 1
        data = getHistorical1(checkInstrument, timeFrame, 5)

        print(dt1)
        print(data)

        opens = data['open'].to_numpy()
        high = data['high'].to_numpy()
        low = data['low'].to_numpy()
        close = data['close'].to_numpy()
        volume = data['volume'].to_numpy()
        # ttime = data['date']

        if shoonya_broker == 1:
            opens = [float(x) for x in opens]
            high = [float(x) for x in high]
            low = [float(x) for x in low]
            close = [float(x) for x in close]
            if (volume[-1] != ''):
                volume = [float(x) for x in volume]

        supertrend_val_total = pd.DataFrame(pta.supertrend(pd.Series(high), pd.Series(low), pd.Series(close), 10, 3))

        if supertrend_val_total.empty == False:
            supertrend_val = supertrend_val_total.iloc[-1][0]
            supertrend_val_prev = supertrend_val_total.iloc[-1][-1]
        else:
            supertrend_val = 'nan'
        print("Supertrend: ", supertrend_val)
        time.sleep(1)

    elif candle_formed == 1:
        if st == 0:
            if close[-1] > supertrend_val:
                print('Green Supertrend')
                sl = float(close[-1]) - sl_point
                target = float(close[-1]) + target_point
                st = 1
                oidentry = findStrikePriceATM(stock, "CE")
                # oidentry = placeOrder1( stock, "BUY", qty, "MARKET", 0, "regular",papertrading)  #equity

            elif close[-1] < supertrend_val:
                print('Red Supertrend')
                sl = float(close[-1]) + sl_point
                target = float(close[-1]) - target_point
                st = 2
                oidentry = findStrikePriceATM(stock, "PE")
                # oidentry = placeOrder1( stock, "SELL", qty, "MARKET", 0, "regular",papertrading) #equity
            else:
                print("No Entry Yet. Current Second", dt1.second)
                time.sleep(0.5)

        # IN BUY TRADE
        elif st == 1:
            if close[-1] <= sl:
                print('SL Hit')
                st = 0
                oidexit = exitPosition(tradeCEoption)
                # oidexit = placeOrder1( stock, "SELL", qty, "MARKET", 0, "regular",papertrading)  #equity
            elif close[-1] >= target:
                print('Target hit')
                st = -1
                oidexit = exitPosition(tradeCEoption)
                # oidexit = placeOrder1( stock, "SELL", qty, "MARKET", 0, "regular",papertrading)  #equity
            elif close[-1] < supertrend_val:
                print('Red Supertrend Exit')
                st = 0
                oidexit = exitPosition(tradeCEoption)
                # oidexit = placeOrder1( stock, "SELL", qty, "MARKET", 0, "regular",papertrading)  #equity
            else:
                print("In Buy Trade. No Exit Yet. Current Second", dt1.second)
                time.sleep(0.5)

        # IN SELL TRADE
        elif st == 2:
            if close[-1] >= sl:
                print('SL Hit')
                st = 0
                oidexit = exitPosition(tradePEoption)
                # oidexit = placeOrder1( stock, "BUY", qty, "MARKET", 0, "regular",papertrading)  #equity
            elif close[-1] <= target:
                print('Target hit')
                st = -1
                oidexit = exitPosition(tradePEoption)
                # oidexit = placeOrder1( stock, "BUY", qty, "MARKET", 0, "regular",papertrading)  #equity
            elif close[-1] > supertrend_val:
                print('Green Supertrend Exit')
                st = 0
                oidexit = exitPosition(tradePEoption)
                # oidexit = placeOrder1( stock, "BUY", qty, "MARKET", 0, "regular",papertrading)  #equity
            else:
                print("In Sell Trade. No Exit Yet. Current Second", dt1.second)
                time.sleep(0.5)

        # TIME EXIT
        if (dt1.hour >= 15 and dt1.minute >= 15):
            if st == 2:
                print("EOD Exit")
                # Exit Position
                oidexit = exitPosition(tradePEoption)
                # oidexit = placeOrder1( stock, "BUY", qty, "MARKET", 0, "regular",papertrading)  #equity
            elif st == 1:
                print("EOD Exit")
                # Exit position
                oidexit = exitPosition(tradeCEoption)
                # oidexit = placeOrder1( stock, "SELL", qty, "MARKET", 0, "regular",papertrading)  #equity
            print('End Of the Day')
            x = 2
            break

    else:
        print("Waiting for first candle to form. Current Second", dt1.second)
        time.sleep(0.5)

# ------------Saving the final lists in csv file------------------
tradesDF.to_csv("template_indicator.csv")
