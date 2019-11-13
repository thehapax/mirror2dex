from pprint import pprint
from uptick.decorators import unlock, online
from uptick.main import main
from bitshares.market import Market
import click
import logging

log = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)


@main.command()
@click.option("--account", default=None)
@click.argument("market")
@click.pass_context
@online
@unlock
def cancelall(ctx, market, account):
    """
    Cancel all orders in a market
    :param ctx: context
    :param market: market e.g.
    :param account: name of your bitshares acct
    :return: Success or Fail
    """
    log.info(f"Market: {market}")
    log.info(f'Account to use: {account}')
    market = Market(market)
    ctx.bitshares.bundle = True
    market.cancel([
        x["id"] for x in market.accountopenorders(account)
    ], account=account)
    pprint(ctx.bitshares.txbuffer.broadcast())



if __name__ == "__main__":
#    market = "USD:BTS"
#    account = 'octet3'

    #USAGE: python3 bts_cancel_allorders.py cancelall "USD:BTS" --account octet3

    main()
