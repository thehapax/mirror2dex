import matplotlib.pyplot as plt
import logging

log = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)

def plot_orderbook(ob_df, invert: bool, barwidth: float):
    # get order book and visualize quickly with matplotlib.
    plt.style.use('ggplot')
    bwidth = barwidth
    if bwidth is None:
        bwidth = 0.1

    ob_df['colors'] = 'g'
    ob_df.loc[ob_df.type == 'asks', 'colors'] = 'r'

    # for use with python 3.6.8
    price = ob_df.price.to_numpy()
    vol = ob_df.vol.to_numpy()

    plot_price = price
    if invert is True:
        ob_df['invert'] = 1 / ob_df['price']
        invert_price = ob_df.invert.to_numpy()  # use if needed
        plot_price = invert_price

    plt.bar(plot_price, vol, bwidth, color=ob_df.colors, align='center')
    # use below line if python 3.7, error with python 3.6.8
    # plt.bar(ob_df.price, ob_df.vol, color=ob_df.colors)


def plot_df(df, title: str, symbol: str, invert: bool, bar_width: float):
    # set up df for matplotlib
    plt.clf()
    plot_orderbook(df, invert=invert, barwidth=bar_width)
    plt.title(title + ":"+ symbol)
    plt.ylabel('volume')
    plt.xlabel('price')
    plt.tight_layout()


def plot_sequence(bts_df, title, bts_symbol, invert, bar_width, poll_time):
    # plot sequence for matplotlib 
    plt.ion()  # interactive plot
    plot_df(bts_df, title, bts_symbol, invert, bar_width)
    plt.pause(poll_time)
    plt.draw()

