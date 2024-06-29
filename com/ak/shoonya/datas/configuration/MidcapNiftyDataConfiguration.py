import datetime
import ssl
from datetime import timedelta

import pandas as pd
import requests

ssl._create_default_https_context = ssl._create_unverified_context

######PIVOT POINTS##########################
####################__INPUT__#####################

exchange1 = "NSE"


def getNiftyExpiryDate():
    nifty_expiry = {
        datetime.datetime(2023, 11, 16).date(): "16NOV23",
        datetime.datetime(2023, 11, 23).date(): "23NOV23",
        datetime.datetime(2023, 11, 30).date(): "30NOV23",
        datetime.datetime(2023, 12, 7).date(): "07DEC23",
        datetime.datetime(2023, 12, 14).date(): "14DEC23",
        datetime.datetime(2023, 12, 21).date(): "21DEC23",
        datetime.datetime(2023, 12, 28).date(): "28DEC23",
        datetime.datetime(2024, 1, 4).date(): "04JAN24",
        datetime.datetime(2024, 1, 11).date(): "11JAN24",
        datetime.datetime(2024, 1, 18).date(): "18JAN24",
        datetime.datetime(2024, 1, 25).date(): "25JAN24",
        datetime.datetime(2024, 2, 1).date(): "01FEB24",
        datetime.datetime(2024, 2, 8).date(): "08FEB24",
        datetime.datetime(2024, 2, 15).date(): "15FEB24",
        datetime.datetime(2024, 2, 22).date(): "22FEB24",
        datetime.datetime(2024, 2, 29).date(): "29FEB24",
        datetime.datetime(2024, 3, 7).date(): "07MAR24",
        datetime.datetime(2024, 3, 14).date(): "14MAR24",
        datetime.datetime(2024, 3, 21).date(): "21MAR24",
        datetime.datetime(2024, 3, 28).date(): "28MAR24",
        datetime.datetime(2024, 4, 4).date(): "04APR24",
        datetime.datetime(2024, 4, 10).date(): "10APR24",
        datetime.datetime(2024, 4, 18).date(): "18APR24",
        datetime.datetime(2024, 4, 25).date(): "25APR24",
        datetime.datetime(2024, 5, 2).date(): "02MAY24",
        datetime.datetime(2024, 5, 9).date(): "09MAY24",
        datetime.datetime(2024, 5, 16).date(): "16MAY24",
        datetime.datetime(2024, 5, 23).date(): "23MAY24",
        datetime.datetime(2024, 5, 30).date(): "30MAY24",
        datetime.datetime(2024, 6, 6).date(): "06JUN24",
        datetime.datetime(2024, 6, 13).date(): "13JUN24",
        datetime.datetime(2024, 6, 20).date(): "20JUN24",
        datetime.datetime(2024, 6, 27).date(): "27JUN24",
        datetime.datetime(2024, 7, 4).date(): "04JUL24",
        datetime.datetime(2024, 7, 11).date(): "11JUL24",
        datetime.datetime(2024, 7, 18).date(): "18JUL24",
        datetime.datetime(2024, 7, 25).date(): "25JUL24",
        datetime.datetime(2024, 8, 1).date(): "01AUG24",
        datetime.datetime(2024, 8, 8).date(): "08AUG24",
        datetime.datetime(2024, 8, 14).date(): "14AUG24",
        datetime.datetime(2024, 8, 22).date(): "22AUG24",
        datetime.datetime(2024, 8, 29).date(): "29AUG24",
        datetime.datetime(2024, 9, 5).date(): "05SEP24",
        datetime.datetime(2024, 9, 12).date(): "12SEP24",
        datetime.datetime(2024, 9, 19).date(): "19SEP24",
        datetime.datetime(2024, 9, 26).date(): "26SEP24",
        datetime.datetime(2024, 10, 3).date(): "03OCT24",
        datetime.datetime(2024, 10, 10).date(): "10OCT24",
        datetime.datetime(2024, 10, 17).date(): "17OCT24",
        datetime.datetime(2024, 10, 24).date(): "24OCT24",
        datetime.datetime(2024, 10, 31).date(): "31OCT24",
        datetime.datetime(2024, 11, 7).date(): "07NOV24",
        datetime.datetime(2024, 11, 14).date(): "14NOV24",
        datetime.datetime(2024, 11, 21).date(): "21NOV24",
        datetime.datetime(2024, 11, 28).date(): "28NOV24",
        datetime.datetime(2024, 12, 5).date(): "05DEC24",
        datetime.datetime(2024, 12, 12).date(): "12DEC24",
        datetime.datetime(2024, 12, 19).date(): "19DEC24",
        datetime.datetime(2024, 12, 26).date(): "26DEC24",
        # current week expiry and onward
        datetime.datetime(datetime.date.year, 12, 26).date(): "26DEC24",
    }

    today = datetime.datetime.now().date()

    for date_key, value in nifty_expiry.items():
        if today <= date_key:
            print(value)
            return value


