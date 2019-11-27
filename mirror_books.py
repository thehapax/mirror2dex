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
cex_dex_title = "Combined Cex mirror to BTS Dex"
mirror_plot_title = "Scaled Mirrored CEX Orderbook"
opp_df_title = "Arb opportunity Dataframe"


# type 1 is scaled mirror, type 2 is exact mirror
scale_type = 2


def scaled_ob_grp(m_df, bts_df):
    # Option #1  concatenate order books (scaled mirror and bts dex)
    new_bts = pd.concat([m_df, bts_df], sort=False) # to help manage legacy
    new_bts.sort_values('price', inplace=True, ascending=False)
#   print(new_bts)
    new_bts_ascii = format_df_ascii(new_bts)
    dynamic_ascii_plot(new_bts_ascii, cex_dex_title)
    return new_bts
    

def scaled_mirror(mirror_asks, mirror_bids, bts_df):
            
    if (mirror_asks is not None) and (mirror_bids is not None):
        # todo: this is the DF that will be placing orders
        #  on the dex in bulk, and then cancelled every X time interval
        #  in order to produce a visual movement in orders
        m_df = pd.concat([mirror_asks, mirror_bids])
        m_df.sort_values('price', inplace=True, ascending=False)
        # print(m_df)
        
        # disply scaled mirror by itself
        # scaled_mirror = format_df_ascii(m_df)
        # print(scaled_mirror)
        # dynamic_ascii_plot(scaled_mirror, mirror_plot_title)
                
        # option #1:
        # log.info(mirror_plot_title)
        new_bts_combo = scaled_ob_grp(m_df, bts_df)
        return new_bts_combo


def exact_ob_grp(cex_ask_df, cex_bid_Df, bts_df):
    # Option #2 concatenate order books (cex and dex) 
    cex_ask_df.loc[cex_ask_df['type'] == 'asks', 'type'] = 'mirror_asks'
    cex_bid_df.loc[cex_bid_df['type'] == 'bids', 'type'] = 'mirror_bids'
    all_dfs = [cex_ask_df, cex_bid_df, bts_df]
    new_bts = pd.concat(all_dfs, sort=False)
    new_bts.sort_values('price', inplace=True, ascending=False)

    new_bts_ascii = format_df_ascii(new_bts)
    dynamic_ascii_plot(new_bts_ascii, cex_dex_title)
    return new_bts
    

def calc_arb_opp(combo):
    combo['PxV'] = combo.price*combo.vol
    print(f'limit volume: {vol_floor}')
    limit_vol = combo[combo['vol'] > vol_floor]
    print(limit_vol)
    return limit_vol
    

if __name__ == '__main__':


    # set time to UTC
    os.environ['TZ'] = 'UTC'
    time.tzset()

    # update this to reflect your config file
    config_file = "safe/secrets_test.ini"
    ccxt_ex = get_ccxt_module(config_file, 'cointiger')
    bts_market = setup_bitshares_market(bts_symbol)

    # minimum volume to trade on cex - we set at 350 bts for now
    vol_floor = 160
    
    depth = 5  # how deep do you want to map your orders

    # BTS/OPEN.ETH
    bid_bal = 100    # OPEN.ETH
    ask_bal = 10000  # BTS
    
    while True:
        os.system("clear")
        log.info(time.ctime())

        print(cex_plot_title)
        # cex data
        l2_ob = ccxt_ex.fetch_l2_order_book(symbol=cex_symbol, limit=None)
        cex_ask_df, cex_bid_df = get_cex_data(l2_ob, depth=depth)  # dynamic data
        ob_df = pd.concat([cex_ask_df, cex_bid_df])
        ob_df.sort_values('price', inplace=True, ascending=False)
        #print(ob_df)
        cex = format_df_ascii(ob_df)
#        dynamic_ascii_plot(cex, cex_plot_title)
        
        # get bts data
        bts_df = get_bts_ob_data(bts_market, depth=depth)
        bts_dex = format_df_ascii(bts_df)
#        dynamic_ascii_plot(bts_dex, bts_plot_title)

        combo_df = pd.DataFrame()       
        if scale_type == 1:
            # option #1:  map scaled cex trades to BTS dex        
            mirror_asks, mirror_bids = get_cex_mirror(cex_ask_df, cex_bid_df, ask_bal, bid_bal)
            combo_df = scaled_mirror(mirror_asks, mirror_bids, bts_df)
        elif scale_type == 2:
            # option #2: exact mirror, no scaling
            combo_df = exact_ob_grp(cex_ask_df, cex_bid_df, bts_df)
            opp_df = calc_arb_opp(combo_df)
            opp_ascii = format_df_ascii(opp_df)
            dynamic_ascii_plot(opp_ascii, opp_df_title)
            
        time.sleep(3)
