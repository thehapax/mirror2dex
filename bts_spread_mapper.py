from bitshares import BitShares
from bitshares.instance import set_shared_bitshares_instance
from bitshares.market import Market
import pandas as pd
import time, os
import logging

from plot_helper import dynamic_ascii_plot, format_df_ascii

log = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)

def setup_bitshares_market(bts_symbol):
    bitshares_instance = BitShares(
        "wss://siliconvalley.us.api.bitshares.org/ws",
#        "wss://new-york.us.api.bitshares.org/ws",
        nobroadcast=True  # <<--- set this to False when you want to fire!
    )
    set_shared_bitshares_instance(bitshares_instance)
    bts_market = Market(
        bts_symbol,
        bitshares_instance=bitshares_instance
    )
    return bts_market


def get_bts_orderbook_df(ob, type):
    price_vol = list()
    for i in range(len(ob[type])):
        price = ob[type][i]['price']
        vol = ob[type][i]['quote']
        price_vol.append([price, vol['amount']])

    df = pd.DataFrame(price_vol)
    df.columns = ['price', 'vol']
    df['timestamp'] = int(time.time())
    df['type'] = type
    return df


def get_bts_ob_data(bts_market, depth: int):
    # get bitshares order book for current market
    bts_orderbook = bts_market.orderbook(limit=depth)
    ask_df = get_bts_orderbook_df(bts_orderbook, 'asks')
    bid_df = get_bts_orderbook_df(bts_orderbook, 'bids')
    bts_df = pd.concat([ask_df, bid_df])
    bts_df.sort_values('price', inplace=True, ascending=False)
    return bts_df


if __name__ == '__main__':

    # set time to UTC
    os.environ['TZ'] = 'UTC'
    time.tzset()

    depth = 5
    bts_symbol = "OPEN.BTC/USD"
    bts_market = setup_bitshares_market(bts_symbol)
    title = "Bitshares DEX Orderbook: " + bts_symbol

    while True:
        os.system("clear")
        log.info(time.ctime())
        bts_df = get_bts_ob_data(bts_market, depth=depth)
        df = format_df_ascii(bts_df)
        dynamic_ascii_plot(df, title)
        time.sleep(2)
