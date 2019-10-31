import logging

log = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)


def single_trade_arb(cex_df, bts_df):
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
    """
    todo
    :param cex_df:
    :param bts_df:
    :return:
    """
    # normalize volue by placing [0,1] values into 'vol_scaled' column
    scaler = MinMaxScaler()
    asks_df['vol_scaled'] = scaler.fit_transform(asks_df['vol'].values.reshape(-1, 1))
    bids_df['vol_scaled'] = scaler.fit_transform(bids_df['vol'].values.reshape(-1, 1))

    asks_total = asks_df['vol_scaled'].sum()
    bids_total = bids_df['vol_scaled'].sum()

    # distribute balance across volume
    asks_dist = asks_bal/asks_total
    bids_dist = bids_bal/bids_total

    print(f"asks_total: {asks_total}, bids_total: {bids_total}")
    print(f"asks_DIST: {asks_dist}, bids_DIST: {bids_dist}")

    asks_df['vol_scaled'] = asks_df['vol_scaled'].mul(asks_dist)
    bids_df['vol_scaled'] = bids_df['vol_scaled'].mul(bids_dist)

    # remove zero row values for dex_vol
    asks_df = asks_df[asks_df['vol_scaled'] != 0]
    bids_df = bids_df[bids_df['vol_scaled'] != 0]

    # return and place orders on dex.
    return asks_df, bids_df


