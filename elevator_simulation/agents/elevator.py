#!/usr/bin/env python
# encoding: utf-8

from elevator_simulation.agents import Agent
import logging


logger = logging.getLogger(__name__)


class ElevatorControllerAgent(Agent):
    """Docstring for ElevatorControllerAgent. """

    def __init__(self, sim, model, **kwargs):
        """Constructs an elevator controller agent for simpy.

        The elevator controller agent has information about how the elevator controller operates in the simulation.

        For example, the agent controls how quickly the elevator doors open and close, how quickly the elevators can
        move.

        """
        Agent.__init__(self, sim, model)

        self.elevator_called = self.env.event()
        self.elevator_agents = [ElevatorAgent(sim, elevator) for elevator in self.model.elevators]

    def call(self, floor, direction):
        """calls an elevator in this elevator bank.

        :param floor Floor: the floor it was called from
        :param direction int: the direction it was called for
        """
        elevator = self.model.call_elevator(floor, direction)
        agent = [agent for agent in self.elevator_agents if agent.model == elevator][0]
        agent.add_stop(floor)


class ElevatorAgent(Agent):
    """agent for an elevator"""
    def __init__(self, sim, model, **kwargs):
        """Constructs an elevator agent for simpy

        :param elevator_open_secs int: seconds it takes to open the elevator doors.
        :param elevator_close_secs int: seconds it takes to close the elevator doors.
        :param elevator_wait_secs int: seconds between the elevator doors opening and closing.
        :param elevator_travel_secs int: number of seconds to move between two levels in the building.
        """
        Agent.__init__(self, sim, model)
        self.action = self.env.process(self.run())

        # events in this simulation
        self.__new_stop_added = self.env.event()
        self.__arrived_at_floor = self.env.event()

        self.elevator_open_secs = kwargs.get("elevator_open_secs", 5)
        self.elevator_close_secs = kwargs.get("elevator_close_secs", 5)
        self.elevator_wait_secs = kwargs.get("elevator_wait_secs", 5)
        self.elevator_travel_secs = kwargs.get("elevator_travel_secs", 7)

        self.__passengers = set()

    # TODO this probably isnt safe, delete later and refactor test
    def __reset_event(self, event):
        ev = self.env.event()
        ev.callbacks = event.callbacks
        return ev

    def run(self):
        while True:
            # wait until we add a new stop to the elevator
            yield self.__new_stop_added
            self.__new_stop_added = self.env.event()

            # moves in the direction of stop
            yield from self.move()

    def move(self):
        """moves toward the destination until it runs out of stops"""
        while self.model.stops:
            logger.debug("elevator at {} must decide to move".format(self.model.location))
            direction = self.model.direction
            if self.model.location not in self.model.stops:
                logger.debug("elevator is not at one of the stops: {}".format(self.model.stops))
                moving_towards_stop = not all([self.model.moving_away(floor) for floor in self.model.stops])
                if not direction:
                    self.model.direction = 1
                    moving_towards_stop = not all([self.model.moving_away(floor) for floor in self.model.stops])
                    if not moving_towards_stop:
                        self.model.direction = -1
                elif direction and moving_towards_stop:
                    pass  # continue moving towards next location
                else:  # we need to switch directions
                    self.model.direction *= -1

                # move to the next floor
                logger.debug("adv {}".format(self.env.now))
                yield self.env.timeout(self.elevator_travel_secs)
                self.model.location = self.model.next_location
                logger.debug("done adv {}".format(self.env.now))
                self.__arrived_at_floor.succeed()
                self.__arrived_at_floor = self.__reset_event(self.__arrived_at_floor)
            else:
                logger.debug("elevator is located at a stop location")
                direction = 0  # don't move if we are at the stop

            if self.model.location in self.model.stops:
                logger.debug("elevator is at stop {}, opening doors".format(self.model.location))
                logger.debug(self.env.now)
                yield from self.open_doors()
                logger.debug(self.env.now)
                self.simulation.building_agent.elevator_available_event(self.model.location).succeed(self)
                self.simulation.building_agent.reset_elevator_available_event(self.model.location)
                yield from self.wait_for_passengers()
                yield from self.close_doors()


        logger.debug("elevator at {}, done moving no stops".format(self.model.location))
        # become idle, no more stops
        self.model.direction = 0

    def close_doors(self):
        yield self.env.timeout(self.elevator_close_secs)

    def wait_for_passengers(self):
        yield self.env.timeout(self.elevator_wait_secs)

    @property
    def total_elevator_travel_secs(self):
        return self.elevator_travel_secs + self.elevator_open_secs + self.elevator_close_secs + self.elevator_wait_secs

    def open_doors(self):
        yield self.env.timeout(self.elevator_open_secs)
        self.model.remove_stop(self.model.location)
        for person in self.__passengers:
            person.notify_floor_reached(self.model.location)

    def enter(self, person):
        self.__passengers.add(person)

    def exit(self, person):
        self.__passengers.remove(person)

    @property
    def arrived_at_floor_event(self):
        return self.__arrived_at_floor

    def add_stop(self, floor, add=True):
        """adds a new stop to the elevator and signals that it should start moving."""
        self.model.add_stop(floor)
        self.__new_stop_added.succeed()
