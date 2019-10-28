from ccxt_helper import get_ccxt_module, read_dict, write_dict
import logging

log = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)

# update this to reflect your config file
config_file = "safe/secrets_test.ini"


def get_test_l2ob(symbol):
    ccxt_ex = get_ccxt_module(config_file)
    log.info(f"Fetch Ticker for {symbol} : {ccxt_ex.fetch_ticker(symbol)}\n")
    print(f"Free Balance:", ccxt_ex.fetch_free_balance())
    l2_ob = ccxt_ex.fetch_l2_order_book(symbol=symbol, limit=None)
    return l2_ob


if __name__ == '__main__':

    symbol = 'BTC/USDT'
    # symbol = 'BTS/BTC'
    log.info("symbol: {} ".format(symbol))
    l2_ob = get_test_l2ob(symbol)

    file_name = 'cex_orderbook.txt'
    write_dict(l2_ob, file_name)
    static_ob = read_dict(file_name)
#   print(static_ob)
    print(static_ob)

