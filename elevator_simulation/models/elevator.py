#!/usr/bin/env python
# encoding: utf-8

from elevator_simulation.models.building import Floor

def nearest_elevator(ctrl, floor, direction):
    """A dispatch strategy for determining the elevator to dispatch to a caller

    :param ctrl ElevatorController: the elevator controller the request was made at.
    :param floor Floor: the floor the call occurred.
    :param direction int: the direction pressed by the user.
    """
    result = (None, -1)
    for elevator in ctrl.elevators:

        if elevator.moving_away(floor):
            suitability = 1
        elif elevator.direction == direction or not elevator.direction:  # moving in same or neutral direction
            suitability = len(ctrl.levels) + 2 - elevator.distance(floor)
        else:
            suitability = len(ctrl.levels) + 1 - elevator.distance(floor)

        best_elevator, best_suitability = result
        if suitability > best_suitability:
            result = (elevator, suitability)

    return result[0]


class ElevatorController(object):
    def __init__(self, floors=None, dispatch_strategy=None):
        """Constructs an elevator controller with a particular dispatch strategy.

        :param dispatch_strategy function: function that selects the elevator that should be dispatched.
        :note: dispatch strategy has a significant impact on elevator efficiency, by default it will
        use the nearest elevator strategy.
        """
        self.__elevators = set()
        self.__floors = tuple([] if not floors else floors)
        self.__dispatch_strategy = None

    @property
    def floors(self):
        return self.__floors

    @property
    def elevators(self):
        return tuple(self.__elevators)

    def add_elevator(self, **kwargs):
        elevator = Elevator(kwargs.get("capacity", None), self)
        self.__elevators.add(elevator)

    def call_elevator(self, floor, direction):
        """Asks to dispatch an elevator to the requested floor.

        Dispatches the elevator according to the elevator dispatch strategy set by the user.

        :param floor Floor: the floor the elevator should be sent to
        :param direction Direction: the direction the elevator caller wants to travel
        """
        elevator = self.__dispatch_strategy(self, floor, direction)
        # dispatch the elevator to get the user
        elevator.add_stop(floor, direction)


class Elevator(object):
    def __init__(self, capacity, ctrl):
        self.__capacity = capacity
        self.__ctrl = ctrl
        self.__direction = None
        self.__location = ctrl.floors[0]
        self.__stops = set()

    def distance(self, floor):
        """computes the distance between an elevator and the floor"""
        return abs(self.__location.level - floor.level)

    def moving_away(self, floor):
        """determines if the elevator in its current position and direction is moving away from the floor

        :param floor Floor: the floor to test if the elevator is moving away from.
        """
        d = self.distance(self.__location, floor)
        nd = self.distance(self.next_location(), floor)
        return nd > d

    @property
    def direction(self):
        return self.__direction

    @direction.setter
    def direction(self, value):
        valid_values = (1, -1, 0, None)
        if value not in valid_values:
            raise ValueError("Direction must be one of the following values: {}".format(valid_values))
        self.__direction = value

    @property
    def location(self):
        """gets the current location of the elevator"""
        return self.__location

    @location.setter
    def location(self, floor):
        """sets the location of the elevator"""
        if not isinstance(floor, Floor):
            raise TypeError("expected param floor to be of type {}".format(Floor.__name__))
        self.__location = floor

    @property
    def next_location(self):
        """Calculates the next expected location given the current position and direction.

        :rtype Floor: the next location where the elevator will be when it completes its next step.
        """
        if not self.__direction or not self.__location:
            return self.__location

        next_level = self.__location.level + self.__direction
        next_level = min(max(1, next_level), len(self.__ctrl.floors))  # boundaries check
        floor = self.__ctrl.floors[next_level - 1]
        return floor

    def add_stop(self, floor, direction):
        self.__stops.add(floor)

    def remove_stop(self, floor, direction):
        self.__stops.remove(floor)
