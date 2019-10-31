from bts_spread_mapper import setup_bitshares_market, get_bts_ob_data
from plot_helper import plot_sequence
import logging

"""
Testing Bitshares exchange, grabs l2 orderbook, then plots it using matplotlib,
refreshing every 3 seconds. 
"""

log = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)

title = "Bitshares DEX"
bts_symbol = "OPEN.BTC/BTS"
output_file = "output_file.csv"
depth = 10
poll_time = 3  # time to wait before polling again
bar_width = 300
enable_plot = False


def append_to_file(txt, file):
    with open(file, 'a') as f:
        f.write(txt)


if __name__ == '__main__':
    bts_market = setup_bitshares_market(bts_symbol)
    bts_df = get_bts_ob_data(bts_market, depth)

    #get the headers for first reading and write to file
    try:
        # check length of output file
        file_length = max(open(output_file, 'r'), key=len)
    except FileNotFoundError as e:
        #first line
        bts_df = get_bts_ob_data(bts_market, depth)
        append_to_file(bts_df.to_csv(header=True, index=False), output_file)

    # for all subsequent writes drop the header
    while True:
        try:
            bts_df = get_bts_ob_data(bts_market, depth)
            append_to_file(bts_df.to_csv(header=False, index=False), output_file)
            log.info(f'{title} {bts_symbol}:\n {bts_df}')
            if enable_plot:
                plot_sequence(bts_df, title, bts_symbol, invert, bar_width, poll_time)
        except Exception as e:
            log.error(e)
            break

