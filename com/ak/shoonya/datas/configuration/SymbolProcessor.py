import pandas as pd

instrumentList = []
symb_token_map = {}
symbolMasterMap = {}


def getSymbolMaster(exch):
    return symbolMasterMap.get(exch)

# exch = "NFO"
# token = pd.read_csv(f'https://api.shoonya.com/{exch}_symbols.txt.zip')

# Tokenization of All symbols as token required to fetch data from exchange or broker terminals ###########

########################################################################

def process_symbols(symbols):
    for i in range(len(symbols)):
        symbol = symbols[i]
        exch = symbol[:3]
        name = symbol[4:]
        symbol_master = getSymbolMaster(exch)

        # building one time symbol master data
        if symbol_master is None:
            symbol_master = pd.read_csv(f'https://api.shoonya.com/{exch}_symbols.txt.zip')
            symbolMasterMap[exch] = symbol_master
        try:
            if name == "Nifty 50":
                inst = exch + "|" + "26000"
                symb_token_map[symbols[i]] = inst
            elif name == "Nifty Bank":
                inst = exch + "|" + "26009"
                symb_token_map[symbols[i]] = inst
            elif name == "Nifty Fin Service":
                inst = exch + "|" + "26037"
                symb_token_map[symbols[i]] = inst
            else:
                token = str(symbol_master[symbol_master['TradingSymbol'] == name]['Token'].values[0])
                inst = exch + "|" + token
                symb_token_map[symbols[i]] = inst
        except IndexError as e:
            print("Skipping while tokenization of symbol with name : ", name)
    #  Generating map of all valid symbols with token
    for symb in symbols:
        if symb in symb_token_map:
            instrumentList.append(symb_token_map[symb])
    print(symb_token_map)
    print('------------------------')
    print(instrumentList)


def getInstrumentList():
    return instrumentList


def getSymbolTokenMap():
    return symb_token_map
