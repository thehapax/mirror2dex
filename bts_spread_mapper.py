import pandas as pd
from bitshares import BitShares
from bitshares.instance import set_shared_bitshares_instance
from bitshares.market import Market
import time
import logging

log = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)

def setup_bitshares_market(bts_symbol):
    bitshares_instance = BitShares(
        "wss://losangeles.us.api.bitshares.org/ws",
        nobroadcast=True  # <<--- set this to False when you want to fire!
    )
    set_shared_bitshares_instance(bitshares_instance)
    bts_market = Market(
        bts_symbol,
        bitshares_instance=bitshares_instance
    )
    return bts_market


def get_bts_orderbook_df(ob, type, inversion: bool):
    price_vol = list()
    if inversion:
        for i in range(len(ob[type])):
            price = ob[type][i]['price']
            invert_price = 1/price
            vol = ob[type][i]['quote']
            vol2 = ob[type][i]['base']  # is this the actual volume?
            price_vol.append([price, vol['amount'], vol2['amount'], invert_price])

        df = pd.DataFrame(price_vol)
        df.columns = ['price', 'vol', 'vol_base', 'invert']
    else:
        for i in range(len(ob[type])):
            price = ob[type][i]['price']
            invert_price = 1/price
            vol = ob[type][i]['quote']
            price_vol.append([price, vol['amount'], invert_price])
        df = pd.DataFrame(price_vol)
        df.columns = ['price', 'vol', 'invert']

    df['timestamp'] = int(time.time())
    df['type'] = type
    return df


def get_ob_data(bts_market, depth: int, invert: bool):
    # get bitshares order book for current market
    bts_orderbook = bts_market.orderbook(limit=depth)
    ask_df = get_bts_orderbook_df(bts_orderbook, 'asks', invert)
    bid_df = get_bts_orderbook_df(bts_orderbook, 'bids', invert)
    bts_df = pd.concat([ask_df, bid_df])
    bts_df.sort_values('price', inplace=True, ascending=False)
    return bts_df


def append_to_file(txt, file):
    with open(file, 'a') as f:
        f.write(txt)
