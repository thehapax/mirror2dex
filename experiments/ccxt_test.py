from ccxt_helper import get_ccxt_module, read_dict, write_dict
import logging
import json

log = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)

# update this to reflect your config file
config_file = "safe/secrets_test.ini"


####### utility methods

def write_dict(l2_ob, file_name):
    """
    write order book to file.
    :param l2_ob:  level 2 order book
    :param file_name:  filanem
    :return: none
    """
    with open(file_name, 'w') as f:
        s = f.write(json.dumps(l2_ob))


def read_dict(file_name):
    """
    read order book from file
    :param file_name: filename
    :return: static orderbook from file read
    """
    with open(file_name, 'r') as f:
        static_ob = json.loads(f.read())
    return static_ob

def test_rw_ob(l2_ob, file_name):
    """
    Test Reading and writing orderbook to file
    :param l2_ob:
    :return:
    """
    # write order book to file.
    # read order book from file
    if file_name is None:
        file_name = 'cex_ob.txt'
    write_dict(l2_ob, file_name)
    static_ob = read_dict(file_name)
    log.info(static_ob)



def get_l2orderbook(symbol):
    ccxt_ex = get_ccxt_module(config_file)
    log.info(f"Fetch Ticker for {symbol} : {ccxt_ex.fetch_ticker(symbol)}\n")
    print(f"Free Balance:", ccxt_ex.fetch_free_balance())
    l2_ob = ccxt_ex.fetch_l2_order_book(symbol=symbol, limit=None)
    return l2_ob


if __name__ == '__main__':

    symbol = 'BTC/USDT'
    # symbol = 'BTS/BTC'
    log.info("symbol: {} ".format(symbol))
    l2_ob = get_l2orderbook(symbol)

    file_name = 'cex_orderbook.txt'
    write_dict(l2_ob, file_name)
    static_ob = read_dict(file_name)
    print(static_ob)

