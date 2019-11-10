from bitshares.market import Market
from bts_spread_mapper import get_bts_config

config_file = "safe/bitshares.ini"

passphrase, account = get_bts_config(config_file)

market = Market("USD:BTS")
print(market.ticker())
market.bitshares.wallet.unlock(passphrase)
#print(market.sell(50, 1))  # sell 1 USD for 50 BTS/USD, way above current spot exch rate.
