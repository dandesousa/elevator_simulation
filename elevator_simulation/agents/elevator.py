#!/usr/bin/env python
# encoding: utf-8

import simpy
from elevator_simulation.models.elevator import ElevatorController


class ElevatorConrollerAgent(object):

    """Docstring for ElevatorControllerAgent. """

    def __init__(self, env, **kwargs):
        """Constructs an elevator controller agent for simpy.

        The elevator controller agent has information about how the elevator controller operates in the simulation.

        For example, the agent controls how quickly the elevator doors open and close, how quickly the elevators can
        move.

        """
        self.env = env

        self.elevator_called = self.env.event()
        self.model = ElevatorController()
        # TODO: construct the model

        self.action = env.process(self.run())
        self.elevator_agents = [ElevatorAgent(env, elevator) for elevator in self.model.elevators]

    def run(self):
        """defines the behavior of the elevator controller in the simulation"""
        while True:
            # wait to take an action until the elevator is called
            #yield self.elevator_called
            yield self.env.timeout(100)

    def call(self, floor, direction):
        """calls an elevator in this elevator bank.

        :param floor Floor: the floor it was called from
        :param direction int: the direction it was called for
        """
        elevator = self.model.call_elevator(floor, direction)
        agent = [agent for agent in self.elevator_agents if agent.model == elevator][0]
        agent.add_stop(floor)
        #self.elevator_called.succeed()


class ElevatorAgent(object):
    """agent for an elevator"""
    def __init__(self, env, elevator, **kwargs):
        """Constructs an elevator agent for simpy

        :param elevator_open_secs int: seconds it takes to open the elevator doors.
        :param elevator_close_secs int: seconds it takes to close the elevator doors.
        :param elevator_wait_secs int: seconds between the elevator doors opening and closing.
        :param elevator_travel_secs int: number of seconds to move between two levels in the building.
        """
        self.env = env
        self.model = elevator
        self.action = env.process(self.run())

        # events in this simulation
        self.__new_stop_added = env.event()
        self.__arrived_at_floor = env.event()

        self.elevator_open_secs = kwargs.get("elevator_open_secs", 5)
        self.elevator_close_secs = kwargs.get("elevator_close_secs", 5)
        self.elevator_wait_secs = kwargs.get("elevator_wait_secs", 5)
        self.elevator_travel_secs = kwargs.get("elevator_travel_secs", 7)

    def __reset_event(self, event):
        ev = self.env.event()
        ev.callbacks = event.callbacks
        return ev

    def run(self):
        while True:
            # wait until we add a new stop to the elevator
            yield self.__new_stop_added
            self.__new_stop_added = self.__reset_event(self.__new_stop_added)

            # moves in the direction of stop
            yield from self.move()

    def move(self):
        """moves toward the destination until it runs out of stops"""
        while self.model.stops:
            direction = self.model.direction
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
            yield from self.advance_to_next_location()

            if self.model.location in self.model.stops:
                yield from self.open_doors()
                yield from self.wait_for_passengers()
                yield from self.close_doors()


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

    def advance_to_next_location(self):
        yield self.env.timeout(self.elevator_travel_secs)
        self.model.location = self.model.next_location
        self.__arrived_at_floor.succeed()
        self.__arrived_at_floor = self.__reset_event(self.__arrived_at_floor)

    @property
    def arrived_at_floor_event(self):
        return self.__arrived_at_floor

    def add_stop(self, floor, add=True):
        """adds a new stop to the elevator and signals that it should start moving."""
        self.model.add_stop(floor)
        self.__new_stop_added.succeed()
