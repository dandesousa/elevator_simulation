#!/usr/bin/env python
# encoding: utf-8

from elevator_simulation.agents import AgentMixin
from elevator_simulation.models import ElevatorBank as ElevatorBankModel
from elevator_simulation.models import Elevator as ElevatorModel
import logging


logger = logging.getLogger(__name__)


class ElevatorBank(AgentMixin, ElevatorBankModel):
    """Docstring for ElevatorControllerAgent. """

    def __init__(self, sim, floors, **kwargs):
        """Constructs an elevator controller agent for simpy.

        The elevator controller agent has information about how the elevator controller operates in the simulation.

        For example, the agent controls how quickly the elevator doors open and close, how quickly the elevators can
        move.
        """
        AgentMixin.__init__(self, sim)
        kwargs["elevator_cls"] = Elevator  # elevator class to instantiate on calls to add_elevator
        ElevatorBankModel.__init__(self, floors, **kwargs)

        self.elevator_called = self.env.event()
        self.elevator_agents = [ElevatorAgent(sim, elevator) for elevator in self.elevators]

    def _create_elevator(self, **kwargs):
        """wrapper for creating an elevator object"""
        return self._elevator_cls(self.simulation, self.floors, **kwargs)


class Elevator(AgentMixin, ElevatorModel):
    """agent for an elevator"""
    def __init__(self, sim, floors, **kwargs):
        """Constructs an elevator agent for simpy

        :param elevator_open_secs int: seconds it takes to open the elevator doors.
        :param elevator_close_secs int: seconds it takes to close the elevator doors.
        :param elevator_wait_secs int: seconds between the elevator doors opening and closing.
        :param elevator_travel_secs int: number of seconds to move between two levels in the building.
        """
        AgentMixin.__init__(self, sim)
        ElevatorModel.__init__(self, floors, **kwargs)
        self.action = self.env.process(self.run())

        # events in this simulation
        self.__new_stop_added = self.env.event()
        self.__arrived_at_floor = self.env.event()

        self.elevator_open_secs = kwargs.get("elevator_open_secs", 5)
        self.elevator_close_secs = kwargs.get("elevator_close_secs", 5)
        self.elevator_wait_secs = kwargs.get("elevator_wait_secs", 5)
        self.elevator_travel_secs = kwargs.get("elevator_travel_secs", 7)


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
        while self.stops:
            logger.debug("elevator at {} must decide to move".format(self.location))
            direction = self.direction
            if self.location not in self.stops:
                logger.debug("elevator is not at one of the stops: {}".format(self.stops))
                moving_towards_stop = not all([self.moving_away(floor) for floor in self.stops])
                if not direction:
                    self.direction = 1
                    moving_towards_stop = not all([self.moving_away(floor) for floor in self.stops])
                    if not moving_towards_stop:
                        self.direction = -1
                elif direction and moving_towards_stop:
                    pass  # continue moving towards next location
                else:  # we need to switch directions
                    self.direction *= -1

                # move to the next floor
                logger.debug("adv {}".format(self.env.now))
                yield self.env.timeout(self.elevator_travel_secs)
                self.location = self.next_location
                logger.debug("done adv {}".format(self.env.now))
                self.__arrived_at_floor.succeed()
                self.__arrived_at_floor = self.__reset_event(self.__arrived_at_floor)
            else:
                logger.debug("elevator is located at a stop location")
                direction = 0  # don't move if we are at the stop

            if self.location in self.stops:
                logger.debug("elevator is at stop {}, opening doors".format(self.location))
                logger.debug(self.env.now)
                yield from self.__open_doors()
                logger.debug(self.env.now)
                self.simulation.building.elevator_available_event(self.location).succeed(self)
                self.simulation.building.reset_elevator_available_event(self.location)
                yield from self.wait_for_passengers()
                yield from self.__close_doors()


        logger.debug("elevator at {}, done moving no stops".format(self.location))
        # become idle, no more stops
        self.direction = 0

    def __open_doors(self):
        yield self.env.timeout(self.elevator_open_secs)
        self.open_doors()
        self.remove_stop(self.location)
        for person in self.passengers:
            person.notify_floor_reached(self.location)

    def __close_doors(self):
        yield self.env.timeout(self.elevator_close_secs)
        self.close_doors()

    def wait_for_passengers(self):
        yield self.env.timeout(self.elevator_wait_secs)

    @property
    def total_elevator_travel_secs(self):
        return self.elevator_travel_secs + self.elevator_open_secs + self.elevator_close_secs + self.elevator_wait_secs

    @property
    def arrived_at_floor_event(self):
        return self.__arrived_at_floor

    def add_stop(self, floor, add=True):
        """adds a new stop to the elevator and signals that it should start moving."""
        ElevatorModel.add_stop(self, floor)
        self.__new_stop_added.succeed()
