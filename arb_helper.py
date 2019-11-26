import logging
from sklearn.preprocessing import MinMaxScaler, StandardScaler

log = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)


def single_trade_arb(cex_df, bts_df):
    """
    calculat if profitable simple arb is possible based on cex/dex df
    :param cex_df: centralized exchange order book
    :param bts_df: bitshares exchange order book
    :return:
    """
    # get closest bid/ask
    # todo : get closese bid/ask with actual tradeable volume, not dust, and not below min trade limit.
    cex_spread_df = cex_df[cex_df.index == 0]  # get closest bid/ask
    bts_spread_df = bts_df[bts_df.index == 0]
    calculate_arb_opp(cex_spread_df, bts_spread_df)


def get_ordersize():
    """
    place holder for getting proposed order size based on reserves
    available on exchange.
    :return:
    """
    return 0.01


def calculate_arb_opp(cex_df, bts_df):  # calculate arbitrage opportunity
    """
    Calculate arb opportunity based on cex and dex orderbooks.
    :param cex_df:
    :param bts_df:
    :return:
    """
    log.info("Calculate Arbitrage Opportunity")
    # look at lowest ask and highest bid
    # if dex ask price is > cex ask,  take cex ask and sell on dex. (account for fees)
    # assumes spread on cex is narrower than dex
    # bids? if cex bid > dex bid, take cex bid and list bid on dex. (+ fees)
    cex_ask = float(cex_df[cex_df['type'] == 'asks'].price)
    dex_ask = float(bts_df[bts_df['type'] == 'asks'].price)

    cex_bid = float(cex_df[cex_df['type'] == 'bids'].price)
    dex_bid = float(bts_df[bts_df['type'] == 'bids'].price)

    cex_spread = cex_ask - cex_bid
    too_small = 10 # random number now, but how do we determine if spread too small
    # percentage of asset?

    if cex_spread < too_small:
        print("cex spread too small: ", cex_spread)
   #     return

    if dex_ask > cex_ask:
        diff = dex_ask - cex_ask
        size = get_ordersize()
        # buy on cex 10189 for 0.01 btc
        # sell on dex at 10399 for 0.01 btc.
        # where dex lowest ask is 10400

        print("profit opportunity for ask trade: ",  diff, "difference * vol =", diff*size)

        my_dex_ask = dex_ask - 0.001*dex_ask # make yours lower than lowest ask by 0.1%
        # make sure that my_dex_ask is crossing into bid? (or should it?)

        # check if my_dex_ask is not lower than highest bid
        print("buy on cex at: ", cex_ask, "sell on dex at: ", my_dex_ask )

#        log.info("take cex ask, make on dex")
#        buy on cex, sell on dex at same price - fees
#        print("cex ask: ", cex_ask, "bts ask: ", dex_ask)

    # todo below
    if cex_bid > dex_bid:
        log.info("take cex bid and list bid on dex")
        print("cex bid: ", cex_bid, "dex bid: ", dex_bid)
    # add fees! calculation


def get_cex_mirror(asks_df, bids_df, asks_bal, bids_bal):
    # how we selected the scaling method, MinMaxScaler()
    # https://towardsdatascience.com/scale-standardize-or-normalize-with-scikit-learn-6ccc7d176a02
    """
    todo
    get scaled mirror of cex in dex dataframe
    uses entire balance give an as arugments here.
    percentage of balance must be specified outside of this method
    :param cex_df:
    :param bts_df:
    :return:
    """
    # normalize volume by placing [0,1] values into 'vol_scaled' column
    try:
        asks_df = asks_df.rename(columns={"vol": "cex_vol"})
        bids_df = bids_df.rename(columns={"vol": "cex_vol"})

        scaler = MinMaxScaler()
        asks_df['vol'] = scaler.fit_transform(asks_df['cex_vol'].values.reshape(-1, 1))
        bids_df['vol'] = scaler.fit_transform(bids_df['cex_vol'].values.reshape(-1, 1))

        # remove zero row values for vol
        asks_df = asks_df[asks_df['vol'] != 0]
        bids_df = bids_df[bids_df['vol'] != 0]

        asks_total = asks_df['vol'].sum()
        bids_total = bids_df['vol'].sum()

        if (bids_total == 0) or (asks_total == 0):
            # avoid division by zero
            return None, None

        # distribute balance across volume
        asks_dist = asks_bal/asks_total
        bids_dist = bids_bal/bids_total

        log.debug(f"asks_total: {asks_total}, bids_total: {bids_total}")
        log.debug(f"asks_DIST: {asks_dist}, bids_DIST: {bids_dist}")

        asks_df['vol'] = asks_df['vol'].mul(asks_dist)
        bids_df['vol'] = bids_df['vol'].mul(bids_dist)

        asks_df.loc[asks_df['type'] == 'asks', 'type'] = 'mirror_asks'
        bids_df.loc[bids_df['type'] == 'bids', 'type'] = 'mirror_bids'

        asks_df.drop(columns=['cex_vol'], inplace=True)
        bids_df.drop(columns=['cex_vol'], inplace=True)

        # order columns properly
        asks_df = asks_df[['price', 'vol', 'timestamp', 'type']]
        bids_df = bids_df[['price', 'vol', 'timestamp', 'type']]
        # return and place orders on dex.
        return asks_df, bids_df

    except Exception as e:
        log.error(e)
        return None, None



