#!/usr/bin/env python
# encoding: utf-8


import logging
from elevator_simulation.agents import Simulation
from elevator_simulation.data import to_csv_header, ElevatorTrip
from elevator_simulation.readers.json import read_simulation

logger = logging.getLogger(__name__)


def get_args():
    from argparse import ArgumentParser
    parser = ArgumentParser(description="elevator simulation")
    parser.add_argument("-v", "--verbose", default=0, action="count", help="the logging verbosity (more gives more detail)")
    parser.add_argument("-i", "--input_file", type=str, help="the input simulation file")
    args = parser.parse_args()

    if args.verbose >= 1:
        level = logging.DEBUG
    else:
        level = logging.INFO

    logging.basicConfig(format="%(levelname)s %(asctime)s: %(message)s", level=level)

    return args


def main():
    """Main simulation loop.

    Each tick represents a second in 'real' time of the schedule.
    """
    args = get_args()

    simulation = read_simulation(args.input_file)
    print(to_csv_header(ElevatorTrip))
    simulation.run()


if __name__ == '__main__':
    main()
