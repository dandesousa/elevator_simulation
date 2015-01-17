#!/usr/bin/env python
# encoding: utf-8


import logging


logger = logging.getLogger(__name__)


def get_args():
    from argparse import ArgumentParser
    parser = ArgumentParser(description="elevator simulation")
    parser.add_argument("-v", "--verbose", action="count", help="the logging verbosity (more gives more detail)")
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

    import simpy
    env = simpy.Environment()

    def clock(env, name, tick):
        while True:
            print(name, env.now)
            yield env.timeout(tick)

    env.process(clock(env, 'fast', 0.5))
    env.process(clock(env, 'slow', 1.0))
    env.run(until=2)


if __name__ == '__main__':
    main()
