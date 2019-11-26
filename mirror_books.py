from bts_spread_mapper import setup_bitshares_market, get_bts_ob_data
from ccxt_helper import get_ccxt_module, get_cex_data
from ascii_plot_helper import dynamic_ascii_plot, format_df_ascii
from arb_helper import get_cex_mirror

import pandas as pd
import time, os
import logging

log = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)

### for matlab gui plot only
#invert = False
#bar_width = 0.1
#poll_time = 10
###

cex_symbol = 'BTS/ETH'
bts_symbol = "BTS/OPEN.ETH"

cex_plot_title = "Cointiger Orderbook: " + cex_symbol
bts_plot_title = "Bitshares DEX Orderbook: " + bts_symbol    


if __name__ == '__main__':

    # set time to UTC
    os.environ['TZ'] = 'UTC'
    time.tzset()

    # update this to reflect your config file
    config_file = "safe/secrets_test.ini"
    ccxt_ex = get_ccxt_module(config_file, 'cointiger')    

    bts_market = setup_bitshares_market(bts_symbol)

    depth = 5  # how deep do you want to map your orders
    # BTS/OPEN.ETH
    bid_bal = 10    # OPEN.ETH
    ask_bal = 10000  # BTS
    
    while True:
        os.system("clear")
        log.info(time.ctime())

        print(cex_plot_title)
        # cex data
        l2_ob = ccxt_ex.fetch_l2_order_book(symbol=cex_symbol, limit=None)
        ask_df, bid_df = get_cex_data(l2_ob, depth=depth)  # dynamic data
        ob_df = pd.concat([ask_df.head(depth), bid_df.head(depth)])
        ob_df.sort_values('price', inplace=True, ascending=False)
        #print(ob_df)
        cex = format_df_ascii(ob_df)
        dynamic_ascii_plot(cex, cex_plot_title)

        # map scaled cex trades to BTS dex
        mirror_plot_title = "Scaled Mirrored CEX Orderbook "
        log.info(mirror_plot_title)
        
        mirror_asks, mirror_bids = get_cex_mirror(ask_df, bid_df, ask_bal, bid_bal)
        if (mirror_asks is not None) and (mirror_bids is not None):
            m_df = pd.concat([mirror_asks, mirror_bids])
            m_df.sort_values('price', inplace=True, ascending=False)
            #print(m_df)

            # adjust column name in mirror df from vol_scaled to be vol
            # or else format_df_ascii won't work properly
            #scaled_mirror = format_df_ascii(m_df)
            #print(scaled_mirror)
            #dynamic_ascii_plot(scaled_mirror, mirror_plot_title)

            # get bts data
            bts_df = get_bts_ob_data(bts_market, depth=depth)
            # print(bts_df)
            # bts_dex = format_df_ascii(bts_df)
            # dynamic_ascii_plot(bts_dex, bts_plot_title)

            # concatenate order books
            new_bts = pd.concat([m_df, bts_df], sort=False) # to help manage legacy
            new_bts.sort_values('price', inplace=True, ascending=False)

            # print(new_bts)
            new_bts_combo = format_df_ascii(new_bts)
            dynamic_ascii_plot(new_bts_combo, "Combined cex mirror to dex")

        time.sleep(3)