def getBankNiftyExpiryDate():
    banknifty_expiry = {
        datetime.datetime(2023, 11, 15).date(): "15NOV23",
        datetime.datetime(2023, 11, 22).date(): "22NOV23",
        datetime.datetime(2023, 11, 30).date(): "30NOV23",
        datetime.datetime(2023, 12, 6).date(): "06DEC23",
        datetime.datetime(2023, 12, 13).date(): "13DEC23",
        datetime.datetime(2023, 12, 20).date(): "20DEC23",
        datetime.datetime(2023, 12, 28).date(): "28DEC23",
        datetime.datetime(2024, 1, 3).date(): "03JAN24",
        datetime.datetime(2024, 1, 10).date(): "10JAN24",
        datetime.datetime(2024, 1, 17).date(): "17JAN24",
        datetime.datetime(2024, 1, 25).date(): "25JAN24",
        datetime.datetime(2024, 2, 7).date(): "07FEB24",
        datetime.datetime(2024, 2, 14).date(): "14FEB24",
        datetime.datetime(2024, 2, 21).date(): "21FEB24",
        datetime.datetime(2024, 2, 29).date(): "29FEB24",
        datetime.datetime(2024, 3, 6).date(): "06MAR24",
        datetime.datetime(2024, 3, 13).date(): "13MAR24",
        datetime.datetime(2024, 3, 20).date(): "20MAR24",
        datetime.datetime(2024, 3, 27).date(): "27MAR24",
        datetime.datetime(2024, 4, 3).date(): "03APR24",
        datetime.datetime(2024, 4, 10).date(): "10APR24",
        datetime.datetime(2024, 4, 16).date(): "16APR24",
        datetime.datetime(2024, 4, 24).date(): "24APR24",
        datetime.datetime(2024, 4, 30).date(): "30APR24",
        datetime.datetime(2024, 5, 8).date(): "08MAY24",
        datetime.datetime(2024, 5, 15).date(): "15MAY24",
        datetime.datetime(2024, 5, 22).date(): "22MAY24",
        datetime.datetime(2024, 5, 29).date(): "29MAY24",
        datetime.datetime(2024, 6, 5).date(): "05JUN24",
        datetime.datetime(2024, 6, 12).date(): "12JUN24",
        datetime.datetime(2024, 6, 19).date(): "19JUN24",
        datetime.datetime(2024, 6, 26).date(): "26JUN24",
        datetime.datetime(2024, 7, 3).date(): "03JUL24",
        datetime.datetime(2024, 7, 10).date(): "10JUL24",
        datetime.datetime(2024, 7, 16).date(): "16JUL24",
        datetime.datetime(2024, 7, 24).date(): "24JUL24",
        datetime.datetime(2024, 7, 31).date(): "31JUL24",
        datetime.datetime(2024, 8, 7).date(): "07AUG24",
        datetime.datetime(2024, 8, 14).date(): "14AUG24",
        datetime.datetime(2024, 8, 21).date(): "21AUG24",
        datetime.datetime(2024, 8, 28).date(): "28AUG24",
        datetime.datetime(2024, 9, 4).date(): "04SEP24",
        datetime.datetime(2024, 9, 11).date(): "11SEP24",
        datetime.datetime(2024, 9, 18).date(): "18SEP24",
        datetime.datetime(2024, 9, 25).date(): "25SEP24",
        datetime.datetime(2024, 10, 1).date(): "01OCT24",
        datetime.datetime(2024, 10, 9).date(): "09OCT24",
        datetime.datetime(2024, 10, 16).date(): "16OCT24",
        datetime.datetime(2024, 10, 23).date(): "23OCT24",
        datetime.datetime(2024, 10, 30).date(): "30OCT24",
        datetime.datetime(2024, 11, 6).date(): "06NOV24",
        datetime.datetime(2024, 11, 13).date(): "13NOV24",
        datetime.datetime(2024, 11, 20).date(): "20NOV24",
        datetime.datetime(2024, 11, 27).date(): "27NOV24",
        datetime.datetime(2024, 12, 4).date(): "04DEC24",
        datetime.datetime(2024, 12, 11).date(): "11DEC24",
        datetime.datetime(2024, 12, 18).date(): "18DEC24",
        datetime.datetime(2024, 12, 24).date(): "24DEC24",
    }

    today = datetime.datetime.now().date()

    for date_key, value in banknifty_expiry.items():
        if today <= date_key:
            print(value)
            return value


