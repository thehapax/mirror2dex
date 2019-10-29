from bts_spread_mapper import setup_bitshares_market, get_ob_data, append_to_file
from plot_helper import plot_sequence
import logging

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
invert = False
enable_plot = True

if __name__ == '__main__':
    bts_market = setup_bitshares_market(bts_symbol)
    bts_df = get_ob_data(bts_market, depth, invert)

    try:
        # check length of output file
        file_length = max(open(output_file, 'r'), key=len)
    except FileNotFoundError as e:
        #first line
        bts_df = get_ob_data(bts_market, depth, invert)
        append_to_file(bts_df.to_csv(header=True, index=False), output_file)

    while True:
        try:
            bts_df = get_ob_data(bts_market, depth, invert)
            append_to_file(bts_df.to_csv(header=False, index=False), output_file)
            log.info(f'{title} {bts_symbol}:\n {bts_df}')
            if enable_plot:
                plot_sequence(bts_df, title, bts_symbol, invert, bar_width, poll_time)
        except Exception as e:
            log.error(e)
            break

