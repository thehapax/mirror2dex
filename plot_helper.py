import matplotlib.pyplot as plt
from ascii_graph import Pyasciigraph
from ascii_graph.colors import Red, Gre, Yel, Blu
import logging

log = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)

def format_df_ascii(df):
    # ascii CLI graph - order book coloring for primary order book red/green.
    # colors for your mirror orders, yellow/blue
    ob_color = {'asks': Red, 'bids': Gre, 'mirror_asks': Yel, 'mirror_bids': Blu}
    # replace asks and bids with corresponding color
    df.loc[df['type'] == 'asks', 'type'] = ob_color['asks']
    df.loc[df['type'] == 'bids', 'type'] = ob_color['bids']
    df = df[['price', 'vol', 'type']]
    return df


def dynamic_ascii_plot(df, title):
    graph = Pyasciigraph(
        line_length=120,
        min_graph_length=50,
        separator_length=4,
        multivalue=True,
        human_readable='si',
        float_format='{0:,.6f}')

    # convert to tuple for ascii graph
    tuple_data = [tuple(x) for x in df.values]

    for line in graph.graph(label=title, data=tuple_data):
        log.info(line)



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
    plt.clf()
    plot_orderbook(df, invert=invert, barwidth=bar_width)
    plt.title(title + ":"+ symbol)
    plt.ylabel('volume')
    plt.xlabel('price')
    plt.tight_layout()


def plot_sequence(bts_df, title, bts_symbol, invert, bar_width, poll_time):
    plt.ion()  # interactive plot
    plot_df(bts_df, title, bts_symbol, invert, bar_width)
    plt.pause(poll_time)
    plt.draw()

