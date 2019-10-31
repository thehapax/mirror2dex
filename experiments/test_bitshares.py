from bitshares import BitShares
from bitshares.instance import set_shared_bitshares_instance
from bitshares.market import Market
import pandas as pd
import time, os
import logging

# testing with ascii graph
from ascii_graph import Pyasciigraph
from ascii_graph.colors import *

log = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)


# ascii CLI graph - order book coloring for primary order book red/green.
# colors for your mirror orders, yellow/blue
ob_color = {'asks': Red, 'bids': Gre, 'mirror_asks': Yel, 'mirror_bids': Blu}


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


def dynamic_ascii_plot(bts_market, title):
    graph = Pyasciigraph(
        line_length=120,
        min_graph_length=50,
        separator_length=4,
        multivalue=True,
        human_readable='si',
        float_format='{0:,.6f}')

    # loop forever, keep getting latest order book and display
    bts_df = get_bts_ob_data(bts_market, depth=depth)
    df = bts_df[['price', 'vol', 'type']]

    # replace asks and bids with corresponding color
    df.loc[df['type'] == 'asks', 'type'] = ob_color['asks']
    df.loc[df['type'] == 'bids', 'type'] = ob_color['bids']

    # convert to tuple for ascii graph
    tuple_data = [tuple(x) for x in df.values]

    for line in graph.graph(label=title, data=tuple_data):
        log.info(line)

    # display original dataframe orderbook
    # log.info(bts_df)


if __name__ == '__main__':

    # set time to UTC
    os.environ['TZ'] = 'UTC'
    time.tzset()

    depth = 5
    bts_symbol = "OPEN.BTC/USD"
    bts_market = setup_bitshares_market(bts_symbol)
    title = "Dynamic Graph: " + bts_symbol

    while True:
        os.system("clear")
        log.info(time.ctime())
        dynamic_ascii_plot(bts_market, title)
        time.sleep(1)
