#!/usr/bin/env python
# encoding: utf-8


class ElevatorTrip(object):
    """models data around an elevator trip"""
    __slots__ = ("elevator_called_secs",
                 "elevator_arrived_secs",
                 "travel_secs",
                 "person",
                 "start_location",
                 "end_location",
                 "event",
                 "direction",
                 "distance")

    def __init__(self):
        self.elevator_called_secs = None
        self.elevator_arrived_secs = None
        self.travel_secs = None
        self.person = None
        self.start_location = None
        self.end_location = None
        self.event = None
        self.direction = None
        self.distance = None

def to_csv_header(cls):
    return ",".join([str(attr) for attr in cls.__slots__])

def to_csv(obj):
    """returns the slotted object as a comma separated value string"""
    return ",".join([str(getattr(obj, attr)) for attr in obj.__class__.__slots__])
