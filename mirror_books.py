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

#cex_symbol = 'BTS/ETH'
#bts_symbol = "BTS/OPEN.ETH"

cex_symbol = 'BTS/BTC'
bts_symbol = "BTS/OPEN.BTC"


cex_plot_title = "Cointiger Orderbook: " + cex_symbol
bts_plot_title = "Bitshares DEX Orderbook: " + bts_symbol    
cex_dex_title = "Combined Cex mirror to BTS Dex"
mirror_plot_title = "Scaled Mirrored CEX Orderbook"
opp_df_title = "Arb opportunity Dataframe"

# type 1 is scaled mirror, type 2 is exact mirror
scale_type = 2


def scaled_ob_grp(m_df, bts_df):
    """
    combine order book from m_df (cec) and bts_df
    :param m_df:
    :param bts_df:
    :return: new_bts, a dataframe
    """
    # Option #1  concatenate order books (scaled mirror and bts dex)
    new_bts = pd.concat([m_df, bts_df], sort=False) # to help manage legacy
    new_bts.sort_values('price', inplace=True, ascending=False)
    # display info for testing
    # print(new_bts)
    # new_bts_ascii = format_df_ascii(new_bts)
    # dynamic_ascii_plot(new_bts_ascii, cex_dex_title)
    return new_bts
    

def scaled_mirror(mirror_asks, mirror_bids, bts_df):
    """
    Scaled the trades from the cex orderbook to the dex
    order book based on the on balance that the trader has on hand
    combine both order books and turn
    :param mirror_asks: asks from cex orderbook
    :param mirror_bids: bids from cex orderbook
    :param bts_df: order book from bts dex
    :return: new combined order books.
    """
            
    if (mirror_asks is not None) and (mirror_bids is not None):
        # todo: this is the DF that will be placing orders
        #  on the dex in bulk, and then cancelled every X time interval
        #  in order to produce a visual movement in orders
        m_df = pd.concat([mirror_asks, mirror_bids])
        m_df.sort_values('price', inplace=True, ascending=False)
        # print(m_df)
        
        # display scaled mirror by itself
        # scaled_mirror = format_df_ascii(m_df)
        # print(scaled_mirror)
        # dynamic_ascii_plot(scaled_mirror, mirror_plot_title)
                
        # option #1:
        # log.info(mirror_plot_title)
        new_bts_combo = scaled_ob_grp(m_df, bts_df)
        return new_bts_combo


def exact_ob_grp(cex_ask_df, cex_bid_df, bts_df):
    """
    mirror order books as is - no modifications between cex and dex
    :param cex_ask_df:
    :param cex_bid_Df:
    :param bts_df:
    :return:
    """
    # Option #2 concatenate order books (cex and dex) 
    cex_ask_df.loc[cex_ask_df['type'] == 'asks', 'type'] = 'mirror_asks'
    cex_bid_df.loc[cex_bid_df['type'] == 'bids', 'type'] = 'mirror_bids'
    cex_dfs = [cex_ask_df, cex_bid_df]
    new_bts = pd.concat(cex_dfs, sort=False)
    new_bts.sort_values('price', inplace=True, ascending=False)
    # display both order books
    #    new_bts_ascii = format_df_ascii(new_bts)
    #    dynamic_ascii_plot(new_bts_ascii, cex_dex_title)
    return new_bts, bts_df
    

def calc_arb_opp(cex_df, bts_df):
    # todo - change arguments to be 2 separate dfs, mirror_df and dex_df
    """
    Calculate arbitrage opportunity for simple 1 trade strategy
    mirror is from cex, bids/asks from bitshares dex
    look for opportunities twice: [mirror_asks, bids] and [mirror_bids, asks]
    :param combo: combined dataframe
    :return: df with arbitrage trades
    """

    cex_df = cex_df[cex_df['vol'] > vol_floor]
    bts_df = bts_df[bts_df['vol'] > vol_floor]

    # fix the slicing - do we even need to compute PxV here?
    bts_df['PxV'] = bts_df.price*bts_df.vol
    cex_df['PxV'] = cex_df.price*cex_df.vol
    print("-------- bts_df_mirror")
    print(bts_df)
    print("-------- cex_df_mirror")
    print(cex_df)
    cex_df.to_csv("csv/cex_df_mirror.csv", sep=',')

    print(f'order min limit volume: {vol_floor}')
