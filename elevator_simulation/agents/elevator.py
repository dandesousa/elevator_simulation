#!/usr/bin/env python
# encoding: utf-8

from elevator_simulation.agents import AgentMixin
from elevator_simulation.models import ElevatorBank as ElevatorBankModel
from elevator_simulation.models import Elevator as ElevatorModel
import logging


logger = logging.getLogger(__name__)


class ElevatorBank(AgentMixin, ElevatorBankModel):
    """Docstring for ElevatorControllerAgent. """

    def __init__(self, sim, **kwargs):
        """Constructs an elevator controller agent for simpy.

        The elevator controller agent has information about how the elevator controller operates in the simulation.

        For example, the agent controls how quickly the elevator doors open and close, how quickly the elevators can
        move.
        """
        AgentMixin.__init__(self, sim, events=["elevator_door_open", "elevator_moving_on"])
        kwargs["elevator_cls"] = Elevator  # elevator class to instantiate on calls to add_elevator
        ElevatorBankModel.__init__(self, sim.building.floors, **kwargs)

        self.register_event_callback("elevator_door_open", self.__elevator_door_open)
        self.register_event_callback("elevator_moving_on", self.__elevator_moving_on)

    def __elevator_moving_on(self, event):
        elevator = event.value
        direction = elevator.direction
        logger.debug("elevator({}) is moving on, notifying all people waiting on floor({}) to go {}".format(elevator.uuid, elevator.location.level, direction))
        for person in self.waiting_passengers(elevator.location, direction):
            person.notify_event("elevator_moving_on", elevator)

    def __elevator_door_open(self, event):
        elevator = event.value
        direction = elevator.next_direction
        if not direction:
            direction = 1 if self.waiting_passengers(elevator.location, 1) else -1
        for person in self.waiting_passengers(elevator.location, direction):
            person.notify_event("elevator_door_open", elevator)

    def _create_elevator(self, **kwargs):
        """wrapper for creating an elevator object"""
        kwargs["elevator_bank"] = self
        return self._elevator_cls(self.simulation, self.floors, **kwargs)


class Elevator(AgentMixin, ElevatorModel):
    """agent for an elevator"""
    def __init__(self, sim, floors, **kwargs):
        """Constructs an elevator agent for simpy

        :param elevator_bank ElevatorBank: the owning elevator bank
        :param elevator_open_secs int: seconds it takes to open the elevator doors.
        :param elevator_close_secs int: seconds it takes to close the elevator doors.
        :param elevator_wait_secs int: seconds between the elevator doors opening and closing.
        :param elevator_travel_secs int: number of seconds to move between two levels in the building.
        """
        AgentMixin.__init__(self, sim, events=["new_stop_added"])
        ElevatorModel.__init__(self, floors, **kwargs)
        self.action = self.env.process(self.run())
        self.__elevator_bank = kwargs["elevator_bank"]


        self.elevator_open_secs = kwargs.get("elevator_open_secs", 5)
        self.elevator_close_secs = kwargs.get("elevator_close_secs", 5)
        self.elevator_wait_secs = kwargs.get("elevator_wait_secs", 5)
        self.elevator_travel_secs = kwargs.get("elevator_travel_secs", 7)

    def run(self):
        while True:
            # wait until we add a new stop to the elevator
            yield self.event("new_stop_added")

            # moves in the direction of stop
            yield from self.move()

    def move(self):
        """moves toward the destination until it runs out of stops"""
        while self.stops:
            logger.debug("{}: elevator({}) moving {} on {}".format(self.env.now, self.uuid, self.direction, self.location))
            if self.location not in self.stops:
                self.__elevator_bank.notify_event("elevator_moving_on", self)
                if self.direction != self.next_direction:
                    logger.debug("{}: elevator({}) changed direction {}".format(self.env.now, self.uuid, self.next_direction))
                self.direction = self.next_direction

                # move to the next floor
                yield self.env.timeout(self.elevator_travel_secs)
                self.location = self.next_location
                for person in self.passengers:
                    person.notify_event("floor_reached", self.location)
            else:
                logger.debug("elevator({}) is located at a stop location".format(self.uuid))

            if self.location in self.stops:
                logger.debug("elevator is at stop {}, opening doors".format(self.location))
                yield from self.__open_doors()
                yield from self.wait_for_passengers()
                yield from self.__close_doors()

        self.direction = 0  # idle, no more stops

    def __open_doors(self):
        yield self.env.timeout(self.elevator_open_secs)
        self.open_doors()
        self.remove_stop(self.location)
        for person in self.passengers:
            person.notify_event("elevator_door_open", self)
        self.__elevator_bank.notify_event("elevator_door_open", self)

    def __close_doors(self):
        yield self.env.timeout(self.elevator_close_secs)
        self.close_doors()

    def wait_for_passengers(self):
        yield self.env.timeout(self.elevator_wait_secs)

    @property
    def total_elevator_travel_secs(self):
        return self.elevator_travel_secs + self.elevator_open_secs + self.elevator_close_secs + self.elevator_wait_secs

    def add_stop(self, floor, add=True):
        """adds a new stop to the elevator and signals that it should start moving."""
        ElevatorModel.add_stop(self, floor)
        self.notify_event("new_stop_added")
