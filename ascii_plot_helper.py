from ascii_graph import Pyasciigraph
from ascii_graph.colors import Red, Gre, Yel, Blu
import logging

log = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)

def format_df_ascii(df):
    """
    format df so that it can be plotted with ascii graph
    :param df: df
    :return: colorized df in type column
    """
    # ascii CLI graph - order book coloring for primary order book red/green.
    # colors for your mirror orders, yellow/blue
    ob_color = {'asks': Red, 'bids': Gre, 'mirror_asks': Yel, 'mirror_bids': Blu}
    # replace asks and bids with corresponding color
    df.loc[df['type'] == 'asks', 'type'] = ob_color['asks']
    df.loc[df['type'] == 'bids', 'type'] = ob_color['bids']

    df.loc[df['type'] == 'mirror_asks', 'type'] = ob_color['mirror_asks']
    df.loc[df['type'] == 'mirror_bids', 'type'] = ob_color['mirror_bids']

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