#    limit_df = cex_df[cex_df['vol'] > vol_floor]

    # if cex asks < dex bids, place trade to
    # take cex ask off books with a buy order
    # place ask on dex at bid price to take off books

    # find if any mirror ask < dex bid in type column
    masks = cex_df[cex_df.type == 'mirror_asks']
    dbids = bts_df[bts_df.type == 'bids']
    # dump to file for testing
    masks.to_csv("csv/masks.csv", sep=",")
    dbids.to_csv("csv/dbids.csv", sep=",")

    print("============= opp_ge ")  # bids on dex
    opp_ge = dbids.loc[dbids['price'].ge(masks['price'])] #show bids df where dex bids > cex asks
    print(opp_ge)
    opp_ge.to_csv("csv/opp_ge.csv", sep=',')

    print("============= opp_masks ")  # asks on cex side
    opp_masks = masks.loc[dbids['price'].ge(masks['price'])]  #show ask df where dex bids > cex asks
    print(opp_masks)
    opp_masks.to_csv("csv/opp_masks.csv", sep=',')
    # return collective opportunity here: opp_masks + opp_ge

    # calculate single arb profitability between opp_ge and opp_masks dfs
    # make trade if profit is worth it
    min_ask = opp_masks.loc[opp_masks['price'].idxmin()] # get row with min asking price
    max_bid = opp_ge.loc[opp_ge['price'].idxmax()]

    if min_ask['vol'] < max_bid['vol']:
        volume = min_ask['vol']
    else:
        volume = max_bid['vol']

    bid_price = max_bid['price']
    ask_price = min_ask['price']

    print(f'volume: {volume}, bid_price: {bid_price}, mirror ask: {ask_price}')
    max_profit = volume*(bid_price - ask_price)
    print(f'max profit: {max_profit}, profit_margin: {profit_margin}')

    if (max_profit > profit_margin):
        # take mirror asking price, and sell at dex bid price
        # place mirror ask order on cex, execute bid on dex simultaneously
        direction = 'cex2dex'
        trade_info = {'direction': direction,
                      'volume': volume,
                      'dex_bid': bid_price,
                      'mirror_ask': ask_price}
    else:
        trade_info = {}

    # do above check if possible to do reverse trade
    # find if any dex ask < mirror bids

    return trade_info
    

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

    profit_margin = 10  # minimum percentage profit margin to account for fees (trader needs to calc)
    
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
        # dynamic_ascii_plot(cex, cex_plot_title)
        
        # get bts data
        bts_df = get_bts_ob_data(bts_market, depth=depth)
        bts_dex = format_df_ascii(bts_df)
        # dynamic_ascii_plot(bts_dex, bts_plot_title)

        if scale_type == 1:  # mirror order books
            # option #1:  map scaled cex trades to BTS dex        
            mirror_asks, mirror_bids = get_cex_mirror(cex_ask_df, cex_bid_df, ask_bal, bid_bal)
            combo_df = scaled_mirror(mirror_asks, mirror_bids, bts_df)
        elif scale_type == 2: # exact order books
            # option #2: exact mirror, no scaling
            cex_df, bts_df = exact_ob_grp(cex_ask_df, cex_bid_df, bts_df)

            trade_info = calc_arb_opp(cex_df, bts_df)
            if not trade_info:
                print(" make trade, data is not empty")

#            ct_symbol = cex_symbol.replace('/', '').lower()
#            side_type = 'buy'  #buy on cex, sell on dex
#            order_id, code_resp = ct_place_order(api_key, bid_price, vol, ct_symbol, side_type)

            #opp_ascii = format_df_ascii(opp_df)
            #dynamic_ascii_plot(opp_ascii, opp_df_title)
            
        time.sleep(3)