def getFinNiftyExpiryDate():
    finnifty_expiry = {
        datetime.datetime(2024, 2, 20).date(): "20FEB24",
        datetime.datetime(2024, 2, 27).date(): "27FEB24",
        datetime.datetime(2024, 3, 5).date(): "05MAR24",
        datetime.datetime(2024, 3, 12).date(): "12MAR24",
        datetime.datetime(2024, 3, 19).date(): "19MAR24",
        datetime.datetime(2024, 3, 26).date(): "26MAR24",
        datetime.datetime(2024, 4, 2).date(): "02APR24",
        datetime.datetime(2024, 4, 9).date(): "09APR24",
        datetime.datetime(2024, 4, 16).date(): "16APR24",
        datetime.datetime(2024, 4, 23).date(): "23APR24",
        datetime.datetime(2024, 4, 30).date(): "30APR24",
        datetime.datetime(2024, 5, 7).date(): "07MAY24",
        datetime.datetime(2024, 5, 14).date(): "14MAY24",
        datetime.datetime(2024, 5, 21).date(): "21MAY24",
        datetime.datetime(2024, 5, 28).date(): "28MAY24",
        datetime.datetime(2024, 6, 4).date(): "04JUN24",
        datetime.datetime(2024, 6, 11).date(): "11JUN24",
        datetime.datetime(2024, 6, 18).date(): "18JUN24",
        datetime.datetime(2024, 6, 25).date(): "25JUN24",
        datetime.datetime(2024, 7, 2).date(): "02JUL24",
        datetime.datetime(2024, 7, 9).date(): "09JUL24",
        datetime.datetime(2024, 7, 16).date(): "16JUL24",
        datetime.datetime(2024, 7, 23).date(): "23JUL24",
        datetime.datetime(2024, 7, 30).date(): "30JUL24",
        datetime.datetime(2024, 8, 6).date(): "06AUG24",
        datetime.datetime(2024, 8, 13).date(): "13AUG24",
        datetime.datetime(2024, 8, 20).date(): "20AUG24",
        datetime.datetime(2024, 8, 27).date(): "27AUG24",
        datetime.datetime(2024, 9, 3).date(): "03SEP24",
        datetime.datetime(2024, 9, 10).date(): "10SEP24",
        datetime.datetime(2024, 9, 17).date(): "17SEP24",
        datetime.datetime(2024, 9, 24).date(): "24SEP24",
        datetime.datetime(2024, 10, 1).date(): "01OCT24",
        datetime.datetime(2024, 10, 8).date(): "08OCT24",
        datetime.datetime(2024, 10, 15).date(): "15OCT24",
        datetime.datetime(2024, 10, 22).date(): "22OCT24",
        datetime.datetime(2024, 10, 29).date(): "29OCT24",
        datetime.datetime(2024, 11, 5).date(): "05NOV24",
        datetime.datetime(2024, 11, 12).date(): "12NOV24",
        datetime.datetime(2024, 11, 19).date(): "19NOV24",
        datetime.datetime(2024, 11, 26).date(): "26NOV24",
        datetime.datetime(2024, 12, 3).date(): "03DEC24",
        datetime.datetime(2024, 12, 10).date(): "10DEC24",
        datetime.datetime(2024, 12, 17).date(): "17DEC24",
        datetime.datetime(2024, 12, 24).date(): "24DEC24",
        datetime.datetime(2024, 12, 31).date(): "31DEC24",
    }

    today = datetime.datetime.now().date()

    for date_key, value in finnifty_expiry.items():
        if today <= date_key:
            print(value)
            return value


