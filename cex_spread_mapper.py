import pandas as pd
from ccxt_helper import get_ccxt_module
from plot_helper import plot_sequence

import logging

log = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)

def get_cex_data(l2, depth: int):
    # let ob stand for orderbook, ob_depth is the order book depth we want to map out

    bids = l2['bids']
    bid_df = pd.DataFrame(bids)
    bid_df.columns = ['price', 'vol']
    bid_df['invert'] = 1/bid_df['price']
    bid_df['timestamp'] = l2['timestamp']
    bid_df['type'] = 'bids'

    ask = l2['asks']
    ask_df = pd.DataFrame(ask)
    ask_df.columns = ['price', 'vol']
    ask_df['invert'] = 1/ask_df['price']
    ask_df['timestamp'] = l2['timestamp']
    ask_df['type'] = 'asks'

    ob_df = pd.concat([ask_df.head(depth), bid_df.head(depth)])
    ob_df.sort_values('price', inplace=True, ascending=False)
    return ob_df


if __name__ == '__main__':

    # CEX orderbook
    symbol = 'BTC/USDT'
    depth = 5 # how deep do you want to map your orders
    title = "cex orderbook"
    invert = False
    bar_width = 0.1
    poll_time = 10

    # update this to reflect your config file
    config_file = "safe/secrets_test.ini"
    ccxt_ex = get_ccxt_module(config_file)
    l2_ob = ccxt_ex.fetch_l2_order_book(symbol=symbol, limit=None)
    cex_df = get_cex_data(l2_ob, depth=depth)  # dynamic data

    print("----- dynamic cex df ------")
    print(cex_df)

    plot_sequence(cex_df, title, symbol, invert, bar_width, poll_time)
