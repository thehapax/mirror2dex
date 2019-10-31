from ccxt_helper import get_ccxt_module, get_cex_data
import pandas as pd
import logging

from plot_helper import plot_sequence


log = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)


if __name__ == '__main__':

"""
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

    ask_df, bid_df = get_cex_data(l2_ob, depth=depth)  # dynamic data
    ob_df = pd.concat([ask_df.head(depth), bid_df.head(depth)])
    ob_df.sort_values('price', inplace=True, ascending=False)

    print("----- dynamic cex df ------")
    print(ob_df)

    plot_sequence(ob_df, title, symbol, invert, bar_width, poll_time)
"""