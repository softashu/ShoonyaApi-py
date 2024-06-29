import com.ak.shoonya.datas.configuration.BNFDataConfiguration as bnfDataConfig
import com.ak.shoonya.datas.configuration.FinNiftyDataConfiguration as finDataConfig
import com.ak.shoonya.datas.configuration.NiftyDataConfiguration as niftyDataConfig


def buildAndGetSymbols(api):
    symbols = []
    # Upending the nifty 50 option symbols
    symbols = symbols + niftyDataConfig.buildAndGetNifty50OptionSymbols(
        api.get_quotes(exchange=niftyDataConfig.exchange, token=niftyDataConfig.nifty50_symbol))
    # Upending the bank nifty option symbols
    symbols = symbols + bnfDataConfig.buildAndGetBNFOptionSymbols(
        api.get_quotes(exchange=bnfDataConfig.exchange, token=bnfDataConfig.bnf_symbol))
    # Upending the fin nifty option symbols
    symbols = symbols + finDataConfig.buildAndGetFinNiftyOptionSymbols(
        api.get_quotes(exchange=finDataConfig.exchange, token=finDataConfig.fin_nifty_symbol))

    # Put all options in the beginning
    index_symbols = [
        'NSE:Nifty 50',
        'NSE:Nifty Bank',
        'NSE:Nifty Fin Service'
    ]
    symbols = symbols + index_symbols
    print("BELOW IS THE COMPLETE INSTRUMENT LIST")
    print(symbols)
    return symbols
