import datetime
import ssl
from datetime import timedelta

import pandas as pd
import requests

ssl._create_default_https_context = ssl._create_unverified_context

######PIVOT POINTS##########################
####################__INPUT__#####################

exchange = "NSE"
fin_nifty_symbol = "26037"


def getFinNiftyExpiryDate():
    currentDateTime = datetime.datetime.now()
    fin_nifty_expiry = {
        # weekly
        datetime.datetime(currentDateTime.year, 6, 18).date(): "18JUN24",
        datetime.datetime(currentDateTime.year, 7, 2).date(): "02JUL24",
        datetime.datetime(currentDateTime.year, 7, 9).date(): "09JUL24",
        datetime.datetime(currentDateTime.year, 7, 16).date(): "16JUL24",

        # Monthly
        datetime.datetime(currentDateTime.year, 6, 25).date(): "25JUN24",
        datetime.datetime(currentDateTime.year, 7, 30).date(): "30JUL24",
        datetime.datetime(currentDateTime.year, 8, 27).date(): "27AUG24"
    }

    today = datetime.datetime.now().date()

    for date_key, value in fin_nifty_expiry.items():
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
    token = pd.read_csv(f'https://api.shoonya.com/{exchange}_symbols.txt.zip')
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


# Method used to build and return the list of fin nifty option symbols that may use for data subscription
def buildAndGetFinNiftyOptionSymbols(ltp):
    a = float(ltp['lp'])
    strikeList = []
    symbolList = []
    fin_nifty_current_expiry = getFinNiftyExpiryDate()
    for i in range(-5, 5):
        strike = (int(a / 100) + i) * 100
        strikeList.append(strike)
        strikeList.append(strike + 50)
    # Add CE
    for strike in strikeList:
        ltp_option = "NFO:FINNIFTY" + str(fin_nifty_current_expiry) + "C" + str(strike)
        symbolList.append(ltp_option)
    # Add PE
    for strike in strikeList:
        ltp_option = "NFO:FINNIFTY" + str(fin_nifty_current_expiry) + "P" + str(strike)
        symbolList.append(ltp_option)
        return symbolList
