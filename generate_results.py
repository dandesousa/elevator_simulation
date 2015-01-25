#!/usr/bin/env python
# encoding: utf-8

from ggplot import *

import pandas as pd
import logging
import os

script_directory = os.path.dirname(os.path.realpath(__file__))
logger = logging.getLogger(__name__)


def get_args():
    from argparse import ArgumentParser
    parser = ArgumentParser(description="generates results for a run of the simulation")
    parser.add_argument("-v", "--verbose", action="count", help="the logging verbosity (more gives more detail)")
    parser.add_argument("-i", "--input_file", required=True, help="path to the simulation results csv file.")
    parser.add_argument("-d", "--output_dir", default=os.path.join(script_directory, "sim_results"), help="path to the output directory where plots should go (default: %(default)s)")
    args = parser.parse_args()

    if args.verbose == 1:
        level = logging.DEBUG
    else:
        level = logging.INFO

    logging.basicConfig(format="%(levelname)s %(asctime)s: %(message)s")
    logger.setLevel(level)

    return args


def main():
    args = get_args()
    df = pd.read_csv(args.input_file)

    # travel point plot
    p = ggplot(df, aes(x='elevator_called_secs', y='travel_secs')) + geom_point() + xlab('seconds since midnight') + ylab('travel time (seconds)') + ggtitle("Travel Time")
    pn = os.path.join(args.output_dir, "travel_time_point.png")
    logger.info("generating plot {}".format(pn))
    ggsave(p, pn)


if __name__ == '__main__':
    main()
