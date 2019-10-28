import logging
import os
import configparser
import ccxt
import json

"""
The purpose of this class is to help setup ccxt exchange configuration. 
Also to read and write orderbooks (in dataframe format) to file.
"""

log = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)


def get_exchange_config(config_filename):
    """
    get exchange config based on filename
    :param config_file:
    :return:
    """
    try:
        config_dir = os.path.dirname(__file__)
        parser = configparser.ConfigParser()
        parser.read(os.path.join(config_dir, config_filename))
        exch_ids = parser.sections()
        log.info("exchange ids")
        log.info(exch_ids)
        sec = {section_name: dict(parser.items(section_name)) for section_name in exch_ids}
        return sec
    except (FileNotFoundError, PermissionError, OSError) as e:
        log.error(e)
        pass


def get_exchange(config_sections):
    # need to fix below in order to check for for
    # acceptable exchanges and parameters
    # for now, get 0th exchange
    """
    get ccxt exchange based on configuration file sections
    :param config_sections: api keys and secrets from encrypted config file.
    :return:
    """
    exch_name = list(config_sections)[0]
    apikey = config_sections[exch_name]['api_key']
    secret = config_sections[exch_name]['secret']
    log.info(f"API Key:  {apikey}")
    log.info(f"SECRET: {secret})")

    # coin tiger requires an API key, even if only for ticker data
    # other exchanges do not need the API key unless trading.
    ccxt_ex = getattr(ccxt, exch_name)({
        "apiKey": apikey,
        "secret": secret,
        'timeout': 30000,
        'enableRateLimit': True,
        'verbose': False,
    })
    return ccxt_ex


def get_ccxt_module(config_file):
    """
    instantiate a ccxt module from the config
    :return: ccxt module
    """
    config_sections = get_exchange_config(config_file)
    log.info(config_sections)
    ccxt_ex = get_exchange(config_sections)
    return ccxt_ex


def write_dict(l2_ob, file_name):
    """
    write order book to file.
    :param l2_ob:  level 2 order book
    :param file_name:  filanem
    :return: none
    """
    with open(file_name, 'w') as f:
        s = f.write(json.dumps(l2_ob))


def read_dict(file_name):
    """
    read order book from file
    :param file_name: filename
    :return: static orderbook from file read
    """
    with open(file_name, 'r') as f:
        static_ob = json.loads(f.read())
    return static_ob


