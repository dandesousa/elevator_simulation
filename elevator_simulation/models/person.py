#!/usr/bin/env python
# encoding: utf-8


from collections import namedtuple
from datetime import timedelta
from elevator_simulation.models.building import Floor

Event = namedtuple("Event", "start_time location description")


class Schedule(object):
    """Class to model a work schedule.

    The schedule consists of list of ordered, non-overlapping events.
    Each event has a start time and location.

    Events relate directly to commands or places a person needs to be,
    for example:

        7am - Go To Work, Office Fl 7
        10am - Get Tea,   Office Fl 3
        12pm - Get Lunch, Office Fl 6
        4pm  - Go Home,   Office Fl 1
    """
    def __init__(self):
        self.__events = []

    @property
    def events(self):
        """Returns a tuple of events in this schedule."""
        return tuple(self.__events)

    def add_event(self, start_time, location, description="unknown event"):
        """Adds an event to the schedule.

        :param start_time timedelta: the time since midnight the event starts
        :param location Floor: the location the person should be
        """
        if not isinstance(start_time, timedelta):
            raise TypeError("Start time must be a timedelta since midnight")

        if not isinstance(location, Floor):
            raise TypeError("location must be of type {}".format(Floor.__name__))

        if start_time > timedelta(days=1) or start_time < timedelta():
            raise ValueError("Start time must be 0-1 day in length, timedelta since midnight")

        event = Event(start_time, location, description)
        self.__events.append(event)
        self.__events.sort()  # this is OK but we really should do an in place insert if we care about performance


class Person(object):
    """Class to model a person with a work schedule.
    """
    def __init__(self, **kwargs):
        """Creates a person with preferences and attributes.

        :param fitness int: combination measure of fitness and willingness to take the stairs (def: 1)
        """
        self.__schedule = Schedule()
        self.__location = None
        self.__fitness = kwargs.get("fitness", 1)

    @property
    def max_stair_levels_down(self):
        return self.__fitness

    @property
    def max_stair_levels_up(self):
        return max(0, self.__fitness - 1)

    @property
    def schedule(self):
        return self.__schedule

    @property
    def location(self):
        return self.__location

    @location.setter
    def location(self, value):
        # TODO: set location type, like None or Floor
        self.__location = value
