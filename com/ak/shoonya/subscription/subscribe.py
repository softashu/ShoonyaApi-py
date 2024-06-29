import logging
import os
import sys

import com.ak.shoonya.datas.configuration.SymbolBuilder as sb

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from com.ak.shoonya.Shoonya_aseem.NorenApi import NorenApi
import time
from time import sleep
import threading
from flask import Flask, request

import com.ak.shoonya.datas.configuration.SymbolProcessor as sp

##############################################
#                   INPUT's                  #
##############################################
# NSE:ACC   --> NSE|22
# NSE:NTPC  --> NSE|11630

api = NorenApi()
api.token_setter()
socket_opened = False

############## Start data building ########################################
symbols = sb.buildAndGetSymbols(api)
sp.process_symbols(symbols)

############## Getting data for subscription  ########################################
instruments = sp.getInstrumentList()
symb_token_map = sp.getSymbolTokenMap()

##############################################
#                   SERVER                   #
##############################################
server = Flask(__name__)
LTPDICT = {}


@server.route("/")
def hello_world():
    return 'Welcome you in the world of algo trading with ak trade ....'


# You may test this rout on browser as example :  http://127.0.0.1:4002/ltp?instrument=NFO:BANKNIFTY03JUL24C51200
@server.route("/ltp")
def getLtp():
    global LTPDICT
    try:
        ltp = -1
        instrument = request.args.get('instrument')
        ltp = LTPDICT[symb_token_map[instrument]]
    except KeyError as ke:
        print("Key not found for given instrument {}", instrument)
        return "Key not found for given instrument : " + instrument
    except Exception as ex:
        print("EXCEPTION occurred while getting ltp of given instrument {}", instrument)
        print(ex)
        return "EXCEPTION occurred while getting ltp of given instrument : " + instrument
    return str(ltp)


def startServer():
    print("Inside startServer()")
    server.run(port=4002)


##############################################
#                  SHOONYA                   #
##############################################

# # For debugging enable this
logging.basicConfig(level=logging.DEBUG)


# ################################ Application callbacks
def event_handler_order_update(message):
    print("ORDER : {0}".format(time.strftime('%d-%m-%Y %H:%M:%S')) + str(message))


def event_handler_quote_update(tick):
    try:
        global LTPDICT
        # process tick to update the ltp dictionary
        # it should be in separate thread.
        key = tick['e'] + '|' + tick['tk']
        LTPDICT[key] = tick['lp']
        print(LTPDICT)
    except KeyError as ke:
        logging.log(logging.ERROR, "Key not found error happened for key {} ".format(key))
    except Exception as ex:
        logging.log(logging.ERROR, "Exception - {} occurred while tick processing for key {}".format(ex, key))


def open_callback():
    global socket_opened
    socket_opened = True
    print('app is connected')
    # api.subscribe('NSE|11630', feed_type='d')
    api.subscribe(instruments)


# ####################################  End of callbacks

def get_time(time_string):
    data = time.strptime(time_string, '%d-%m-%Y %H:%M:%S')
    return time.mktime(data)


def main():
    global uid
    global pwd
    global vc
    global app_key
    global imei

    # start of our program
    print(" Main Started ")
    t1 = threading.Thread(target=startServer)
    t1.start()
    sleep(1)

    ret = api.start_websocket(order_update_callback=event_handler_order_update,
                              subscribe_callback=event_handler_quote_update,
                              socket_open_callback=open_callback)
    print("Websocket Sta-----------------------------------")

    sleep(2)
    while True:
        continue

    t1.join()


if __name__ == "__main__":
    main()
