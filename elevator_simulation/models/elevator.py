#!/usr/bin/env python
# encoding: utf-8

from elevator_simulation.models.building import Floor


def nearest_elevator_dispatch_strategy(ctrl, floor, direction):
    """A dispatch strategy for determining the elevator to dispatch to a caller

    Follows the 'Nearest Elevator' algorithm as described in the following presentation:
        http://www.columbia.edu/~cs2035/courses/ieor4405.S13/p14.pdf

    :param ctrl ElevatorController: the elevator controller the request was made at.
    :param floor Floor: the floor the call occurred.
    :param direction int: the direction pressed by the user.
    """
    result = (None, -1)
    for elevator in ctrl.elevators:

        distance = elevator.distance(floor)

        if elevator.moving_away(floor) and distance:  # suitability shouldn't be low if we are on the same floor
            suitability = 1
        elif elevator.direction == direction or not elevator.direction:  # moving in same or neutral direction
            suitability = len(ctrl.floors) + 2 - distance
        else:
            suitability = len(ctrl.floors) + 1 - distance

        best_elevator, best_suitability = result
        if suitability > best_suitability:
            result = (elevator, suitability)

    return result[0]


class ElevatorController(object):
    def __init__(self, floors=None, dispatch_strategy=nearest_elevator_dispatch_strategy):
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
        """Returns a tuple of the floors serviced by the elevator controller"""
        return self.__floors

    @property
    def elevators(self):
        """Returns a tuple of the elevators in the elevator bank"""
        return tuple(self.__elevators)

    def add_elevator(self, **kwargs):
        """Adds an eleavtor to the elevator bank of this controller.

        See Elevator.__init__ for parameters

        :rtype Elevator: Returns the elevator that was created
        """
        elevator = Elevator(self, **kwargs)
        self.__elevators.add(elevator)
        return elevator

    def call_elevator(self, floor, direction):
        """Asks to dispatch an elevator to the requested floor.

        Dispatches the elevator according to the elevator dispatch strategy set by the user.

        :param floor Floor: the floor the elevator should be sent to
        :param direction Direction: the direction the elevator caller wants to travel

        """
        elevator = self.__dispatch_strategy(self, floor, direction)
        return elevator


class Elevator(object):
    def __init__(self, ctrl, **kwargs):
        """Creates an elevator with the given settings.

        :param ctrl ElevatorController: Reference to the controller that owns the elevator
        :param capacity int: the maximum number of people allowed on this elevator (def: 10)
        :param starting_location floor: the initial starting location for this elevator (def: 1st floor)
        """
        self.__ctrl = ctrl
        self.__stops = set()
        self.__capacity = kwargs.get("capacity", 10)
        self.direction = None
        self.location = kwargs.get("starting_location", ctrl.floors[0])

    @property
    def capacity(self):
        """the maximum number of people allowed on this elevator."""
        return self.__capacity

    def distance(self, floor):
        """computes the distance between an elevator and the floor"""
        return self.location.distance(floor)

    def moving_away(self, floor):
        """determines if the elevator in its current position and direction is moving away from the floor

        :param floor Floor: the floor to test if the elevator is moving away from.
        """
        return self.next_location.distance(floor) > self.location.distance(floor)

    @property
    def direction(self):
        """Returns the direction the elevator is currently travelling"""
        return self.__direction

    @direction.setter
    def direction(self, value):
        """Property to set the direction.

        :param value int: the value indicating the direction (1 - up, -1 - down, 0 / None - idle)
        """
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
        if not self.direction or not self.location:
            return self.location

        next_level = self.location.level + self.direction
        next_level = min(max(1, next_level), len(self.__ctrl.floors))  # boundaries check
        floor = self.__ctrl.floors[next_level - 1]
        return floor

    @property
    def stops(self):
        """Returns the floors that the elevator should stop on"""
        return frozenset(self.__stops)

    def add_stop(self, floor):
        """Adds a floor to the list of floors the elevator should stop on

        :param floor Floor: floor to stop on
        """
        if floor in self.__ctrl.floors:
            self.__stops.add(floor)
        else:
            raise ValueError("Floor does not exist in the list of valid floors for this elevator".format(floor))

    def remove_stop(self, floor):
        """Removes a floor from the list of floors the elevator should stop on

        :param floor Floor: floor to remove stop from
        """
        if floor in self.__stops:
            self.__stops.remove(floor)
        else:
            raise ValueError("Floor cannot be removed because it is not a stop on the elevator".format(floor))

    def __repr__(self):
        return "<Elevator(location={}, direction={}>".format(self.location, self.direction)
