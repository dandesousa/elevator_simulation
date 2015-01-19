#!/usr/bin/env python
# encoding: utf-8

import simpy
from datetime import timedelta
from elevator_simulation.models.person import Person


def call_strategy_all(elevator_banks):
    return tuple(elevator_banks)


def call_strategy_random(elevator_banks):
    import random
    bank_index = random.randint(0, len(elevator_banks)-1)
    return (elevator_banks[bank_index], )


def default_trip_complete(trip):
    print trip

class ElevatorTrip(object):
    __slots__ = ("elevator_called_secs", "elevator_arrived_secs", "travel_secs", "person",
                 "start_location", "end_location", "event", "direction", "distance")
    """Docstring for ElevatorTrip. """

    def __init__(self):
        """TODO: to be defined1. """
        self.elevator_called_secs = None
        self.elevator_arrived_secs = None
        self.travel_secs = None
        self.person = None
        self.start_location = None
        self.end_location = None
        self.event = None
        self.direction = None
        self.distance = None

    def __str__(self):
        return ",".join([getattr(self, attr) for attr in self.__slots__])


class PersonAgent(object):
    """Behavior for person agent"""
    def __init__(self, sim, model, **kwargs):
        """creates a person agent that defines how an individual behaves.

        :param elevator_call_strategy func: The strategy to use when deciding the elevator bank to use.
        :param trip_complete func: The function to invoke when elevator arrives (def: logs)
        """
        self.simulation = sim
        self.env = sim.env
        self.model = model
        self.action = self.env.process(self.run())
        self.call_strategy = kwargs("elevator_call_strategy", call_strategy_random)
        self.trip_complete = kwargs.get("trip_complete", default_trip_complete)

    def run(self):
        while True:
            now_td = timedelta(self.env.now)
            next_event = self.model.schedule.next_event(now_td)
            time_until_next_event = next_event.start_time - now_td

            # TODO: check if time is negative, if so, proceed directly without
            # waiting...
            # waits until the next event time
            yield self.env.timeout(time_until_next_event.total_seconds())

            trip = ElevatorTrip()
            trip.person = self.model
            trip.event = next_event
            trip.start_location = self.model.location
            trip.end_location = trip.event.location
            trip.distance = self.model.location.distance(next_event.location)
            trip.direction = self.model.location.direction(next_event.location)
            # TODO: correct later to check for stairs
            # determine whether to take the steps or call the elevator
            # if elevator, call elevator and wait
            trip.elevator_called_secs = self.env.now
            elevator_banks = self.call_strategy(self.simulation.elevator_bank_agents)
            for agent in elevator_banks:
                agent.call(trip.event, trip.direction)

            # Wait until notified of elevator open door on floor
            elevator_available = self.simulation.build_agent.elevator_available_event(trip.start_location)
            yield elevator_available
            elevator_agent = elevator_available.value
            trip.elevator_arrived_secs = self.env.now

            # TODO: update capacity
            elevator_agent.add_stop(trip.end_location)

            # TODO: need to wait for the elevator doors to open
            while elevator_agent.model.location != trip.end_location:
                yield elevator_agent.arrived_at_floor_event

            trip.travel_secs = self.env.now - trip.elevator_arrived_secs
            self.model.location = trip.end_location  # we reached our location, yay!
            self.trip_complete(trip)

            # TODO: ELEVATOR: check that we ONLY stop when we are going in the
                # direction of the user (we'll get them on the way back)
