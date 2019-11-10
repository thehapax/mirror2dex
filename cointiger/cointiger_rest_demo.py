import time
import logging
from cointiger_sdk import cointiger
from cointiger_sdk import const
#from test_encrypt_config import get_exchange_config, get_by_strategy_name
from configparser import ConfigParser, NoOptionError


log = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)

def get_exchange_config(content):
    try:
        parser = ConfigParser()
        parser.read_string(content)
        return parser
    except Exception as e:
        log.error(e)
        pass


def get_by_strategy_name(parser, name):
    section_name = None

    has_section = parser.has_section(name)
    if has_section:
        log.info(f'section_name: {name}')
        section_name = name

    try:
        api_key = parser.get(section_name, 'api_key')
        secret = parser.get(section_name, 'secret')
        exchange_name = parser.get(section_name, 'exchange-name')

        return api_key, secret, exchange_name
    except NoOptionError as e:
        log.error(e)


print(cointiger.timestamp())
all_currencies = cointiger.currencys()
print(all_currencies)  # fees, pairs and min withdrawls listed here.

sname = "ccxt-mirror"
config_file = "../safe/secrets_test2.ini"

with open(config_file, 'r') as enc_file:
    plain_text = enc_file.read()
    print(plain_text)
    parser = get_exchange_config(plain_text)
    api_key, secret, exchange_name = get_by_strategy_name(parser, sname)
    log.info( f"strategy-name: {sname}, "
              f"exchange: {exchange_name}, "
              f"api_key: {api_key}, "
              f"secret: {secret}, ")

cointiger.set_key_and_secret(api_key, secret)

order_data = {
    'api_key': api_key,
    'symbol': 'btcusdt',
    'price': '0.01',
    'volume': '1',
    'side': const.SideType.BUY.value,
    'type': const.OrderType.LimitOrder.value,
    'time': int(time.time())
}

log.info("COINTIGER: get signature from order data")
print(cointiger.get_sign(order_data))
log.info("COINTIGER PLACE ORDER")
print(cointiger.order(dict(order_data, **{'sign': cointiger.get_sign(order_data)})))

cancel_data = {
    'api_key': api_key,
    'orderIdList': '{"btcusdt":["1","2"],"ethusdt":["11","22"]}',
    'time': int(time.time()),
}

log.info("COINTIGER BATCH CANCEL")
print(cointiger.batch_cancel(dict(cancel_data, **{'sign': cointiger.get_sign(cancel_data)})))

log.info("COINTIGER orders cancelled")
print(cointiger.orders('btcusdt', 'canceled', int(time.time()), types='buy-market'))