def getIndexSpot(stock):
    if stock == "BANKNIFTY":
        name = "NSE:Nifty Bank"
    elif stock == "NIFTY":
        name = "NSE:Nifty 50"
    elif stock == "FINNIFTY":
        name = "NSE:Nifty Fin Service"

    return name


def getOptionFormat(stock, intExpiry, strike, ce_pe):
    return "NFO:" + str(stock) + str(intExpiry) + str(ce_pe[0]) + str(strike)


def getLTP(instrument):
    url = "http://localhost:4002/ltp?instrument=" + instrument
    try:
        resp = requests.get(url)
    except Exception as e:
        print(e)
    data = resp.json()
    return data


def manualLTP(symbol, api):
    exch = symbol[:3]
    stockname = symbol[4:]
    temp = api.get_quotes(exchange=exch, token=stockname)
    return float(temp['lp'])


def placeOrder(inst, t_type, qty, order_type, price, variety, api, papertrading=0):
    exch = inst[:3]
    symb = inst[4:]
    # paperTrading = 0 #if this is 1, then real trades will be placed
    if (t_type == "BUY"):
        t_type = "B"
    else:
        t_type = "S"

    if (order_type == "MARKET"):
        order_type = "MKT"
        price = 0
    elif (order_type == "LIMIT"):
        order_type = "LMT"

    try:
        if (papertrading == 1):
            print(t_type)
            print(exch)
            print(symb)
            print(qty)
            print(order_type)
            print(price)
            order_id = api.place_order(buy_or_sell=t_type,  # B, S
                                       product_type="I",  # C CNC, M NRML, I MIS
                                       exchange=exch,
                                       tradingsymbol=symb,
                                       quantity=qty,
                                       discloseqty=qty,
                                       price_type=order_type,  # LMT, MKT, SL-LMT, SL-MKT
                                       price=price,
                                       trigger_price=price,
                                       amo="NO",  # YES, NO
                                       retention="DAY"
                                       )
            print(" => ", symb, order_id['norenordno'])
            return order_id['norenordno']

        else:
            order_id = 0
            return order_id

    except Exception as e:
        print(" => ", symb, "Failed : {} ".format(e))


