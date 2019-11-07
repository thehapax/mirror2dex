from bts_spread_mapper import setup_bitshares_market, get_bts_ob_data, get_bts_config
from ccxt_helper import get_ccxt_module, get_cex_data
from ascii_plot_helper import dynamic_ascii_plot, format_df_ascii

import pandas as pd
import time, os
import logging

log = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)


if __name__ == '__main__':

    # CEX orderbook
    # symbol = 'BTC/USDT'
    symbol = 'BTS/ETH'
    depth = 5  # how deep do you want to map your orders
    cex_plot_title = "Cointiger Orderbook: " + symbol

    ###
    invert = False
    bar_width = 0.1
    poll_time = 10
    ###

    # update this to reflect your config file
    config_file = "safe/secrets_test.ini"
    ccxt_ex = get_ccxt_module(config_file)

    # set time to UTC
    os.environ['TZ'] = 'UTC'
    time.tzset()

    # bts_symbol = "OPEN.BTC/USD"
    bts_symbol = "BTS/OPEN.ETH"
    bts_market = setup_bitshares_market(bts_symbol)
    bts_plot_title = "Bitshares DEX Orderbook: " + bts_symbol

    while True:
        os.system("clear")
        log.info(time.ctime())

        # cex data
        l2_ob = ccxt_ex.fetch_l2_order_book(symbol=symbol, limit=None)
        ask_df, bid_df = get_cex_data(l2_ob, depth=depth)  # dynamic data
        ob_df = pd.concat([ask_df.head(depth), bid_df.head(depth)])
        ob_df.sort_values('price', inplace=True, ascending=False)
        cex = format_df_ascii(ob_df)
        dynamic_ascii_plot(cex, cex_plot_title)

        # bts data
        bts_df = get_bts_ob_data(bts_market, depth=depth)
        df = format_df_ascii(bts_df)
        dynamic_ascii_plot(df, bts_plot_title)

        time.sleep(3)

