#!/usr/bin/env python
# encoding: utf-8

import logging
import random
import sys

from datetime import datetime, timedelta
from elevator_simulation.agents import Simulation, ElevatorBank, Person
from elevator_simulation.generators.json import write_simulation


logger = logging.getLogger(__name__)


def get_args():
    from argparse import ArgumentParser
    parser = ArgumentParser(description="Generates a simulation file.")
    parser.add_argument("-v", "--verbose", action="count", help="the logging verbosity (more gives more detail)")
    parser.add_argument("-p", "--people", required=True, type=int, help="the number of people in the building")
    parser.add_argument("--floors", default=9, type=int, help="the number of floors in the building (default: %(default)s)")
    parser.add_argument("--num_elevator_banks", default=1, type=int, help="the number of elevator banks in the building (default: %(default)s)")
    parser.add_argument("--num_elevators_per_bank", default=6, type=int, help="the number of elevators in each bank in the building (default: %(default)s)")
    parser.add_argument("--elevator_capacity", default=10, type=int, help="the number of people which fit in a single elevator at once (default: %(default)s)")
    parser.add_argument("--work_begin", default="6:00:00", help="the starting time for work starting for all people (default: %(default)s)")
    parser.add_argument("--work_end", default="10:00:00", help="the ending time for work starting for all people (default: %(default)s)")
    parser.add_argument("--work_length_mins", default=60*9, type=int, help="the length of time each person spends at the office for all people in minutes (default: %(default)s)")
    parser.add_argument("--lunch_begin", default="12:00:00", help="the start time for lunch for all people (default: %(default)s)")
    parser.add_argument("--lunch_end", default="13:00:00", help="the end time for lunch for all people (default: %(default)s)")
    parser.add_argument("--lunch_length_mins", default=45, type=int, help="the length of time taken for lunch for all people in minutes (default: %(default)s)")
    parser.add_argument("--lunch_on_floor", default=[], required=True, action="append", type=int, help="adds to the list of floors where people eat lunch (default: %(default)s)")
    parser.add_argument("--breaks_per_day", default=3, type=int, help="number of breaks for all people during the day (default: %(default)s)")
    parser.add_argument("--break_length_mins", default=15, type=int, help="the length of time taken for breaks for all people in minutes (default: %(default)s)")
    parser.add_argument("--call_strategy", default="call_strategy_random", choices=["call_strategy_random", "call_strategy_all"], help="the call strategy to be employed by the individuals in the simulation (default: %(default)s)")
    args = parser.parse_args()

    if args.verbose == 1:
        level = logging.DEBUG
    else:
        level = logging.INFO

    logging.basicConfig(format="%(levelname)s %(asctime)s: %(message)s")
    logger.setLevel(level)

    return args


def get_random_timedelta_in_interval(start_str, end_str):
    st = datetime.strptime(start_str, "%H:%M:%S")
    et = datetime.strptime(end_str, "%H:%M:%S")
    day = datetime(1900, 1, 1)

    std = st - day
    etd = et - day

    secs = int((etd-std).total_seconds())
    return std + timedelta(seconds=random.randint(0, secs))


def main():
    args = get_args()
    simulation = Simulation(number_of_floors=args.floors)

    # generator elevators
    for i in range(args.num_elevator_banks):
        eb = ElevatorBank(simulation)
        simulation.elevator_banks.append(eb)
        for j in range(args.num_elevators_per_bank):
            eb.add_elevator(capacity=args.elevator_capacity)

    # generate people
    for i in range(args.people):
        p = Person(simulation, call_strategy=args.call_strategy)
        simulation.people.append(p)

        # setup schedule for the following events:

        # start work
        td = get_random_timedelta_in_interval(args.work_begin, args.work_end)
        work_level = random.randint(1, args.floors-1)
        p.schedule.add_event(td, simulation.building.floors[work_level], "starting the work day")
        # end work
        td += timedelta(minutes=args.work_length_mins)
        p.schedule.add_event(td, simulation.building.floors[0], "ending the work day")

        # lunch time
        td = get_random_timedelta_in_interval(args.lunch_begin, args.lunch_end)
        lunch_level = sorted(args.lunch_on_floor, key=lambda l: abs(work_level-l))[0]
        p.schedule.add_event(td, simulation.building.floors[lunch_level-1], "going to lunch")

        # lunch end
        td += timedelta(minutes=args.lunch_length_mins)
        p.schedule.add_event(td, simulation.building.floors[work_level], "back to work after lunch")
        # each break generated
        # determine when the person should come to work
        # determine when t

    write_simulation(simulation, sys.stdout)


if __name__ == '__main__':
    main()
