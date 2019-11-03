from bitshares import BitShares
from bitshares.instance import set_shared_bitshares_instance
from bitshares.market import Market
import pandas as pd
import time, os
import logging
import configparser

log = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)

"""
Setup config file and methods to get orderbook from bitshares exchange 
"""

# temporary for testing without dexbot only.
def get_bts_config(bts_config_file):
    try:
        config_dir = os.path.dirname(__file__)
        parser = configparser.ConfigParser()
        parser.read(os.path.join(config_dir, bts_config_file))
        info = parser.sections()
        log.info(info)
        config_sections = {section_name: dict(parser.items(section_name)) for section_name in info}

        exch_name = list(config_sections)[0]
        passwd = config_sections[exch_name]['password']
        acct = config_sections[exch_name]['account']
        log.info(f'passwd = {passwd}')
        log.info(f'account = {acct}')
        return passwd, acct
    except (FileNotFoundError, PermissionError, OSError) as e:
        log.error(e)
        pass


def setup_bitshares_market(bts_symbol):
    bitshares_instance = BitShares(
        "wss://siliconvalley.us.api.bitshares.org/ws",
        # "wss://new-york.us.api.bitshares.org/ws",
        nobroadcast=True  # <<--- set this to False when you want to fire!
    )
    bts_config_file = "safe/bitshares.ini"
    bts_passwd, acct= get_bts_config(bts_config_file)
    bitshares_instance.wallet.unlock(bts_passwd)

    set_shared_bitshares_instance(bitshares_instance)
    bts_market = Market(
        bts_symbol,
        bitshares_instance=bitshares_instance
    )
    return bts_market


def get_bts_orderbook_df(ob, type):
    """
    filter bts order book by ask, bids
    return as a dataframe
    :param ob: orderbook as dataframe
    :param type: type of order 'ask' or 'bid'
    :return: dataframe
    """
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
    """
    get bts orderbook and label asks and bids
    :param bts_market: name of bts market
    :param depth: depth of orderbook
    :return: order book filtered and labeled with asks/bids
    """
    # get bitshares order book for current market
    bts_orderbook = bts_market.orderbook(limit=depth)
    ask_df = get_bts_orderbook_df(bts_orderbook, 'asks')
    bid_df = get_bts_orderbook_df(bts_orderbook, 'bids')
    bts_df = pd.concat([ask_df, bid_df])
    bts_df.sort_values('price', inplace=True, ascending=False)
    return bts_df

