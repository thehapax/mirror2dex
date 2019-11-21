from uptick.decorators import unlock, online
from uptick.main import main

import bitshares.exceptions
import graphenecommon.exceptions
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
def cancel(ctx, market, account):
    """
    Cancel all orders in a market
    :param ctx: context
    :param market: market e.g.
    :param account: name of your bitshares acct
    :return: Success or Fail
    """
    try:
        log.info(f"Market: {market}")
        log.info(f'Account to use: {account}')
        market = Market(market)
        ctx.bitshares.bundle = True
        market.cancel([
            x["id"] for x in market.accountopenorders(account)
        ], account=account)
        log.info(ctx.bitshares.txbuffer.broadcast())

    except (bitshares.exceptions.AssetDoesNotExistsException):
        log.error(f"Asset does not exist: {market}")
    except (graphenecommon.exceptions.AccountDoesNotExistsException):
        log.error(f"Account does not exist: {account}")


if __name__ == "__main__":
    # example:
    market = "USD:BTS"
    account = 'my_account_name'

    # USAGE: python3 bts_cancel.py cancel "USD:BTS" --account my_account
    
    main()