def getHistorical(ticker, interval, duration, api):
    # token = pd.read_csv(f'https://api.shoonya.com/{exchange1}_symbols.txt.zip')
    exch = ticker[:3]
    token = pd.read_csv(f'https://api.shoonya.com/{exch}_symbols.txt.zip')
    stockname = ticker[4:]
    today = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    no_of_days_before = duration
    starting_date = today - timedelta(days=no_of_days_before)
    starting_date = starting_date.timestamp()

    if stockname == "Nifty 50":
        inst = "26000"
    elif stockname == "Nifty Bank":
        inst = "26009"
    elif stockname == "Nifty Fin Service":
        inst = "26037"
    elif stockname == "NIFTY MID SELECT":
        inst = "26074"
    else:
        inst = str(token[token['TradingSymbol'] == stockname]['Token'].values[0])
        print(inst)
    # inst = token[token.TradingSymbol==stockname].Token.values[0]
    # print(inst)
    # inst = str(inst)
    # for j in range(0,len(token)):
    #    if(token['TradingSymbol'][j] == stockname):
    #        inst = str(token['Token'][j])
    #        time.sleep(1)
    #        break
    # print(inst)

    print(starting_date)
    print(interval)
    hist_data = api.get_time_price_series(exchange=exch, token=inst, starttime=starting_date, interval=1)
    hist_data = pd.DataFrame(hist_data)
    print(hist_data)

    # hist_data = hist_data.sort_values(by='time', ascending=True)
    hist_data = hist_data.reset_index(drop=True)

    # hist_data.columns = ['status','Date','Interval open','Interval high','Interval low','Interval close','Interval vwap','Interval volume','volume','Interval io change','oi']
    # for i in range(0,hist_data['Current epoch time'].size):
    #   hist_data['Current epoch time'][i] = datetime.fromtimestamp(int(hist_data['Current epoch time'][i]))

    reversed_df = hist_data.iloc[::-1]
    reversed_df = reversed_df.reset_index(drop=True)
    new_column_names = {'into': 'open', 'inth': 'high', 'intl': 'low', 'intc': 'close', 'intv': 'volume',
                        'intoi': 'openinterest'}
    reversed_df.rename(columns=new_column_names, inplace=True)

    reversed_df['open'] = pd.to_numeric(reversed_df['open'])
    reversed_df['high'] = pd.to_numeric(reversed_df['high'])
    reversed_df['low'] = pd.to_numeric(reversed_df['low'])
    reversed_df['close'] = pd.to_numeric(reversed_df['close'])
    reversed_df['volume'] = pd.to_numeric(reversed_df['volume'])
    reversed_df['openinterest'] = pd.to_numeric(reversed_df['openinterest'])
    reversed_df['datetime2'] = reversed_df['time'].copy()
    reversed_df['time'] = pd.to_datetime(reversed_df['time'], format="%d-%m-%Y %H:%M:%S")
    reversed_df = reversed_df[reversed_df['time'].dt.time >= pd.to_datetime("09:15:00").time()]
    reversed_df = reversed_df.reset_index(drop=True)

    # Set 'datetime' as the index
    reversed_df.set_index('time', inplace=True)
    # Update the format of the datetime index and add 5 hours and 30 minutes for IST
    # reversed_df.index = reversed_df.index.floor('min')  # Floor to minutes
    # print(hist_data)

    # finaltimeframe = str(interval)  + "min"
    if interval < 375:
        finaltimeframe = str(interval) + "min"
    elif interval == 375:
        finaltimeframe = "D"

    # Resample to a specific time frame, for example, 30 minutes
    resampled_df = reversed_df.resample(finaltimeframe).agg({
        'open': 'first',
        'high': 'max',
        'low': 'min',
        'close': 'last',
        'volume': 'sum',
        'datetime2': 'first',
        'openinterest': 'last'
    })

    # If you want to fill any missing values with a specific method, you can use fillna
    # resampled_df = resampled_df.fillna(method='ffill')  # Forward fill

    # print(resampled_df)
    resampled_df = resampled_df.dropna(subset=['open'])
    return resampled_df


def getHistorical_old(ticker, interval, duration, api):
    token = pd.read_csv(f'https://api.shoonya.com/{exchange1}_symbols.txt.zip')
    exch = ticker[:3]
    stockname = ticker[4:]
    today = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    no_of_days_before = duration
    starting_date = today - timedelta(days=no_of_days_before)
    starting_date = starting_date.timestamp()

    if stockname == "Nifty 50":
        inst = "26000"
    elif stockname == "Nifty Bank":
        inst = "26009"
    else:
        inst = token[token.TradingSymbol == stockname].Token.values[0]
        inst = str(inst)
        # for j in range(0,len(token)):
        #    if(token['TradingSymbol'][j] == stockname):
        #        inst = str(token['Token'][j])
        #        time.sleep(1)
        #        break
    # print(inst)

    print(starting_date)
    print(interval)
    hist_data = api.get_time_price_series(exchange=exch, token=inst, starttime=starting_date, interval=interval)
    hist_data = pd.DataFrame(hist_data)
    print(hist_data)

    # hist_data = hist_data.sort_values(by='time', ascending=True)
    hist_data = hist_data.reset_index(drop=True)

    # hist_data.columns = ['status','Date','Interval open','Interval high','Interval low','Interval close','Interval vwap','Interval volume','volume','Interval io change','oi']
    # for i in range(0,hist_data['Current epoch time'].size):
    #   hist_data['Current epoch time'][i] = datetime.fromtimestamp(int(hist_data['Current epoch time'][i]))

    reversed_df = hist_data.iloc[::-1]
    reversed_df = reversed_df.reset_index(drop=True)
    new_column_names = {'into': 'open', 'inth': 'high', 'intl': 'low', 'intc': 'close', 'intv': 'volume', 'intoi': 'oi'}
    reversed_df.rename(columns=new_column_names, inplace=True)
    print(reversed_df)
    return reversed_df
